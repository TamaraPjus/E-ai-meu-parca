"""
=============================================================================
  Agente "e aí, meu parça"
  ---------------------
  Automatiza a solicitação do relatório semanal de parceiros na esteira PJUS,
  aguarda o recebimento por e-mail no Outlook, salva o Excel na pasta correta,
  alimenta a planilha de análise (BD_EnvioParceiros) e notifica ao final.
=============================================================================
"""

import os
import sys
import time
import logging
import shutil
import glob as glob_mod
from datetime import datetime, timedelta
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import win32com.client
import tkinter as tk
from tkinter import messagebox

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
URL_ESTEIRA = "https://esteira.pjus.com.br/home/index?esteiraId=6"

# Arquivo base (fonte de verdade) — sempre ler daqui para calcular datas
ARQUIVO_BASE = Path(
    r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA"
    r"\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca"
    r"\Analise Parcerias.xlsx"
)

PASTA_BASE_PARCERIAS = Path(
    r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA"
    r"\USwork - INTELIGENCIA DE MERCADO\Atividades\09. Parcerias"
)

PASTA_BASE_ANALISE = Path(
    r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA"
    r"\USwork - INTELIGENCIA DE MERCADO\Atividades\07. Analises e Estudos\05. Parcerias"
)

PASTA_LOGS = Path(
    r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA"
    r"\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca\logs"
)

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

TEMPO_ESPERA_EMAIL_SEG = 5 * 60  # 5 minutos
MAX_TENTATIVAS_EMAIL = 6         # checa a cada 1 min por mais 5 min apos espera inicial

# Colunas com formula em BD_EnvioParceiros (indice 1-based)
# Col 19: Mes      =MONTH(Tabela1[[#This Row],[DataCriacao]])
# Col 20: Semana   =WEEKNUM(Tabela1[[#This Row],[DataCriacao]])
# Col 21: Varejo   =IF(Tabela1[[#This Row],[ValorBruto]]>=10000000,"não","sim")
# Col 22: Ano      =YEAR(Tabela1[[#This Row],[DataCriacao]])
# Col 23: Motivo reprovação2  =XLOOKUP(...)
# Col 25: Nome ajustado       =VLOOKUP(...)
COLUNAS_FORMULA_ENVIO = [19, 20, 21, 22, 23, 25]

# BD_Pagos: colunas com formula (1-based no destino)
# Col 57: Ano           =YEAR(Tabela4[[#This Row],[Comprado em]])
# Col 58: Semana        =WEEKNUM(Tabela4[[#This Row],[Comprado em]])
# Col 59: Semana - Ano  =CONCAT(Semana,"-",Ano)
# Col 60: Nome Ajustado =VLOOKUP(Intermediário,DePara!I:K,3,0)
COLUNAS_FORMULA_PAGOS = [57, 58, 59, 60]

# Mapeamento: col_destino_BD_Pagos -> col_fonte_BS_Producao (1-based)
# Colunas sem correspondência ficam vazias
MAPA_PAGOS = {
    1: 2,    # Id Processos <- idprocessos
    2: 3,    # Estado Processo <- estadoprocesso
    3: 4,    # Nome Beneficiário <- nomebeneficiário
    4: 5,    # Valor de Face <- valordeface
    5: 6,    # Esfera <- esfera
    6: 7,    # Hunter <- hunter
    7: 8,    # Squad Comercial <- squadcomercial
    8: 9,    # Gestor <- gestor
    9: 10,   # Categoria <- categoria
    10: 11,  # Líq. PJUS <- líq.pjus
    11: 12,  # Líq. Ofício <- líq.ofício
    12: 13,  # Compra p/ <- compra
    13: 14,  # % Com,PJUS <- %com.pjus
    14: 15,  # R$ Com.PJUS <- r$com.pjus
    15: 16,  # Comprado em <- compradoem
    16: 17,  # Intermediário <- intermediário
    17: 18,  # Valor Intermediario <- valorintermediario
    18: 19,  # Desc Operação <- descoperação
    19: 20,  # Cod. Operação <- cod.operação
    20: 21,  # vencimento <- vencimento
    21: 22,  # N Prazo <- nprazo
    22: 23,  # Valor Presente <- valorpresente
    23: 24,  # % de Acordo <- %deacordo
    24: 25,  # Entrada do processo na base <- entradaprocessonabase
    28: 26,  # CPF <- cpf_cnpj
    29: 27,  # Num_Processo <- numerodoprocesso
    31: 28,  # Tribunal <- tribunal
    32: 29,  # Responsavel Originação <- responsavel_originação
    33: 32,  # Pri_ent_Est <- Pri_ent_Est
    41: 33,  # Responsavel Originação + Parceiros <- col 33
    42: 31,  # Liquido Oficio Acordo Ajustado <- liquido_a_receber_oficio
    43: 30,  # Flag Raspagem <- flag raspagem
    44: 36,  # Data Envio ao Onboarding <- col 36
    45: 37,  # Originação <- col 37
    39: 34,  # Data Envio ao Onboarding* <- col 34
    40: 35,  # Regional <- col 35
    46: 38,  # Regional + GG <- col 38
    47: 39,  # SLA <- col 39
    48: 40,  # Liq. Ofício_Conversão <- col 40
    49: 42,  # Ente | Tribunal <- col 42
    50: 43,  # Semana Onboarding <- col 43
    51: 47,  # Faixa VLR <- col 47
    53: 48,  # Semana material <- col 48
    54: 49,  # SLA Pagamento <- col 49
    55: 50,  # 4MTI <- col 50
}

# Caminho do arquivo de Acompanhamento_Metas (fonte de pagos)
ARQUIVO_PAGOS_FONTE = Path(
    r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA"
    r"\USwork - BD_Excel\20260119_Acompanhamento_Metas_Semana_Env_Est_e_Prod_02.xlsx"
)

