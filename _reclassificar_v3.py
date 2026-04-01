"""
Reclassificacao completa dos parceiros v3
- 6 categorias: Diamante, Prata, Pipeline, Em Recuperacao, Inativo, Fantasma (Pipeline absorve Novo)
- ISP reformulado: nao penaliza sazonalidade, nao premia frequencia vazia
- Flags especiais: sazonal, em_recuperacao, novo, fantasma (sem termo 'ressuscitado')
- Classificacao de envio: consistente, regular, esporadico, novo, sem envio
- Metricas semanais e mensais
"""
import json
import win32com.client
import pythoncom
from collections import defaultdict
from datetime import datetime

pythoncom.CoInitialize()

ARQUIVO = (
    r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA"
    r"\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca\Analise Parcerias.xlsx"
)
JSON_PATH = (
    r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA"
    r"\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca\parceiros_data.json"
)

def to_float(v):
    try: return float(v) if v and str(v).strip() not in ("[NULL]","","None") else 0
    except: return 0
def to_int(v):
    try: return int(float(v)) if v and str(v).strip() not in ("[NULL]","","None") else 0
    except: return 0

import re
def normalizar_nome(nome):
    """Remove prefixo CPF/CNPJ (ex: '57.893.313 HYAN NOGUEIRA' -> 'HYAN NOGUEIRA')
    e limpa nomes numéricos inválidos."""
    if not nome:
        return nome
    s = str(nome).strip()
    # Remove prefixo numérico tipo CPF/CNPJ: dígitos, pontos, traços, barras seguidos de espaço
    s = re.sub(r'^\d[\d.\-/]*\s+', '', s).strip()
    # Se ficou vazio ou só número, retorna original
    if not s or s.replace('.','').replace('-','').isdigit():
        return str(nome).strip()
    return s

# ============================================================
# 1. LER DADOS BRUTOS DO EXCEL
# ============================================================
print("Lendo Excel...")
excel = win32com.client.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

wb = excel.Workbooks.Open(ARQUIVO, CorruptLoad=1)

hoje = datetime.now()
sem_atual = hoje.isocalendar()[1]
ano_atual = hoje.year

# BD_EnvioParceiros
ws_e = wb.Worksheets("BD_EnvioParceiros")
ult_e = ws_e.Cells(ws_e.Rows.Count, 1).End(-4162).Row
print(f"  Envios: {ult_e} linhas")

envio = defaultdict(lambda: {
    "total": 0, "meses_set": set(), "por_semana": defaultdict(int),
    "por_mes": defaultdict(int), "primeira_sem": None, "ultima_sem": None,
    "regionais": defaultdict(int),
})

linhas_filtradas = 0
linhas_total = 0

for r in range(2, ult_e + 1):
    linhas_total += 1
    nome = ws_e.Cells(r, 25).Value
    nome_raw = ws_e.Cells(r, 1).Value
    # Fallback: se Nome Ajustado é erro COM (#N/A = -2146826246) ou número, usar nome raw
    if nome is None or (isinstance(nome, (int, float)) and nome < 0):
        nome = nome_raw
    # Filtro obrigatório: apenas Varejo = "sim" (col 21)
    varejo = ws_e.Cells(r, 21).Value
    if not varejo or str(varejo).strip().lower() != "sim":
        continue
    linhas_filtradas += 1
    sem = to_int(ws_e.Cells(r, 20).Value)
    ano = to_int(ws_e.Cells(r, 22).Value)
    mes = to_int(ws_e.Cells(r, 19).Value)
    regional_envio = ws_e.Cells(r, 24).Value
    if not nome: continue
    nome = normalizar_nome(nome)
    if not nome: continue
    p = envio[nome]
    # Contagem por linha (cada registro = 1 lead)
    p["total"] += 1
    if regional_envio:
        p["regionais"][str(regional_envio).strip()] += 1
    p["meses_set"].add(f"{mes:02d}/{ano}")
    if ano >= 2025:
        p["por_semana"][(ano, sem)] += 1
        p["por_mes"][(ano, mes)] += 1
    key = (ano, sem)
    if p["primeira_sem"] is None or key < p["primeira_sem"]:
        p["primeira_sem"] = key
    if p["ultima_sem"] is None or key > p["ultima_sem"]:
        p["ultima_sem"] = key

print(f"  Filtro Varejo=sim: {linhas_filtradas}/{linhas_total} linhas ({linhas_filtradas*100//max(1,linhas_total)}%)")
print(f"  Contagem por linha (cada registro = 1 lead)")

# BD_Parceiros (fonte de UF)
ws_parc = wb.Worksheets("BD_Parceiros")
ult_parc = ws_parc.Cells(ws_parc.Rows.Count, 1).End(-4162).Row
print(f"  Parceiros (BD_Parceiros): {ult_parc} linhas")

parceiros_uf = {}
for r in range(2, ult_parc + 1):
    nome_aj = ws_parc.Cells(r, 7).Value  # Nome Ajustado
    uf_val = ws_parc.Cells(r, 2).Value    # UF
    if nome_aj and uf_val:
        nome_aj_norm = normalizar_nome(str(nome_aj).strip())
        parceiros_uf[nome_aj_norm] = str(uf_val).strip().upper()

print(f"  UFs mapeadas: {len(parceiros_uf)}")

# BD_Pagos
ws_p = wb.Worksheets("BD_Pagos")
ult_p = ws_p.Cells(ws_p.Rows.Count, 1).End(-4162).Row
print(f"  Pagos: {ult_p} linhas")

pagos = defaultdict(lambda: {"total": 0, "compra": 0, "liq": 0, "ultimo_pago": (0, 0),
                              "por_semana": defaultdict(int), "primeira_sem": None,
                              "ufs": defaultdict(int)})
for r in range(2, ult_p + 1):
    nome = ws_p.Cells(r, 60).Value
    # Fallback: se Nome Ajustado é erro COM, usar col 17 (intermediário) ou ignorar
    if nome is not None and isinstance(nome, (int, float)) and nome < 0:
        nome_int = ws_p.Cells(r, 17).Value
        if nome_int and not (isinstance(nome_int, (int, float)) and nome_int < 0):
            nome = nome_int
        else:
            continue  # pular linha com erro irreparável
    compra = to_float(ws_p.Cells(r, 12).Value)
    liq = to_float(ws_p.Cells(r, 10).Value)
    ano = to_int(ws_p.Cells(r, 57).Value)
    sem = to_int(ws_p.Cells(r, 58).Value)
    # UF from Estado Processo (col 2) or Regional (col 40)
    uf_raw = ws_p.Cells(r, 2).Value
    if not nome or str(nome).strip().upper() == "NAO INFORMADO": continue
    nome = normalizar_nome(nome)
    if not nome: continue
    p = pagos[nome]
    p["total"] += 1
    p["compra"] += compra
    p["liq"] += liq
    if uf_raw and str(uf_raw).strip():
        uf_val = str(uf_raw).strip().upper()
        if len(uf_val) == 2 and uf_val.isalpha():
            p["ufs"][uf_val] += 1
    if ano >= 2025:
        p["por_semana"][(ano, sem)] += 1
    key = (ano, sem)
    if p["primeira_sem"] is None or (key > (0, 0) and key < p["primeira_sem"]):
        p["primeira_sem"] = key
    if key > p["ultimo_pago"]:
        p["ultimo_pago"] = key

wb.Close(False)
excel.Quit()

# ============================================================
# 1.5 MERGE NOMES DUPLICADOS
# ============================================================
import re

MERGE_MAP = {
    "ANTECIPE PRECATORIOS LTDA": "ANTECIPE INVESTIMENTOS EM DIREITO CREDITORIO LTDA",
    "LUGE": "LUGE ASSESSORIA LTDA",
    "AL MENDEZ REPRESENTACOES": "AL MENDEZ REPRESENTACOES LTDA",
}