# Data minima para filtro de pagos
DATA_MINIMA_PAGOS = datetime(2025, 1, 1)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def configurar_logging():
    PASTA_LOGS.mkdir(parents=True, exist_ok=True)
    log_file = PASTA_LOGS / "e_ai_meu_parca.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("e_ai_meu_parca")


# ---------------------------------------------------------------------------
# Calculo do periodo — baseado na ultima data do arquivo base
# ---------------------------------------------------------------------------
def obter_ultima_data_arquivo_base(logger):
    """Abre o arquivo base (BD_EnvioParceiros), identifica a data mais recente
    na coluna DataCriacao e retorna como datetime.date.

    A coluna DataCriacao é tipicamente a coluna 1 ou a coluna que contém datas.
    Vamos verificar a coluna 1 (que no BD_EnvioParceiros costuma ser DataCriacao).
    """
    import pythoncom
    pythoncom.CoInitialize()

    excel = None
    try:
        if not ARQUIVO_BASE.exists():
            logger.error(f"Arquivo base nao encontrado: {ARQUIVO_BASE}")
            return None

        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        logger.info(f"Abrindo arquivo base: {ARQUIVO_BASE.name}")
        wb = excel.Workbooks.Open(str(ARQUIVO_BASE), CorruptLoad=1)
        ws = wb.Worksheets("BD_EnvioParceiros")

        ultima_linha = ws.Cells(ws.Rows.Count, 1).End(-4162).Row
        logger.info(f"BD_EnvioParceiros no arquivo base: {ultima_linha} linhas")

        # Encontrar a data mais recente na coluna 6 (DataCriacao)
        # Percorrer do fim para o inicio para ser mais rapido
        data_mais_recente = None
        for row in range(ultima_linha, 1, -1):
            val = ws.Cells(row, 6).Value
            if val is None:
                continue
            try:
                if hasattr(val, 'year'):
                    dt = datetime(val.year, val.month, val.day).date()
                else:
                    dt = datetime.strptime(str(val)[:10], "%Y-%m-%d").date()

                if data_mais_recente is None or dt > data_mais_recente:
                    data_mais_recente = dt
            except Exception:
                continue

        wb.Close(False)
        logger.info(f"Data mais recente no arquivo base: {data_mais_recente}")
        return data_mais_recente

    except Exception as e:
        logger.error(f"Erro ao ler arquivo base: {e}", exc_info=True)
        return None
    finally:
        if excel:
            try:
                excel.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def calcular_periodo_incremental(logger):
    """Calcula o periodo incremental baseado no arquivo base.

    Logica:
    - Abre o arquivo base e identifica a ultima data processada
    - Data inicio = dia seguinte a ultima data encontrada
    - Data fim = ontem
    - Se nao ha gap (ultima data >= ontem), retorna None, None

    Retorna: (data_inicio, data_fim) como datetime.date ou (None, None)
    """
    ultima_data = obter_ultima_data_arquivo_base(logger)

    if ultima_data is None:
        logger.error("Nao foi possivel determinar a ultima data do arquivo base.")
        return None, None

    ontem = (datetime.now() - timedelta(days=1)).date()
    data_inicio = ultima_data + timedelta(days=1)
    data_fim = ontem

    if data_inicio > data_fim:
        logger.info(
            f"Nenhum periodo novo a processar. "
            f"Ultima data no arquivo: {ultima_data.strftime('%d/%m/%Y')}, "
            f"ontem: {ontem.strftime('%d/%m/%Y')}"
        )
        return None, None

    logger.info(
        f"Periodo incremental calculado: "
        f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')} "
        f"(base ate {ultima_data.strftime('%d/%m/%Y')})"
    )
    return data_inicio, data_fim


def calcular_semana_anterior(data_referencia=None):
    """LEGADO — Mantido para compatibilidade.
    Retorna (segunda, domingo) da semana anterior completa.
    """
    hoje = data_referencia or datetime.now().date()
    segunda_corrente = hoje - timedelta(days=hoje.weekday())
    domingo = segunda_corrente - timedelta(days=1)
    segunda = domingo - timedelta(days=6)
    return segunda, domingo


# ---------------------------------------------------------------------------
# Selenium — solicitar relatorio na esteira
# ---------------------------------------------------------------------------
PERFIL_AGENTE = Path.home() / ".e_ai_meu_parca_chrome"


def iniciar_driver(logger):
    """Inicia Chrome com perfil dedicado do agente.

    Na primeira execução, o perfil estará vazio e a esteira vai pedir login.
    Faça login manualmente UMA VEZ. A sessão fica salva e nas próximas
    execuções o agente já entra logado automaticamente.
    """
    logger.info("Iniciando Chrome com perfil dedicado do agente...")

    PERFIL_AGENTE.mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument(f"--user-data-dir={PERFIL_AGENTE}")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    return driver


def solicitar_relatorio(driver, data_inicio, data_fim, logger):
    """Acessa a esteira, preenche periodo e solicita envio por e-mail."""

    logger.info(f"Acessando esteira: {URL_ESTEIRA}")
    driver.get(URL_ESTEIRA)
    wait = WebDriverWait(driver, 90)

    logger.info("Aguardando pagina carregar (15s)...")
    time.sleep(15)
    logger.info("Aguardando botao 'Enviar relatorio por e-mail'...")

    btn_relatorio = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Enviar relat')]/..")
        )
    )
    btn_relatorio.click()
    logger.info("Botao de envio clicado.")
    time.sleep(2)

    fmt_input = "%Y-%m-%d"

    campo_inicio = wait.until(
        EC.presence_of_element_located((By.ID, "dataInicioRelatorioParceiro"))
    )
    campo_inicio.clear()
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
        campo_inicio,
        data_inicio.strftime(fmt_input),
    )
    logger.info(f"Data inicio preenchida: {data_inicio.strftime('%d/%m/%Y')}")
    time.sleep(1)

    campo_fim = wait.until(
        EC.presence_of_element_located((By.ID, "dataFimRelatorioParceiro"))
    )
    campo_fim.clear()
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
        campo_fim,
        data_fim.strftime(fmt_input),
    )
    logger.info(f"Data fim preenchida: {data_fim.strftime('%d/%m/%Y')}")
    time.sleep(1)

    btn_ok = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#form-relatorio-esteira-parceiro button[type='submit']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", btn_ok)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", btn_ok)
    logger.info("Botao OK clicado. Relatorio solicitado com sucesso.")
    time.sleep(3)


# ---------------------------------------------------------------------------
# Outlook — buscar e-mail e salvar anexo
# ---------------------------------------------------------------------------
def buscar_email_outlook(logger):
    """Busca e-mail recente com assunto 'Parceiro' e retorna o anexo Excel."""

    import pythoncom
    pythoncom.CoInitialize()

    logger.info(f"Aguardando {TEMPO_ESPERA_EMAIL_SEG // 60} minutos para o e-mail chegar...")
    time.sleep(TEMPO_ESPERA_EMAIL_SEG)

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox

    for tentativa in range(1, MAX_TENTATIVAS_EMAIL + 1):
        logger.info(f"Tentativa {tentativa}/{MAX_TENTATIVAS_EMAIL} de localizar e-mail...")

        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        limite = datetime.now() - timedelta(hours=2)

        for msg in messages:
            try:
                recebido = msg.ReceivedTime
                recebido_dt = datetime(
                    recebido.year, recebido.month, recebido.day,
                    recebido.hour, recebido.minute, recebido.second,
                )
                if recebido_dt < limite:
                    break

                assunto = msg.Subject or ""
                if "parceiro" not in assunto.lower():
                    continue

                logger.info(f"E-mail encontrado: '{assunto}' recebido em {recebido_dt}")

                for i in range(1, msg.Attachments.Count + 1):
                    anexo = msg.Attachments.Item(i)
                    nome_anexo = anexo.FileName.lower()
                    if "relatorio" in nome_anexo and nome_anexo.endswith((".xlsx", ".xls")):
                        logger.info(f"Anexo encontrado: {anexo.FileName}")
                        return anexo

                logger.warning("E-mail encontrado, mas sem anexo 'relatorio' Excel.")
            except Exception:
                continue

        if tentativa < MAX_TENTATIVAS_EMAIL:
            logger.info("E-mail nao encontrado ainda. Aguardando 60 segundos...")
            time.sleep(60)

    return None


def salvar_anexo(anexo, data_inicio, data_fim, logger):
    """Salva o anexo na pasta correta com o nome padronizado."""

    num_mes = data_fim.month
    nome_mes = MESES_PT[num_mes]
    pasta_mes = PASTA_BASE_PARCERIAS / f"{num_mes:02d}. {nome_mes}"
    pasta_mes.mkdir(parents=True, exist_ok=True)
    logger.info(f"Pasta destino: {pasta_mes}")

    nome_arquivo = (
        f"parceiros_{data_inicio.strftime('%d-%m')} a {data_fim.strftime('%d-%m')}.xlsx"
    )
    caminho_final = pasta_mes / nome_arquivo

    anexo.SaveAsFile(str(caminho_final))
    logger.info(f"Arquivo salvo: {caminho_final}")

    return caminho_final


# ---------------------------------------------------------------------------
# Planilha de analise — copiar, alimentar BD_EnvioParceiros
# ---------------------------------------------------------------------------
def encontrar_planilha_mais_recente(logger):
    """Encontra a planilha de analise mais recente em qualquer pasta de mes."""
    padrao = str(PASTA_BASE_ANALISE / "**" / "*_Analise Parcerias.xlsx")
    arquivos = glob_mod.glob(padrao, recursive=True)
    if not arquivos:
        logger.error("Nenhuma planilha de analise encontrada!")
        return None
    # Ordenar por nome (YYYY.MM.DD garante ordem cronologica)
    arquivos.sort()
    mais_recente = Path(arquivos[-1])
    logger.info(f"Planilha mais recente encontrada: {mais_recente.name}")
    return mais_recente


def criar_copia_semanal(planilha_origem, logger):
    """Cria copia da planilha com a data de hoje no mes correto."""
    hoje = datetime.now()
    num_mes = hoje.month
    nome_mes = MESES_PT[num_mes]
    pasta_destino = PASTA_BASE_ANALISE / f"{num_mes:02d}. {nome_mes}"
    pasta_destino.mkdir(parents=True, exist_ok=True)

    nome_novo = f"{hoje.strftime('%Y.%m.%d')}_Analise Parcerias.xlsx"
    caminho_novo = pasta_destino / nome_novo

    if caminho_novo.exists():
        logger.info(f"Planilha de hoje ja existe: {caminho_novo.name}")
        return caminho_novo

    shutil.copy2(str(planilha_origem), str(caminho_novo))
    logger.info(f"Copia criada: {caminho_novo.name}")
    return caminho_novo