def merge_into(source_name, target_name, envio_dict, pagos_dict):
    """Merge source into target, combining all data"""
    if source_name not in envio_dict and source_name not in pagos_dict:
        return
    # Merge envio
    if source_name in envio_dict:
        src = envio_dict[source_name]
        tgt = envio_dict[target_name]
        tgt["total"] += src["total"]
        tgt["meses_set"] |= src["meses_set"]
        for k, v in src["por_semana"].items():
            tgt["por_semana"][k] += v
        for k, v in src["por_mes"].items():
            tgt["por_mes"][k] += v
        if src["primeira_sem"] and (tgt["primeira_sem"] is None or src["primeira_sem"] < tgt["primeira_sem"]):
            tgt["primeira_sem"] = src["primeira_sem"]
        if src["ultima_sem"] and (tgt["ultima_sem"] is None or src["ultima_sem"] > tgt["ultima_sem"]):
            tgt["ultima_sem"] = src["ultima_sem"]
        del envio_dict[source_name]
    # Merge pagos
    if source_name in pagos_dict:
        src = pagos_dict[source_name]
        tgt = pagos_dict[target_name]
        tgt["total"] += src["total"]
        tgt["compra"] += src["compra"]
        tgt["liq"] += src["liq"]
        for k, v in src["por_semana"].items():
            tgt["por_semana"][k] += v
        if src["primeira_sem"] and (tgt["primeira_sem"] is None or src["primeira_sem"] < tgt["primeira_sem"]):
            tgt["primeira_sem"] = src["primeira_sem"]
        if src["ultimo_pago"] > tgt["ultimo_pago"]:
            tgt["ultimo_pago"] = src["ultimo_pago"]
        del pagos_dict[source_name]

print("Merging duplicados...")
for source, target in MERGE_MAP.items():
    merge_into(source, target, envio, pagos)
    print(f"  {source} -> {target}")

def yw_to_iso(year, week):
    """Approximate ISO date from year+week (Monday of that week)"""
    try:
        from datetime import date
        d = date.fromisocalendar(year, max(1, min(week, 52)), 1)
        return d.isoformat()
    except Exception:
        return None

# ============================================================
# 2. CALCULAR METRICAS POR PARCEIRO
# ============================================================
print("Calculando metricas...")

todos_nomes = set(list(envio.keys()) + list(pagos.keys()))
resultado = []