def alimentar_bd_envio_parceiros(planilha_analise, relatorio_parceiros, logger):
    """Abre a planilha de analise via Excel COM, cola dados novos do relatorio
    na aba BD_EnvioParceiros, estende formulas e redimensiona a tabela."""

    import pythoncom
    pythoncom.CoInitialize()

    excel = None
    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False

        logger.info("Abrindo planilha de analise no Excel...")
        wb_analise = excel.Workbooks.Open(str(planilha_analise))
        ws_destino = wb_analise.Worksheets("BD_EnvioParceiros")

        # Encontrar ultima linha com dados na coluna A
        ultima_linha_destino = ws_destino.Cells(ws_destino.Rows.Count, 1).End(-4162).Row
        logger.info(f"BD_EnvioParceiros: ultima linha atual = {ultima_linha_destino}")

        # Abrir relatorio de parceiros
        logger.info("Abrindo relatorio de parceiros...")
        wb_relatorio = excel.Workbooks.Open(str(relatorio_parceiros))
        ws_relatorio = wb_relatorio.Worksheets(1)

        # Encontrar dimensoes do relatorio
        ultima_linha_rel = ws_relatorio.Cells(ws_relatorio.Rows.Count, 1).End(-4162).Row
        ultima_col_rel = ws_relatorio.Cells(1, ws_relatorio.Columns.Count).End(-4159).Column

        total_novos = ultima_linha_rel - 1  # exclui cabecalho
        if total_novos <= 0:
            logger.warning("Relatorio de parceiros vazio. Nada a adicionar.")
            wb_relatorio.Close(False)
            wb_analise.Close(False)
            return 0

        logger.info(f"Relatorio: {total_novos} linhas novas, {ultima_col_rel} colunas de dados")

        # Copiar apenas dados (sem cabecalho) do relatorio
        # Colunas de dados no relatorio = colunas 1 a ultima_col_rel
        # No destino, colunas de dados = 1 a 18 (as primeiras 18 sao dados)
        colunas_dados = min(ultima_col_rel, 18)

        rng_origem = ws_relatorio.Range(
            ws_relatorio.Cells(2, 1),
            ws_relatorio.Cells(ultima_linha_rel, colunas_dados)
        )

        linha_inicio_destino = ultima_linha_destino + 1
        rng_destino = ws_destino.Range(
            ws_destino.Cells(linha_inicio_destino, 1),
            ws_destino.Cells(linha_inicio_destino + total_novos - 1, colunas_dados)
        )

        # Colar valores
        rng_destino.Value = rng_origem.Value
        logger.info(f"Dados colados: linhas {linha_inicio_destino} a {linha_inicio_destino + total_novos - 1}")

        time.sleep(3)
        try:
            wb_relatorio.Close(False)
        except Exception as e:
            logger.warning(f"Erro ao fechar relatório (ignorando): {e}")

        # Aguardar Excel estabilizar antes de continuar
        logger.info("Aguardando Excel estabilizar (10s)...")
        time.sleep(10)

        # Estender formulas das colunas calculadas (com retry)
        logger.info("Estendendo formulas...")
        for col in COLUNAS_FORMULA_ENVIO:
            for tentativa in range(3):
                try:
                    celula_modelo = ws_destino.Cells(ultima_linha_destino, col)
                    if celula_modelo.HasFormula:
                        rng_formula_origem = ws_destino.Range(celula_modelo, celula_modelo)
                        rng_formula_destino = ws_destino.Range(
                            ws_destino.Cells(linha_inicio_destino, col),
                            ws_destino.Cells(linha_inicio_destino + total_novos - 1, col)
                        )
                        rng_formula_origem.Copy()
                        rng_formula_destino.PasteSpecial(-4123)  # xlPasteFormulas
                        logger.info(f"  Formula estendida na coluna {col}")
                    else:
                        logger.warning(f"  Coluna {col} nao tem formula na linha {ultima_linha_destino}")
                    break
                except Exception as e:
                    logger.warning(f"  Retry {tentativa+1}/3 coluna {col}: {e}")
                    time.sleep(5)

        try:
            excel.CutCopyMode = False
        except Exception:
            pass

        # Redimensionar tabela (Tabela1)
        nova_ultima_linha = linha_inicio_destino + total_novos - 1
        try:
            tabela = ws_destino.ListObjects("Tabela1")
            novo_ref = f"A1:Y{nova_ultima_linha}"
            tabela.Resize(ws_destino.Range(novo_ref))
            logger.info(f"Tabela1 redimensionada para {novo_ref}")
        except Exception as e:
            logger.warning(f"Erro ao redimensionar tabela: {e}")

        # Salvar (com retry)
        time.sleep(5)
        for tentativa in range(3):
            try:
                wb_analise.Save()
                logger.info("Planilha de analise salva com sucesso!")
                break
            except Exception as e:
                logger.warning(f"Retry save {tentativa+1}/3: {e}")
                time.sleep(5)

        time.sleep(3)
        try:
            wb_analise.Close(False)
        except Exception as e:
            logger.warning(f"Erro ao fechar planilha (ignorando): {e}")

        return total_novos

    except Exception as e:
        logger.error(f"Erro ao alimentar BD_EnvioParceiros: {e}", exc_info=True)
        raise
    finally:
        if excel:
            try:
                excel.ScreenUpdating = True
                excel.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def atualizar_depara(planilha_analise, logger):
    """Verifica parceiros novos que deram erro no VLOOKUP (col 25 = erro COM)
    e adiciona automaticamente na aba DePara para normalizar nomes.

    Lógica:
    - Percorre BD_EnvioParceiros col 25 buscando valores numéricos negativos (erro COM)
    - Para cada erro, pega o nome original (col 1) e limpa prefixo CPF/CNPJ
    - Adiciona na aba DePara: col 9 = nome original, col 10 = nome limpo, col 11 = nome limpo
    """
    import re
    import pythoncom
    pythoncom.CoInitialize()

    excel = None
    novos = 0
    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        wb = excel.Workbooks.Open(str(planilha_analise), CorruptLoad=1)
        ws_envio = wb.Worksheets("BD_EnvioParceiros")
        ws_depara = wb.Worksheets("DePara")

        ult_envio = ws_envio.Cells(ws_envio.Rows.Count, 1).End(-4162).Row
        ult_depara = ws_depara.Cells(ws_depara.Rows.Count, 9).End(-4162).Row

        # Coletar nomes existentes no DePara (col 9) para nao duplicar
        nomes_existentes = set()
        for r in range(2, ult_depara + 1):
            v = ws_depara.Cells(r, 9).Value
            if v:
                nomes_existentes.add(str(v).strip().upper())

        logger.info(f"DePara: {len(nomes_existentes)} nomes existentes")

        # Percorrer BD_EnvioParceiros buscando erros na col 25
        nomes_novos = {}  # {nome_original: nome_limpo}
        for r in range(2, ult_envio + 1):
            val_25 = ws_envio.Cells(r, 25).Value
            if val_25 is None:
                continue
            # Erro COM aparece como numero negativo grande
            try:
                num = float(val_25)
                if num < -1000000:
                    # É erro — pegar nome original
                    nome_orig = ws_envio.Cells(r, 1).Value
                    if nome_orig:
                        nome_orig = str(nome_orig).strip()
                        if nome_orig.upper() not in nomes_existentes and nome_orig not in nomes_novos:
                            # Limpar prefixo CPF/CNPJ
                            nome_limpo = re.sub(r'^\d[\d.]+\s+', '', nome_orig).strip()
                            if not nome_limpo:
                                nome_limpo = nome_orig
                            nomes_novos[nome_orig] = nome_limpo
            except (ValueError, TypeError):
                pass

        if not nomes_novos:
            logger.info("DePara: nenhum nome novo a adicionar")
            wb.Close(False)
            return 0

        # Adicionar na aba DePara
        logger.info(f"DePara: adicionando {len(nomes_novos)} nomes novos")
        prox_linha = ult_depara + 1
        for nome_orig, nome_limpo in nomes_novos.items():
            ws_depara.Cells(prox_linha, 9).Value = nome_orig
            ws_depara.Cells(prox_linha, 10).Value = nome_limpo
            ws_depara.Cells(prox_linha, 11).Value = nome_limpo
            logger.info(f"  + {nome_orig[:40]} → {nome_limpo[:40]}")
            prox_linha += 1
            novos += 1

        # Forcar recalculo para que os VLOOKUPs peguem os novos nomes
        time.sleep(3)
        wb.Application.CalculateFull()
        time.sleep(5)

        wb.Save()
        logger.info(f"DePara atualizado: +{novos} nomes. Recalculo feito.")
        wb.Close(False)

        return novos

    except Exception as e:
        logger.error(f"Erro ao atualizar DePara: {e}", exc_info=True)
        return 0
    finally:
        if excel:
            try:
                excel.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def alimentar_bd_pagos(planilha_analise, logger):
    """Abre a planilha de analise via Excel COM, lê dados de BS_Produção do arquivo
    de Acompanhamento_Metas, filtra por Comprado em >= 01/01/2025, identifica registros
    novos (por Id Processos) e cola na aba BD_Pagos."""

    if not ARQUIVO_PAGOS_FONTE.exists():
        logger.warning(f"Arquivo de pagos nao encontrado: {ARQUIVO_PAGOS_FONTE}")
        return 0

    import pythoncom
    pythoncom.CoInitialize()

    excel = None
    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False

        # Abrir planilha de analise
        logger.info("Abrindo planilha de analise para BD_Pagos...")
        wb_analise = excel.Workbooks.Open(str(planilha_analise))
        ws_destino = wb_analise.Worksheets("BD_Pagos")

        # Ultima linha atual
        ultima_linha_destino = ws_destino.Cells(ws_destino.Rows.Count, 1).End(-4162).Row
        logger.info(f"BD_Pagos: ultima linha atual = {ultima_linha_destino}")

        # Coletar IDs existentes para evitar duplicatas
        ids_existentes = set()
        for row in range(2, ultima_linha_destino + 1):
            val = ws_destino.Cells(row, 1).Value
            if val is not None:
                ids_existentes.add(str(val).strip())
        logger.info(f"IDs existentes em BD_Pagos: {len(ids_existentes)}")

        # Abrir fonte de pagos
        logger.info(f"Abrindo fonte de pagos: {ARQUIVO_PAGOS_FONTE.name}...")
        wb_fonte = excel.Workbooks.Open(str(ARQUIVO_PAGOS_FONTE))

        # Encontrar aba BS_Produção
        ws_fonte = None
        for i in range(1, wb_fonte.Worksheets.Count + 1):
            nome = wb_fonte.Worksheets(i).Name
            if "BS_Produ" in nome or "BS Produ" in nome:
                ws_fonte = wb_fonte.Worksheets(i)
                break
        if ws_fonte is None:
            logger.error("Aba BS_Produção nao encontrada no arquivo de pagos!")
            wb_fonte.Close(False)
            wb_analise.Close(False)
            return 0

        logger.info(f"Aba fonte encontrada: {ws_fonte.Name}")

        # Dados comecam na linha 3 (linha 1 = header tecnico, linha 2 = header legivel)
        ultima_linha_fonte = ws_fonte.Cells(ws_fonte.Rows.Count, 2).End(-4162).Row
        logger.info(f"Fonte: {ultima_linha_fonte - 2} linhas de dados")

        # Coluna "Comprado em" na fonte = col 16
        COL_COMPRADO_EM_FONTE = 16
        COL_ID_FONTE = 2  # idprocessos

        # Filtrar linhas: Comprado em >= 01/01/2025 e ID nao duplicado
        linhas_novas = []
        for row in range(3, ultima_linha_fonte + 1):
            # Verificar data
            data_compra = ws_fonte.Cells(row, COL_COMPRADO_EM_FONTE).Value
            if data_compra is None:
                continue

            # Converter para datetime se necessario
            try:
                if hasattr(data_compra, 'year'):
                    dt = datetime(data_compra.year, data_compra.month, data_compra.day)
                else:
                    dt = datetime.strptime(str(data_compra)[:10], "%Y-%m-%d")
            except Exception:
                continue

            if dt < DATA_MINIMA_PAGOS:
                continue

            # Verificar duplicata
            id_proc = str(ws_fonte.Cells(row, COL_ID_FONTE).Value or "").strip()
            if id_proc in ids_existentes:
                continue

            linhas_novas.append(row)

        total_novos = len(linhas_novas)
        logger.info(f"Linhas novas a adicionar (pos-filtro): {total_novos}")

        if total_novos == 0:
            logger.info("Nenhum registro novo para BD_Pagos.")
            wb_fonte.Close(False)
            wb_analise.Save()
            wb_analise.Close(False)
            return 0

        # Colar dados linha a linha usando o mapeamento
        linha_inicio_destino = ultima_linha_destino + 1

        for idx, row_fonte in enumerate(linhas_novas):
            row_destino = linha_inicio_destino + idx
            for col_dest, col_src in MAPA_PAGOS.items():
                valor = ws_fonte.Cells(row_fonte, col_src).Value
                ws_destino.Cells(row_destino, col_dest).Value = valor

            if idx % 500 == 0 and idx > 0:
                logger.info(f"  Progresso: {idx}/{total_novos} linhas coladas...")

        logger.info(f"Dados colados: linhas {linha_inicio_destino} a {linha_inicio_destino + total_novos - 1}")

        wb_fonte.Close(False)

        # Estender formulas das colunas calculadas
        logger.info("Estendendo formulas de BD_Pagos...")
        for col in COLUNAS_FORMULA_PAGOS:
            celula_modelo = ws_destino.Cells(ultima_linha_destino, col)
            if celula_modelo.HasFormula:
                rng_formula_origem = ws_destino.Range(celula_modelo, celula_modelo)
                rng_formula_destino = ws_destino.Range(
                    ws_destino.Cells(linha_inicio_destino, col),
                    ws_destino.Cells(linha_inicio_destino + total_novos - 1, col)
                )
                rng_formula_origem.Copy()
                rng_formula_destino.PasteSpecial(-4123)  # xlPasteFormulas
                logger.info(f"  Formula estendida na coluna {col}")
            else:
                logger.warning(f"  Coluna {col} nao tem formula na linha {ultima_linha_destino}")

        excel.CutCopyMode = False

        # Redimensionar tabela (Tabela4)
        nova_ultima_linha = linha_inicio_destino + total_novos - 1
        try:
            tabela = ws_destino.ListObjects("Tabela4")
            # BH = coluna 60
            novo_ref = f"A1:BH{nova_ultima_linha}"
            tabela.Resize(ws_destino.Range(novo_ref))
            logger.info(f"Tabela4 redimensionada para {novo_ref}")
        except Exception as e:
            logger.warning(f"Erro ao redimensionar Tabela4: {e}")

        # Salvar
        wb_analise.Save()
        logger.info("BD_Pagos atualizada com sucesso!")
        wb_analise.Close(False)

        return total_novos

    except Exception as e:
        logger.error(f"Erro ao alimentar BD_Pagos: {e}", exc_info=True)
        raise
    finally:
        if excel:
            try:
                excel.ScreenUpdating = True
                excel.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def atualizar_dinamicas_e_performance(planilha_analise, logger):
    """Abre a planilha, atualiza todas as tabelas dinamicas (pivots)
    e forca recalculo das abas de Performance."""

    import pythoncom
    pythoncom.CoInitialize()

    excel = None
    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False

        logger.info("Abrindo planilha para atualizar dinamicas e Performance...")
        wb = excel.Workbooks.Open(str(planilha_analise))

        # Atualizar todas as tabelas dinamicas (20 pivots em "Analise meio")
        logger.info("Atualizando tabelas dinamicas (RefreshAll)...")
        wb.RefreshAll()

        # Forcar recalculo de todas as formulas
        logger.info("Forcando recalculo de formulas...")
        excel.CalculateFull()

        # Aguardar processamento
        import time as _time
        _time.sleep(3)

        # Contar pivots atualizados
        total_pivots = 0
        for i in range(1, wb.Worksheets.Count + 1):
            ws = wb.Worksheets(i)
            total_pivots += ws.PivotTables().Count

        logger.info(f"Atualizadas {total_pivots} tabelas dinamicas")
        logger.info("Performance_Compradores e Performance_Geral recalculadas")

        wb.Save()
        logger.info("Planilha salva apos atualizacao.")
        wb.Close(False)

        return total_pivots

    except Exception as e:
        logger.error(f"Erro ao atualizar dinamicas: {e}", exc_info=True)
        raise
    finally:
        if excel:
            try:
                excel.ScreenUpdating = True
                excel.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Fluxo B — Atualizar arquivo consolidado na pasta Marco