for nome in todos_nomes:
    e = envio[nome]
    pg = pagos[nome]

    tl = e["total"]
    meses_ativos = len(e["meses_set"])
    tp = pg["total"]
    vc = pg["compra"]
    vl = pg["liq"]
    ticket = vc / tp if tp > 0 else 0
    taxa_conv = tp / tl * 100 if tl > 0 else 0

    # Leads por janela
    s4 = sum(e["por_semana"].get((ano_atual, s), 0) for s in range(sem_atual - 3, sem_atual + 1))
    s4a = sum(e["por_semana"].get((ano_atual, s), 0) for s in range(sem_atual - 7, sem_atual - 3))
    s8 = s4 + s4a
    s12 = s8 + sum(e["por_semana"].get((ano_atual, s), 0) for s in range(sem_atual - 11, sem_atual - 7))

    # Semanas ativas nas ultimas 4
    semanas_ativas_4 = sum(1 for s in range(sem_atual - 3, sem_atual + 1) if e["por_semana"].get((ano_atual, s), 0) > 0)

    # Media semanal nas semanas ativas (ultimas 4)
    leads_em_semanas_ativas = [e["por_semana"].get((ano_atual, s), 0) for s in range(sem_atual - 3, sem_atual + 1) if e["por_semana"].get((ano_atual, s), 0) > 0]
    media_sem_ativa = sum(leads_em_semanas_ativas) / len(leads_em_semanas_ativas) if leads_em_semanas_ativas else 0

    # Tendencia
    tend = ((s4 - s4a) / s4a * 100) if s4a > 0 else (100 if s4 > 0 else (-100 if tl > 0 else 0))

    # Semanas parado
    ultima_sem_envio = e["ultima_sem"]
    semanas_parado = 0
    if ultima_sem_envio:
        if ultima_sem_envio[0] == ano_atual:
            semanas_parado = max(0, sem_atual - ultima_sem_envio[1])
        else:
            semanas_parado = sem_atual + (52 - ultima_sem_envio[1])

    # Primeira semana (para detectar "Novo")
    primeira_sem = e["primeira_sem"]
    semanas_desde_primeiro = 0
    if primeira_sem:
        if primeira_sem[0] == ano_atual:
            semanas_desde_primeiro = sem_atual - primeira_sem[1]
        else:
            semanas_desde_primeiro = sem_atual + (52 - primeira_sem[1])

    # Sparkline (ultimas 12 semanas)
    levels = ['\u2581','\u2582','\u2583','\u2584','\u2585','\u2586','\u2587','\u2588']
    spark_chars = []
    for s in range(sem_atual - 11, sem_atual + 1):
        cnt = e["por_semana"].get((ano_atual, s), 0)
        if cnt == 0: spark_chars.append(levels[0])
        elif cnt <= 2: spark_chars.append(levels[1])
        elif cnt <= 5: spark_chars.append(levels[2])
        elif cnt <= 10: spark_chars.append(levels[3])
        elif cnt <= 20: spark_chars.append(levels[4])
        elif cnt <= 40: spark_chars.append(levels[5])
        elif cnt <= 80: spark_chars.append(levels[6])
        else: spark_chars.append(levels[7])
    spark = " ".join(spark_chars)

    # Melhor mes
    melhor_mes_vol = 0
    melhor_mes_key = None
    for (a, m), vol in e["por_mes"].items():
        if vol > melhor_mes_vol:
            melhor_mes_vol = vol
            melhor_mes_key = (a, m)

    # Media mensal
    meses_com_dados = [v for v in e["por_mes"].values() if v > 0]
    media_mensal = sum(meses_com_dados) / len(meses_com_dados) if meses_com_dados else 0

    # ============================================================
    # FLAGS ESPECIAIS
    # ============================================================
    is_fantasma = tl == 0 and tp > 0
    is_novo = semanas_desde_primeiro <= 4 and tl > 0 and not is_fantasma

    # Ressuscitado: teve gap >= 8 semanas e voltou nas ultimas 4
    is_em_recuperacao = False
    if s4 > 0 and not is_novo:
        # Verificar se houve gap de 8+ semanas antes da retomada
        gap_antes = 0
        for s in range(sem_atual - 4, sem_atual - 20, -1):
            if e["por_semana"].get((ano_atual, s), 0) == 0:
                gap_antes += 1
            else:
                break
        if gap_antes >= 8:
            is_em_recuperacao = True

    # Sazonal: envia em rajadas (alta concentracao em poucas semanas)
    is_sazonal = False
    if tl >= 10 and meses_ativos >= 2:
        semanas_12 = [e["por_semana"].get((ano_atual, s), 0) for s in range(sem_atual - 11, sem_atual + 1)]
        semanas_com_envio = sum(1 for v in semanas_12 if v > 0)
        if semanas_com_envio > 0 and semanas_com_envio <= 6:
            media_quando_envia = sum(semanas_12) / semanas_com_envio
            if media_quando_envia >= 3:
                is_sazonal = True

    # ============================================================
    # CLASSIFICACAO DE ENVIO
    # ============================================================
    if is_novo:
        envio_class = "Novo"
    elif s4 == 0:
        envio_class = "Sem envio"
    elif s4 >= 6 and meses_ativos >= 3:
        envio_class = "Consistente"
    elif s4 >= 3 and meses_ativos >= 2:
        envio_class = "Regular"
    elif s4 >= 1 and (media_sem_ativa >= 2 or meses_ativos >= 2):
        envio_class = "Regular"
    else:
        envio_class = "Esporadico"

    # ============================================================
    # ISP v3 - Nao penaliza sazonalidade, nao premia frequencia vazia
    # ============================================================
    if is_fantasma:
        isp = -1
        saude = "N/A"
    else:
        # RECENCIA (25 pts) - baseado em semanas parado
        if semanas_parado <= 4: isp_rec = 25
        elif semanas_parado <= 8: isp_rec = 18
        elif semanas_parado <= 12: isp_rec = 8
        else: isp_rec = 0

        # PRODUCAO (25 pts) - baseado em pagos + taxa conversao
        if tp >= 6: isp_prod = 25
        elif tp >= 3: isp_prod = 20
        elif tp == 2: isp_prod = 15
        elif tp == 1: isp_prod = 10
        else: isp_prod = 0
        # Bonus conversao (quem converte bem merece mais)
        if tl > 0 and tp > 0 and taxa_conv > 15: isp_prod = min(25, isp_prod + 3)

        # VOLUME AJUSTADO (20 pts) - media semanal nas semanas ativas, nao frequencia bruta
        if media_sem_ativa >= 10: isp_vol = 20
        elif media_sem_ativa >= 5: isp_vol = 16
        elif media_sem_ativa >= 3: isp_vol = 12
        elif media_sem_ativa >= 1.5: isp_vol = 8
        elif s4 >= 1: isp_vol = 4
        else: isp_vol = 0
        # Parceiro sazonal com bom volume total nao perde pontos
        if is_sazonal and s12 >= 10: isp_vol = max(isp_vol, 14)

        # CONSISTENCIA (15 pts) - meses ativos (historico)
        if meses_ativos >= 7: isp_cons = 15
        elif meses_ativos >= 4: isp_cons = 12
        elif meses_ativos >= 3: isp_cons = 9
        elif meses_ativos >= 2: isp_cons = 5
        elif meses_ativos == 1: isp_cons = 2
        else: isp_cons = 0

        # TENDENCIA (10 pts)
        if tend > 20: isp_tend = 10
        elif tend >= -20: isp_tend = 7
        elif tend >= -50: isp_tend = 3
        else: isp_tend = 0
        # Ressuscitado ganha bonus de tendencia
        if is_em_recuperacao: isp_tend = max(isp_tend, 7)

        # VALOR (5 pts) - ticket / valor acumulado
        if vc >= 2e6: isp_val = 5
        elif vc >= 500e3: isp_val = 4
        elif vc >= 100e3: isp_val = 3
        elif vc > 0: isp_val = 2
        else: isp_val = 0

        isp = isp_rec + isp_prod + isp_vol + isp_cons + isp_tend + isp_val

        # SAUDE baseada no ISP
        if isp >= 80: saude = "Excelente"
        elif isp >= 60: saude = "Bom"
        elif isp >= 40: saude = "Regular"
        elif isp >= 20: saude = "Ruim"
        else: saude = "Péssimo"

        # Override: Em Recuperação (flag, não muda ISP)
        if is_em_recuperacao and saude in ("Ruim", "Péssimo"):
            saude = "Em Recuperação"

    # ============================================================
    # CATEGORIA (7): Diamante, Ouro, Prata, Bronze, Em Recuperacao, Inativo, Fantasma
    # ============================================================
    # Media semanal ultimas 8 semanas
    avg_8sem = s8 / 8.0 if s8 > 0 else 0

    ativo8 = s8 > 0  # enviou qualquer coisa nas ultimas 8 semanas

    # REGRA 1: Fantasma (compra fora da esteira)
    if is_fantasma:
        categoria = "Fantasma"
    # REGRA 2: Inativo = parado 8+ semanas, FIM. Nenhuma outra regra se aplica.
    elif not ativo8 and not is_em_recuperacao:
        categoria = "Inativo"
    # REGRA 3: Em Recuperação (voltou apos gap)
    elif is_em_recuperacao:
        categoria = "Em Recuperação"
    # REGRA 4: Diamante (ticket >= 1M OU pagos+volume+historico)
    elif ticket >= 1e6 and meses_ativos >= 2:
        categoria = "Diamante"
    elif (tp >= 3 or ticket >= 5e5) and avg_8sem >= 3 and meses_ativos >= 4:
        categoria = "Diamante"
    # REGRA 5: Ouro (tem pagos + ativo + historico)
    elif tp >= 1 and meses_ativos >= 2:
        categoria = "Ouro"
    # REGRA 6: Prata (ativo, 3+ leads)
    elif tl >= 3:
        categoria = "Prata"
    # REGRA 7: Bronze (ativo, pouco volume ou novo)
    else:
        categoria = "Bronze"

    # ============================================================
    # DIAGNOSTICO
    # ============================================================
    diag = []
    nome_mes_map = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

    if s4 > 0:
        diag.append(f"Ativo: {s4} leads em {semanas_ativas_4} sem (media {media_sem_ativa:.1f}/sem ativa)")
    elif ultima_sem_envio:
        diag.append(f"Parado ha {semanas_parado} sem. Ultimo envio: S{ultima_sem_envio[1]}/{ultima_sem_envio[0]}")
    elif not is_fantasma:
        diag.append("Sem historico de envio")

    if s4a > 0 and s4 > 0:
        if tend > 20: diag.append(f"Tend: +{tend:.0f}% (de {s4a} para {s4})")
        elif tend >= -20: diag.append(f"Tend: estavel ({tend:+.0f}%)")
        else: diag.append(f"Tend: queda {tend:.0f}% (de {s4a} para {s4})")
    elif s4a > 0 and s4 == 0:
        diag.append(f"Parou. Tinha {s4a} leads no bloco anterior")

    if melhor_mes_key and media_mensal > 0:
        pico = f"{nome_mes_map.get(melhor_mes_key[1],'?')}/{melhor_mes_key[0]}"
        diag.append(f"Hist: {tl}L em {meses_ativos}m. Media {media_mensal:.1f}/m. Pico: {melhor_mes_vol} em {pico}")

    if tp > 0:
        diag.append(f"Pagos: {tp} (R$ {vc:,.0f}). Ticket: R$ {ticket:,.0f}. Conv: {taxa_conv:.1f}%")

    flags_txt = []
    if is_sazonal: flags_txt.append("SAZONAL")
    if is_em_recuperacao: flags_txt.append("EM RECUPERACAO")
    if is_novo: flags_txt.append("NOVO")
    if is_fantasma: flags_txt.append("FANTASMA")
    if flags_txt:
        diag.append("Flags: " + ", ".join(flags_txt))

    diagnostico = " | ".join(diag)

    # Acao
    if categoria == "Inativo" and tp >= 3:
        acao = f"REATIVACAO URGENTE. {tp} pagos, R$ {vc:,.0f}. Parado ha {semanas_parado} sem."
    elif categoria == "Inativo" and tp > 0:
        acao = f"Reativar. {tp} pago(s). Verificar causa."
    elif categoria == "Diamante" and tend < -30:
        acao = f"ACAO IMEDIATA. {categoria} em queda {tend:.0f}%. Contato 48h."
    elif categoria == "Em Recuperacao":
        acao = f"Monitorar retomada. Voltou apos gap. Manter contato proximo."
    elif categoria == "Bronze" and is_novo:
        acao = f"Boas-vindas. Parceiro novo na base. Acompanhar primeiras semanas."
    elif categoria == "Bronze" and tl >= 20 and tp == 0:
        acao = f"Auditar. {tl} leads, zero compras. Revisar qualidade."
    elif categoria == "Fantasma":
        acao = "Observacao. Entender canal."
    else:
        acao = "Monitorar."

    # Prioridade
    if categoria == "Diamante" and (tend < -30 or s4 == 0) and tp > 0: prior = "CRITICA"
    elif categoria == "Diamante" and tend < -20: prior = "ALTA"
    elif categoria == "Prata" and tend < -30: prior = "ALTA"
    elif categoria == "Bronze" and tl >= 20: prior = "MEDIA"
    elif categoria == "Em Recuperacao": prior = "MEDIA"
    elif categoria == "Bronze" and is_novo: prior = "MEDIA"
    elif categoria == "Fantasma": prior = "OBSERVACAO"
    else: prior = "BAIXA"

    prazo = {"CRITICA": "48h", "ALTA": "1 semana", "MEDIA": "2 semanas"}.get(prior, "Mensal")

    # Build semanas dict: "YYYY-WW" -> count
    semanas_dict = {}
    for (a, s), cnt in e["por_semana"].items():
        semanas_dict[f"{a}-{s:02d}"] = cnt
    # Build pagos_semanas dict: "YYYY-WW" -> count
    pagos_semanas_dict = {}
    for (a, s), cnt in pg["por_semana"].items():
        pagos_semanas_dict[f"{a}-{s:02d}"] = cnt

    # Date fields
    data_primeiro_envio = yw_to_iso(*primeira_sem) if primeira_sem else None
    data_ultimo_envio = yw_to_iso(*e["ultima_sem"]) if e["ultima_sem"] else None
    pg_primeira = pg.get("primeira_sem")
    data_primeiro_pago = yw_to_iso(*pg_primeira) if pg_primeira and pg_primeira != (0, 0) else None
    pg_ultimo = pg["ultimo_pago"]
    data_ultimo_pago = yw_to_iso(*pg_ultimo) if pg_ultimo != (0, 0) else None

    # Determine UF: prioridade BD_Parceiros > BD_Pagos
    parceiro_uf = parceiros_uf.get(nome, "")
    if not parceiro_uf:
        pg_ufs = pg.get("ufs", {})
        if pg_ufs:
            parceiro_uf = max(pg_ufs, key=pg_ufs.get)

    # Determine regional (from envio col 24 if available)
    envio_regs = e.get("regionais", {})
    parceiro_regional = ""
    if envio_regs:
        parceiro_regional = max(envio_regs, key=envio_regs.get)

    resultado.append({
        "nome": nome, "cat": categoria, "saude": saude, "isp": isp,
        "uf": parceiro_uf, "regional_envio": parceiro_regional,
        "leads": tl, "sem4": s4, "sem4a": s4a, "sem8": s8, "sem12": s12,
        "pagos": tp, "compra": round(vc), "liq": round(vl), "ticket": round(ticket),
        "tend": round(tend, 1), "taxa_conv": round(taxa_conv, 1),
        "meses": meses_ativos, "media_mensal": round(media_mensal, 1),
        "media_sem_ativa": round(media_sem_ativa, 1),
        "semanas_parado": semanas_parado,
        "envio_class": envio_class,
        "is_sazonal": is_sazonal, "is_em_recuperacao": is_em_recuperacao,
        "is_novo": is_novo, "is_fantasma": is_fantasma,
        "diagnostico": diagnostico, "acao": acao,
        "prior": prior, "prazo": prazo, "spark": spark,
        # Full weekly data for dynamic filtering
        "semanas": semanas_dict,
        "pagos_semanas": pagos_semanas_dict,
        "data_primeiro_envio": data_primeiro_envio,
        "data_ultimo_envio": data_ultimo_envio,
        "data_primeiro_pago": data_primeiro_pago,
        "data_ultimo_pago": data_ultimo_pago,
        # ISP componentes (para auditoria)
        "isp_rec": isp_rec if not is_fantasma else 0,
        "isp_prod": isp_prod if not is_fantasma else 0,
        "isp_vol": isp_vol if not is_fantasma else 0,
        "isp_cons": isp_cons if not is_fantasma else 0,
        "isp_tend": isp_tend if not is_fantasma else 0,
        "isp_val": isp_val if not is_fantasma else 0,
        # Datas para filtro (semana/ano do primeiro envio e ultimo pago)
        "primeira_sem": list(primeira_sem) if primeira_sem else None,
        "ultima_compra_sem": list(pg["ultimo_pago"]) if pg["ultimo_pago"] != (0,0) else None,
    })