# ---------------------------------------------------------------------------
def atualizar_arquivo_consolidado(caminho_relatorio, data_inicio, data_fim, logger):
    """Atualiza o arquivo consolidado (Fluxo B) na pasta Parcerias/Marco.

    1. Encontra o arquivo mais recente na pasta do mês
    2. Copia-o com a nova data
    3. Cola dados novos no BD_EnvioParceiros
    4. Estende fórmulas e redimensiona tabela
    """
    import pythoncom
    import shutil
    import glob

    pythoncom.CoInitialize()

    try:
        # Identificar pasta do mês
        mes_ref = data_fim.month
        ano_ref = data_fim.year
        meses_nomes = {
            1: "01. Janeiro", 2: "02. Fevereiro", 3: "03. Marco",
            4: "04. Abril", 5: "05. Maio", 6: "06. Junho",
            7: "07. Julho", 8: "08. Agosto", 9: "09. Setembro",
            10: "10. Outubro", 11: "11. Novembro", 12: "12. Dezembro",
        }
        pasta_mes = PASTA_BASE_ANALISE / meses_nomes.get(mes_ref, f"{mes_ref:02d}. Mes")
        pasta_mes.mkdir(parents=True, exist_ok=True)
        logger.info(f"Pasta consolidada: {pasta_mes}")

        # Encontrar arquivo mais recente na pasta
        pattern = str(pasta_mes / "*_Analise Parcerias.xlsx")
        existentes = sorted(glob.glob(pattern))

        if not existentes:
            logger.info("Nenhum arquivo consolidado anterior encontrado. Copiando do arquivo base.")
            origem = ARQUIVO_BASE
        else:
            origem = Path(existentes[-1])
            logger.info(f"Base para cópia: {origem.name}")

        # Nome do novo arquivo
        nome_novo = f"{data_fim.strftime('%Y.%m.%d')}_Analise Parcerias.xlsx"
        destino = pasta_mes / nome_novo

        if destino.exists():
            logger.info(f"Arquivo {nome_novo} já existe. Atualizando in-place.")
        else:
            shutil.copy2(str(origem), str(destino))
            logger.info(f"Cópia criada: {nome_novo}")

        # Abrir e alimentar BD_EnvioParceiros
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        wb_dest = excel.Workbooks.Open(str(destino), CorruptLoad=1)
        wb_rel = excel.Workbooks.Open(str(caminho_relatorio))

        ws_dest = wb_dest.Worksheets("BD_EnvioParceiros")
        ws_rel = wb_rel.Worksheets(1)

        # Última linha no destino
        ult_dest = ws_dest.Cells(ws_dest.Rows.Count, 1).End(-4162).Row
        # Última linha no relatório
        ult_rel = ws_rel.Cells(ws_rel.Rows.Count, 1).End(-4162).Row
        cols_rel = ws_rel.Cells(1, ws_rel.Columns.Count).End(-4159).Column

        logger.info(f"Destino: {ult_dest} linhas, Relatório: {ult_rel - 1} linhas novas")

        if ult_rel > 1:
            # Copiar dados (sem cabeçalho)
            rng_src = ws_rel.Range(
                ws_rel.Cells(2, 1), ws_rel.Cells(ult_rel, cols_rel)
            )
            rng_dst = ws_dest.Cells(ult_dest + 1, 1)
            rng_src.Copy(rng_dst)

            nova_ult = ult_dest + (ult_rel - 1)
            logger.info(f"Dados colados: +{ult_rel - 1} linhas")

            # Fechar relatório antes de estender fórmulas
            try:
                wb_rel.Close(False)
            except Exception:
                pass

            # Aguardar Excel estabilizar
            logger.info("Aguardando Excel estabilizar (15s)...")
            time.sleep(15)

            # Estender fórmulas (com retry)
            logger.info("Estendendo fórmulas no Fluxo B...")
            total_cols = 0
            for tentativa_ext in range(3):
                try:
                    total_cols = ws_dest.Cells(1, ws_dest.Columns.Count).End(-4159).Column
                    break
                except Exception:
                    time.sleep(5)

            for col in range(1, total_cols + 1):
                for tentativa in range(3):
                    try:
                        cell_ref = ws_dest.Cells(ult_dest, col)
                        if cell_ref.HasFormula:
                            rng_form = ws_dest.Range(
                                ws_dest.Cells(ult_dest, col),
                                ws_dest.Cells(ult_dest, col)
                            )
                            rng_form.Copy(
                                ws_dest.Range(
                                    ws_dest.Cells(ult_dest + 1, col),
                                    ws_dest.Cells(nova_ult, col)
                                )
                            )
                        break
                    except Exception as e:
                        if tentativa < 2:
                            time.sleep(5)
                        else:
                            logger.warning(f"  Fluxo B: coluna {col} falhou após 3 retries: {e}")

            # Redimensionar tabela se existir
            time.sleep(3)
            try:
                if ws_dest.ListObjects.Count > 0:
                    lo = ws_dest.ListObjects(1)
                    new_range = f"A1:{chr(64 + lo.Range.Columns.Count)}{nova_ult}"
                    lo.Resize(ws_dest.Range(new_range))
                    logger.info(f"Tabela redimensionada: {new_range}")
            except Exception as e:
                logger.warning(f"Erro ao redimensionar tabela Fluxo B: {e}")
        else:
            try:
                wb_rel.Close(False)
            except Exception:
                pass

        # Salvar e fechar (com retry)
        time.sleep(5)
        for tentativa in range(3):
            try:
                wb_dest.Save()
                logger.info("Arquivo consolidado salvo!")
                break
            except Exception:
                time.sleep(5)

        try:
            wb_dest.Close(False)
        except Exception:
            pass
        try:
            excel.Quit()
        except Exception:
            pass

        return str(destino)

    except Exception as e:
        logger.error(f"Erro no Fluxo B: {e}", exc_info=True)
        raise
    finally:
        pythoncom.CoUninitialize()