# Stats
from collections import Counter
print(f"\nTotal: {len(resultado)}")
print("\nCategorias:")
for c, n in Counter(p["cat"] for p in resultado).most_common():
    leads = sum(p["leads"] for p in resultado if p["cat"] == c)
    pagos = sum(p["pagos"] for p in resultado if p["cat"] == c)
    compra = sum(p["compra"] for p in resultado if p["cat"] == c)
    print(f"  {c:20s}: {n:4d} | {leads:5d}L | {pagos:4d}P | R${compra:>12,}")

print("\nSaude:")
for s, n in Counter(p["saude"] for p in resultado).most_common():
    print(f"  {s:16s}: {n}")

print("\nEnvio:")
for e, n in Counter(p["envio_class"] for p in resultado).most_common():
    print(f"  {e:16s}: {n}")

print("\nFlags:")
print(f"  Sazonais: {sum(1 for p in resultado if p['is_sazonal'])}")
print(f"  Em Recuperacao: {sum(1 for p in resultado if p['is_em_recuperacao'])}")
print(f"  Novos: {sum(1 for p in resultado if p['is_novo'])}")
print(f"  Fantasmas: {sum(1 for p in resultado if p['is_fantasma'])}")

# Salvar JSON
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print(f"\nJSON salvo: {len(resultado)} parceiros")

pythoncom.CoUninitialize()
print("Concluido!")