# ---------------------------------------------------------------------------
# Atualizar dashboard HTML
# ---------------------------------------------------------------------------
def atualizar_dashboard_html(logger):
    """Executa _reclassificar_v3.py e _build_v2.py para regenerar o HTML."""
    import subprocess

    pasta_robos = ARQUIVO_BASE.parent
    python = sys.executable

    # 1. Reclassificar parceiros → JSON
    script_reclass = pasta_robos / "_reclassificar_v3.py"
    if script_reclass.exists():
        logger.info(f"Executando: {script_reclass.name}")
        result = subprocess.run(
            [python, str(script_reclass)],
            capture_output=True, text=True, timeout=300,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode != 0:
            logger.error(f"Erro em _reclassificar_v3: {result.stderr[:500]}")
            raise RuntimeError(f"Reclassificação falhou: {result.stderr[:200]}")
        logger.info("Reclassificação concluída → parceiros_data.json")
    else:
        logger.warning(f"{script_reclass.name} não encontrado, pulando.")

    # 2. Rebuildar HTML
    script_build = pasta_robos / "_build_v2.py"
    if script_build.exists():
        logger.info(f"Executando: {script_build.name}")
        result = subprocess.run(
            [python, str(script_build)],
            capture_output=True, text=True, timeout=300,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode != 0:
            logger.error(f"Erro em _build_v2: {result.stderr[:500]}")
            raise RuntimeError(f"Build HTML falhou: {result.stderr[:200]}")
        logger.info("HTML regenerado → e_ai_meu_parca.html")
    else:
        logger.warning(f"{script_build.name} não encontrado, pulando.")


# Notificacao visual
# ---------------------------------------------------------------------------
def notificar(titulo, mensagem):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(titulo, mensagem)
    root.destroy()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    logger = configurar_logging()
    logger.info("=" * 60)
    logger.info("Agente 'e ai, meu parca' iniciado")
    logger.info(f"Data de execucao: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 60)

    driver = None
    try:
        # 1. Calcular periodo incremental a partir do arquivo base
        data_inicio, data_fim = calcular_periodo_incremental(logger)

        if data_inicio is None:
            logger.info("Nenhum periodo novo para processar. Encerrando sem erro.")
            notificar(
                "e aí, meu parça",
                "Arquivo base já está atualizado. Nenhum período novo para processar.",
            )
            return

        logger.info(
            f"Período calculado: {data_inicio.strftime('%d/%m/%Y')} "
            f"a {data_fim.strftime('%d/%m/%Y')}"
        )

        # 2. Solicitar relatorio na esteira
        driver = iniciar_driver(logger)
        solicitar_relatorio(driver, data_inicio, data_fim, logger)
        logger.info("Status do envio: SUCESSO")

    except Exception as e:
        logger.error(f"Erro ao solicitar relatorio: {e}", exc_info=True)
        notificar(
            "Erro - e ai, meu parca",
            f"Falha ao solicitar o relatorio na esteira.\n\n{e}",
        )
        return
    finally:
        if driver:
            driver.quit()
            logger.info("Navegador fechado.")

    caminho_relatorio = None
    try:
        # 3. Buscar e-mail no Outlook
        anexo = buscar_email_outlook(logger)
        if anexo is None:
            msg = (
                "E-mail com relatorio nao encontrado apos todas as tentativas.\n"
                "Verifique sua caixa de entrada manualmente."
            )
            logger.error(msg)
            logger.info("Status do recebimento do e-mail: FALHA")
            notificar("Erro - e ai, meu parca", msg)
            return

        logger.info("Status do recebimento do e-mail: SUCESSO")

        # 4. Salvar anexo na pasta de parcerias
        caminho_relatorio = salvar_anexo(anexo, data_inicio, data_fim, logger)
        logger.info(f"Caminho final do arquivo: {caminho_relatorio}")

    except Exception as e:
        logger.error(f"Erro ao processar e-mail/anexo: {e}", exc_info=True)
        notificar(
            "Erro - e ai, meu parca",
            f"Falha ao buscar e-mail ou salvar anexo.\n\n{e}",
        )
        return

    # 5. Alimentar planilha de analise (arquivo base fixo)
    try:
        logger.info("--- Iniciando alimentação da planilha de análise ---")

        # 5a. Usar arquivo base fixo (fonte de verdade)
        if not ARQUIVO_BASE.exists():
            notificar(
                "Erro - e aí, meu parça",
                f"Arquivo base não encontrado:\n{ARQUIVO_BASE}",
            )
            return

        planilha_alvo = ARQUIVO_BASE
        logger.info(f"Arquivo base (fonte de verdade): {planilha_alvo.name}")

        # 5b. Alimentar BD_EnvioParceiros (incremental, não sobrescreve)
        total_envio = alimentar_bd_envio_parceiros(
            planilha_alvo, caminho_relatorio, logger
        )
        logger.info(f"BD_EnvioParceiros: +{total_envio} registros")

        # 5b2. Normalizar nomes no DePara
        total_depara = 0
        try:
            total_depara = atualizar_depara(planilha_alvo, logger)
            if total_depara > 0:
                logger.info(f"DePara: +{total_depara} nomes normalizados")
        except Exception as e:
            logger.error(f"Erro ao atualizar DePara (continuando): {e}")

        # 5c. Alimentar BD_Pagos (incremental por ID)
        total_pagos = 0
        try:
            total_pagos = alimentar_bd_pagos(planilha_alvo, logger)
            logger.info(f"BD_Pagos: +{total_pagos} registros")
        except Exception as e:
            logger.error(f"Erro ao alimentar BD_Pagos (continuando): {e}")

        # 5d. Atualizar tabelas dinâmicas e Performance
        total_pivots = 0
        try:
            total_pivots = atualizar_dinamicas_e_performance(planilha_alvo, logger)
        except Exception as e:
            logger.error(f"Erro ao atualizar dinâmicas (continuando): {e}")

        logger.info("Planilha de análise (Arquivo A) atualizada com sucesso!")

        # 5e. Atualizar arquivo consolidado (Arquivo B - pasta Marco)
        msg_fluxo_b = ""
        try:
            logger.info("--- Iniciando atualização do arquivo consolidado (Fluxo B) ---")
            resultado_b = atualizar_arquivo_consolidado(
                caminho_relatorio, data_inicio, data_fim, logger
            )
            if resultado_b:
                msg_fluxo_b = f"\nArquivo consolidado: {resultado_b}\n"
            logger.info("Fluxo B concluído!")
        except Exception as e:
            logger.error(f"Erro no Fluxo B (continuando): {e}")
            msg_fluxo_b = f"\nFluxo B (consolidado): ERRO - {e}\n"

        # 5f. Atualizar dashboard HTML
        msg_html = ""
        try:
            logger.info("--- Atualizando dashboard HTML ---")
            atualizar_dashboard_html(logger)
            msg_html = "\nDashboard HTML atualizado!"
            logger.info("Dashboard HTML atualizado com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao atualizar HTML (continuando): {e}")
            msg_html = f"\nDashboard HTML: ERRO - {e}"

        # 6. Notificar sucesso
        notificar(
            "e aí, meu parça - Concluído!",
            f"Processo finalizado com sucesso!\n\n"
            f"Relatório salvo: {caminho_relatorio.name}\n"
            f"Período: {data_inicio.strftime('%d/%m')} a {data_fim.strftime('%d/%m')}\n\n"
            f"Arquivo base atualizado:\n"
            f"  {planilha_alvo.name}\n"
            f"  +{total_envio} registros em BD_EnvioParceiros\n"
            f"  +{total_pagos} registros em BD_Pagos\n"
            f"  {total_pivots} tabelas dinâmicas atualizadas\n"
            f"  Performance recalculada"
            f"{msg_fluxo_b}{msg_html}",
        )
        logger.info("Processo finalizado com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao alimentar planilha de analise: {e}", exc_info=True)
        notificar(
            "Erro - e ai, meu parca",
            f"Relatorio salvo com sucesso, mas houve erro ao\n"
            f"atualizar a planilha de analise.\n\n{e}",
        )


if __name__ == "__main__":
    main()
