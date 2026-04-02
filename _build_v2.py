"""
Build v2 da plataforma 'E aí, meu parça'
- Visão Geral executiva com graficos, insights, ranking, filtro
- Ação Imediata em Kanban (max 10)
- Explorador com filtros
- Fantasmas
- Chatbot 'Meu parça'
- Identidade PJUS com logo
"""
import json
from datetime import datetime, date, timedelta


# ====================================================================
# FERIADOS NACIONAIS BRASILEIROS
# ====================================================================
def calc_easter(year: int) -> date:
    """Calcula a data da Páscoa para o ano dado (algoritmo Meeus/Jones/Butcher)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    ll = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * ll) // 451
    month = (h + ll - 7 * m + 114) // 31
    day   = ((h + ll - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def get_br_holidays(year: int) -> list:
    """Retorna lista de strings ISO (YYYY-MM-DD) com feriados nacionais do ano."""
    easter = calc_easter(year)
    feriados = set()
    # Feriados fixos
    fixos = [(1,1),(4,21),(5,1),(9,7),(10,12),(11,2),(11,15),(11,20),(12,25)]
    for m, d in fixos:
        feriados.add(date(year, m, d).isoformat())
    # Feriados móveis baseados na Páscoa
    feriados.add((easter - timedelta(days=48)).isoformat())  # Segunda de Carnaval
    feriados.add((easter - timedelta(days=47)).isoformat())  # Terça de Carnaval
    feriados.add((easter - timedelta(days=2)).isoformat())   # Sexta-feira Santa
    feriados.add((easter + timedelta(days=60)).isoformat())  # Corpus Christi
    return sorted(feriados)

# Gera feriados para ano anterior, atual e próximo (cobre sempre a janela de dados)
_anos = [datetime.now().year - 1, datetime.now().year, datetime.now().year + 1]
feriados_list = []
for _ano in _anos:
    feriados_list.extend(get_br_holidays(_ano))
feriados_json = json.dumps(sorted(set(feriados_list)))

JSON_PATH = r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca\parceiros_data.json"
OUT_PATH = r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca\e_ai_meu_parca.html"

LOGO_B64_PATH = r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca\_logo_b64.txt"
AVATAR_B64_PATH = r"C:\Users\tamara.araujo\PJUS INVESTIMENTOS EM DIREITOS CREDITORIOS LTDA\USwork - INTELIGENCIA DE MERCADO\02. robos\e_ai_meu_parca\_avatar_b64.txt"

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)
with open(LOGO_B64_PATH, encoding="utf-8") as f:
    logo_b64 = f.read().strip()
with open(AVATAR_B64_PATH, encoding="utf-8") as f:
    avatar_b64 = f.read().strip()

json_str = json.dumps(data, ensure_ascii=False)
hoje = datetime.now().strftime("%d/%m/%Y")
sem_atual_num    = datetime.now().isocalendar()[1]
ano_iso_atual    = datetime.now().isocalendar()[0]
dia_semana_atual = datetime.now().isoweekday()   # Mon=1 … Sun=7

# Avatar SVG do "Meu parça" - personagem amigavel com gravata
AVATAR_IMG = '<img src="data:image/png;base64,' + avatar_b64 + '" alt="Meu parça" style="width:100%;height:100%;object-fit:cover;border-radius:50%">'
AVATAR_BTN_IMG = '<img src="data:image/png;base64,' + avatar_b64 + '" alt="Meu parça" style="width:100%;height:100%;object-fit:cover;border-radius:50%">'

# ====================================================================
# CSS
# ====================================================================
CSS = r"""
:root{--az:#0074FF;--ae:#0E2F5D;--vd:#00A68C;--ac:#D6F1FF;--ce:#2B313B;--ow:#FCFCFC;
--sh:0 2px 8px rgba(0,0,0,.07);--r4:4px;--r8:8px;--r12:12px;--r16:16px;--tr:.2s ease;--ft:#804080;
--warn:#FF8C00;--danger:#E53E3E;--gold:#FFD400;--silver:#B0B0B0;--bronze:#FF6B35}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#F0F4F8;color:var(--ce);line-height:1.5;-webkit-font-smoothing:antialiased;overflow-x:hidden}

/* HEADER */
.hd{background:linear-gradient(135deg,var(--ae) 0%,#1a4a8a 100%);color:#fff;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:200}
.hd-left{display:flex;align-items:center;gap:16px}
.hd-logo{width:120px;height:auto;filter:brightness(0) invert(1)}
.hd-sep{width:1px;height:32px;background:rgba(255,255,255,.2)}
.hd-title h1{font-size:22px;font-weight:800;letter-spacing:-.5px}
.hd-title .sub{font-size:11px;opacity:.6;font-weight:400}
.hd-right{text-align:right;font-size:11px;opacity:.6}

/* TABS */
.tabs{display:flex;background:var(--ae);padding:0 32px;position:sticky;top:0;z-index:199;border-bottom:1px solid rgba(255,255,255,.08)}
.tab{padding:11px 22px;color:rgba(255,255,255,.5);font-size:12px;font-weight:600;cursor:pointer;border-bottom:3px solid transparent;transition:all var(--tr);white-space:nowrap}
.tab:hover{color:rgba(255,255,255,.8)}
.tab.active{color:#fff;border-bottom-color:var(--vd);background:rgba(255,255,255,.05)}
.tab .cnt{background:rgba(255,255,255,.12);border-radius:20px;padding:1px 7px;font-size:10px;margin-left:5px}
.tab.active .cnt{background:var(--vd)}

/* PANELS */
.pnl{display:none;padding:24px 32px;max-width:1480px;margin:0 auto}
.pnl.active{display:block}

/* SECTION TITLE */
.stit{font-size:15px;font-weight:700;color:var(--ae);margin-bottom:14px;display:flex;align-items:center;gap:8px}
.stit .ico{font-size:18px}

/* KPI CARDS */
.kpis{display:grid;grid-template-columns:repeat(7,1fr);gap:12px;margin-bottom:20px}
.kpi{background:#fff;border-radius:var(--r12);padding:16px;box-shadow:var(--sh);border-left:4px solid var(--az);position:relative;overflow:hidden}
.kpi-l{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;color:#7A8599;margin-bottom:4px}
.kpi-v{font-size:22px;font-weight:800;color:var(--ae);line-height:1.2}
.kpi-d{font-size:10px;color:#7A8599;margin-top:2px}
.kpi.green{border-left-color:var(--vd)}.kpi.orange{border-left-color:var(--warn)}.kpi.red{border-left-color:var(--danger)}.kpi.purple{border-left-color:var(--ft)}

/* INSIGHTS */
.insights{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}
.insight{background:#fff;border-radius:var(--r12);padding:16px;box-shadow:var(--sh);border-top:3px solid var(--vd)}
.insight.warn{border-top-color:var(--warn)}
.insight.danger{border-top-color:var(--danger)}
.insight-icon{font-size:20px;margin-bottom:6px}
.insight-title{font-size:11px;font-weight:600;text-transform:uppercase;color:#7A8599;margin-bottom:4px}
.insight-value{font-size:13px;font-weight:600;color:var(--ae);line-height:1.4}

/* CHART AREA */
.chart-row{display:grid;grid-template-columns:1.2fr .8fr;gap:16px;margin-bottom:20px}
.chart-box{background:#fff;border-radius:var(--r12);padding:20px;box-shadow:var(--sh)}
.chart-box h3{font-size:13px;font-weight:700;color:var(--ae);margin-bottom:12px}
.bars{display:flex;align-items:flex-end;gap:6px;height:160px;padding-top:16px}
.bar-col{flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end}
.bar{width:100%;max-width:40px;border-radius:var(--r4) var(--r4) 0 0;transition:height .5s ease;min-height:2px;position:relative;cursor:default}
.bar:hover::after{content:attr(data-val);position:absolute;top:-18px;left:50%;transform:translateX(-50%);font-size:9px;font-weight:700;color:var(--ae);white-space:nowrap}
.bar-lbl{font-size:9px;color:#7A8599;margin-top:4px;text-align:center;font-weight:500}

/* RANKING */
.rank-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F0F2F5}
.rank-pos{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:#fff;flex-shrink:0}
.rank-pos.g{background:var(--gold);color:#333}.rank-pos.s{background:var(--silver);color:#333}.rank-pos.b{background:var(--bronze)}.rank-pos.d{background:#DDD;color:#666}
.rank-name{font-size:12px;font-weight:600;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rank-val{font-size:11px;font-weight:700;color:var(--ae)}
.rank-bad{font-size:11px;font-weight:700;color:var(--danger)}

/* DISTRIBUTION + BUBBLE */
.dist-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}
.cb-row{display:flex;align-items:center;gap:8px;margin-bottom:5px}
.cb-lbl{width:100px;font-size:11px;font-weight:600;text-align:right;flex-shrink:0}
.cb-trk{flex:1;height:24px;background:#E8EDF2;border-radius:var(--r8);overflow:hidden}
.cb-fill{height:100%;border-radius:var(--r8);display:flex;align-items:center;padding-left:8px;font-size:11px;font-weight:700;color:#fff;min-width:28px;transition:width .5s ease}
.bub-wrap{background:#fff;border-radius:var(--r12);padding:20px;box-shadow:var(--sh);overflow-x:auto}
.bg{display:grid;gap:0}
.bg .hc{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#7A8599;padding:4px;text-align:center}
.bg .rl{font-size:10px;font-weight:600;color:var(--ce);display:flex;align-items:center;justify-content:flex-end;padding-right:10px}
.bg .cell{display:flex;align-items:center;justify-content:center;padding:4px;min-height:44px}
.bub{border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#fff;cursor:default;position:relative;transition:transform var(--tr)}
.bub:hover{transform:scale(1.2)}
.bub-tip{display:none;position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);background:var(--ae);color:#fff;padding:3px 8px;border-radius:4px;font-size:9px;white-space:nowrap;z-index:10;pointer-events:none}
.bub:hover .bub-tip{display:block}

/* TABLES */
.tw{background:#fff;border-radius:var(--r12);box-shadow:var(--sh);overflow:hidden}
.tw table{width:100%;border-collapse:collapse;font-size:11px}
.tw thead th{background:#F7F9FC;padding:9px 10px;text-align:left;font-weight:600;font-size:9px;text-transform:uppercase;letter-spacing:.5px;color:#7A8599;border-bottom:2px solid #E8EDF2;cursor:pointer;user-select:none;white-space:nowrap;position:sticky;top:0;z-index:2}
.tw thead th:hover{background:#EEF2F7;color:var(--az)}
.tw tbody tr{border-bottom:1px solid #F0F2F5;transition:background var(--tr)}
.tw tbody tr:hover{background:#F7F9FC}
.tw tbody td{padding:8px 10px;vertical-align:middle}
/* bordas de prioridade removidas */

/* BADGES */
.bd{display:inline-block;padding:2px 7px;border-radius:14px;font-size:9px;font-weight:600;white-space:nowrap}
.c-dia{background:#0E2F5D;color:#fff}.c-our{background:#FFD400;color:#333}.c-pra{background:#B0B0B0;color:#333}.c-pip{background:#CD7F32;color:#fff}.c-nov{background:#0074FF;color:#fff}.c-rec{background:#17A2B8;color:#fff}.c-ris{background:#E53E3E;color:#fff}.c-ina{background:#2B313B;color:#fff}.c-fan{background:var(--ft);color:#fff}
.s-sau{background:#C6F6D5;color:#22543D}.s-bom{background:var(--ac);color:var(--ae)}.s-ate{background:#FEFCBF;color:#744210}.s-ris-s{background:#FED7AA;color:#9C4221}.s-cri{background:#FED7D7;color:#9B2C2C}.s-rec{background:#E0F7FA;color:#00796B}.s-na{background:#E2E8F0;color:#718096}
.p-cri{background:#FED7D7;color:#9B2C2C;font-weight:700}.p-alt{background:#FED7AA;color:#9C4221}.p-med{background:#FEFCBF;color:#744210}.p-bai{background:var(--ac);color:var(--ae)}.p-obs{background:#E2E8F0;color:#718096}
.b-sus{background:var(--ft);color:#fff;font-weight:700}
.spk{font-family:'Courier New',monospace;font-size:12px;letter-spacing:1px;color:var(--az);white-space:nowrap}
.spk-bar{display:inline-flex;align-items:flex-end;gap:1px;height:36px;vertical-align:middle}
.spk-bar .sb{display:flex;flex-direction:column;align-items:center;width:16px;font-size:7px;color:#2B313B;line-height:1}
.spk-bar .sb .sv{min-height:2px;width:12px;border-radius:2px 2px 0 0}
.spk-bar .sb .sn{margin-bottom:1px;font-weight:600}
.tend-up{color:var(--vd)}.tend-down{color:var(--danger)}.tend-flat{color:#7A8599}

/* EXPAND ROW */
.exr{display:none}.exr.open{display:table-row}
.exr td{padding:12px 16px;background:#F7F9FC;border-left:3px solid var(--az)}
.exc{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.exc .fl{font-size:9px;font-weight:600;text-transform:uppercase;color:#7A8599;margin-bottom:2px}
.exc .fv{font-size:11px;color:var(--ce);line-height:1.3}

/* FILTERS */
.flt{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;align-items:center}
.fi{padding:6px 12px;border:1px solid #D1D9E6;border-radius:var(--r8);font-family:'Inter',sans-serif;font-size:11px;outline:none;min-width:180px}
.fi:focus{border-color:var(--az);box-shadow:0 0 0 3px rgba(0,116,255,.1)}
.fs{padding:6px 24px 6px 10px;border:1px solid #D1D9E6;border-radius:var(--r8);font-family:'Inter',sans-serif;font-size:11px;background:#fff;outline:none;cursor:pointer;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath fill='%237A8599' d='M0 0l5 6 5-6z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 8px center}
.ms-wrap{position:relative}
.ms-btn{padding:6px 12px;border:1px solid #D1D9E6;border-radius:var(--r8);font-family:'Inter',sans-serif;font-size:11px;background:#fff;cursor:pointer;white-space:nowrap;display:flex;align-items:center;gap:4px}
.ms-btn:hover{border-color:var(--az)}
.ms-arrow{font-size:8px;color:#7A8599}
.ms-dd{position:absolute;top:100%;left:0;z-index:999;background:#fff;border:1px solid #D1D9E6;border-radius:var(--r8);box-shadow:0 4px 16px rgba(0,0,0,.12);padding:6px 0;min-width:160px;max-height:240px;overflow-y:auto}
.ms-dd label{display:flex;align-items:center;gap:6px;padding:5px 12px;font-size:11px;color:var(--ce);cursor:pointer;white-space:nowrap}
.ms-dd label:hover{background:#F0F4F8}
.ms-dd input[type=checkbox]{accent-color:var(--az);width:14px;height:14px}
.btn{padding:6px 16px;border:none;border-radius:var(--r8);font-family:'Inter',sans-serif;font-size:11px;font-weight:600;cursor:pointer;transition:all var(--tr)}
.btn-p{background:var(--az);color:#fff}.btn-p:hover{background:#0060D6}
.btn-o{background:transparent;color:var(--az);border:1px solid var(--az)}.btn-o:hover{background:rgba(0,116,255,.05)}
.tc{font-size:10px;color:#7A8599;margin-bottom:6px}

/* FANTASMA */
.fh{background:linear-gradient(135deg,#f5eef8 0%,#fff 100%);padding:16px;border-left:4px solid var(--ft)}
.fh h3{color:var(--ft);font-size:15px;font-weight:700;margin-bottom:2px}
.fh p{font-size:11px;color:#7A8599}

/* KANBAN */
.kanban{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;min-height:400px}
.kanban-col{background:#F0F4F8;border-radius:var(--r12);padding:12px;min-height:300px}
.kanban-col-hd{font-size:12px;font-weight:700;padding:8px 12px;border-radius:var(--r8);margin-bottom:10px;text-align:center}
.kc-todo .kanban-col-hd{background:var(--ac);color:var(--ae)}
.kc-doing .kanban-col-hd{background:#FEFCBF;color:#744210}
.kc-review .kanban-col-hd{background:#FED7AA;color:#9C4221}
.kc-done .kanban-col-hd{background:#C6F6D5;color:#22543D}
.k-card{background:#fff;border-radius:var(--r8);padding:12px;margin-bottom:8px;box-shadow:var(--sh);cursor:grab;border-left:3px solid var(--az);transition:all var(--tr)}
.k-card:hover{box-shadow:0 4px 12px rgba(0,0,0,.12)}
.k-card.dragging{opacity:.5;transform:rotate(2deg)}
.k-card-title{font-size:12px;font-weight:700;color:var(--ae);margin-bottom:4px}
.k-card-desc{font-size:10px;color:#7A8599;margin-bottom:6px;line-height:1.3}
.k-card-meta{display:flex;flex-wrap:wrap;gap:4px;font-size:9px}
.k-card-gain{background:#C6F6D5;color:#22543D;padding:2px 6px;border-radius:10px;font-weight:600;font-size:9px;margin-top:6px;display:inline-block}
.k-card .bd{font-size:8px}

/* CHATBOT */
.chat-btn{position:fixed;bottom:24px;right:24px;width:64px;height:64px;border-radius:50%;background:transparent;color:#fff;border:none;cursor:pointer;box-shadow:0 4px 16px rgba(0,116,255,.35);z-index:300;display:flex;align-items:center;justify-content:center;font-size:24px;transition:all var(--tr);overflow:hidden;padding:0}
.chat-btn:hover{transform:scale(1.08);box-shadow:0 6px 24px rgba(0,116,255,.45)}
.chat-panel{position:fixed;bottom:90px;right:24px;width:360px;height:480px;background:#fff;border-radius:var(--r16);box-shadow:0 8px 32px rgba(0,0,0,.15);z-index:300;display:none;flex-direction:column;overflow:hidden}
.chat-panel.open{display:flex}
.chat-hd{background:linear-gradient(135deg,var(--ae),#1a4a8a);color:#fff;padding:16px;display:flex;align-items:center;gap:10px}
.chat-hd .avatar{width:40px;height:40px;border-radius:50%;overflow:hidden;flex-shrink:0}
.chat-hd-info h3{font-size:14px;font-weight:700}
.chat-hd-info p{font-size:10px;opacity:.7}
.chat-close{margin-left:auto;background:none;border:none;color:#fff;font-size:18px;cursor:pointer;opacity:.6}
.chat-close:hover{opacity:1}
.chat-body{flex:1;padding:16px;overflow-y:auto;background:#F7F9FC}
.chat-msg{margin-bottom:12px;max-width:85%}
.chat-msg.bot{margin-right:auto}
.chat-msg.user{margin-left:auto}
.chat-msg .bubble{padding:10px 14px;border-radius:var(--r12);font-size:12px;line-height:1.4}
.chat-msg.bot .bubble{background:#fff;color:var(--ce);box-shadow:0 1px 4px rgba(0,0,0,.06)}
.chat-msg.user .bubble{background:var(--az);color:#fff}
.chat-msg .time{font-size:9px;color:#7A8599;margin-top:2px}
.chat-input{display:flex;padding:12px;border-top:1px solid #E8EDF2;gap:8px}
.chat-input input{flex:1;border:1px solid #D1D9E6;border-radius:var(--r8);padding:8px 12px;font-family:'Inter',sans-serif;font-size:12px;outline:none}
.chat-input input:focus{border-color:var(--az)}
.chat-input button{background:var(--az);color:#fff;border:none;border-radius:var(--r8);padding:8px 16px;font-weight:600;cursor:pointer;font-size:12px}

/* TOAST */
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--ae);color:#fff;padding:10px 24px;border-radius:var(--r8);font-size:12px;opacity:0;transition:all .3s;z-index:9999;pointer-events:none}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* RESPONSIVE */
@media(max-width:1400px){.kpis{grid-template-columns:repeat(4,1fr)}}
@media(max-width:1200px){.kpis{grid-template-columns:repeat(3,1fr)}.kanban{grid-template-columns:repeat(2,1fr)}.chart-row,.dist-row{grid-template-columns:1fr}.insights{grid-template-columns:repeat(2,1fr)}}
@media(max-width:768px){.kpis{grid-template-columns:1fr}.kanban{grid-template-columns:1fr}.tabs{overflow-x:auto}.flt{flex-direction:column}.fi,.fs{width:100%}.chat-panel{width:calc(100vw - 48px);right:24px}.insights{grid-template-columns:1fr}}
/* STORY BLOCKS */
.story-block{margin-bottom:28px}
.story-hd{display:flex;align-items:center;gap:10px;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #E8EDF2}
.story-num{width:28px;height:28px;border-radius:50%;background:var(--ae);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex-shrink:0}
.story-label{font-size:16px;font-weight:700;color:var(--ae)}
.story-desc{font-size:11px;color:#7A8599;margin-left:auto;font-style:italic}

/* PANORAMA BAR */
.panorama-bar{display:flex;height:36px;border-radius:var(--r8);overflow:hidden;margin-top:12px;box-shadow:var(--sh)}
.panorama-seg{display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;transition:width .6s ease;cursor:default;position:relative}
.panorama-seg:hover::after{content:attr(data-tip);position:absolute;top:-28px;left:50%;transform:translateX(-50%);background:var(--ae);color:#fff;padding:3px 8px;border-radius:4px;font-size:9px;white-space:nowrap;z-index:5}

/* SAUDE ROW */
.saude-row{display:flex;gap:16px}
.saude-meter{display:flex;flex-direction:column;gap:8px}
.saude-bar-row{display:flex;align-items:center;gap:8px}
.saude-lbl{width:80px;font-size:11px;font-weight:600;text-align:right}
.saude-bar{height:22px;border-radius:var(--r4);display:flex;align-items:center;padding-left:8px;font-size:10px;font-weight:700;color:#fff;min-width:24px}

/* PROD ROW */
.prod-row{display:flex;gap:16px}
.prod-table{width:100%;border-collapse:collapse;font-size:11px}
.prod-table th{text-align:left;padding:6px 8px;font-size:9px;text-transform:uppercase;color:#7A8599;border-bottom:2px solid #E8EDF2}
.prod-table td{padding:8px;border-bottom:1px solid #F0F2F5}
.prod-table tr:hover{background:#F7F9FC}
.prod-badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:9px;font-weight:700;color:#fff;transition:transform .15s,box-shadow .15s}
.prod-badge[onclick]:hover{transform:scale(1.08);box-shadow:0 2px 8px rgba(0,0,0,.2)}
.bub[onclick]:hover{transform:scale(1.12);box-shadow:0 2px 12px rgba(0,0,0,.25)}

/* EVOLUTION HEATMAP */
.evo-grid{display:grid;gap:2px;font-size:10px}
.evo-hd{font-weight:700;color:#7A8599;text-align:center;padding:4px 2px;font-size:9px}
.evo-lbl{font-weight:600;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-size:11px}
.evo-cell{border-radius:var(--r4);display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:600;color:#fff;min-height:28px;cursor:default;position:relative}
.evo-cell:hover::after{content:attr(data-tip);position:absolute;bottom:calc(100% + 4px);left:50%;transform:translateX(-50%);background:var(--ae);color:#fff;padding:2px 6px;border-radius:3px;font-size:8px;white-space:nowrap;z-index:5}

/* GG ROW */
.gg-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.gg-danger{border-top:3px solid var(--danger)}
.gg-gain{border-top:3px solid var(--vd)}
.gg-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F0F2F5}
.gg-item:last-child{border:none}
.gg-icon{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.gg-name{font-size:12px;font-weight:600;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gg-val{font-size:11px;font-weight:700}
.gg-tend{font-size:10px;font-weight:600}

/* CONCLUSAO */
.conclusao-box{background:linear-gradient(135deg,var(--ae) 0%,#1a4a8a 100%);border-radius:var(--r12);padding:24px;color:#fff}
.conclusao-box h3{font-size:14px;font-weight:700;margin-bottom:12px;opacity:.9}
.conclusao-item{display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;font-size:12px;line-height:1.5}
.conclusao-bullet{width:8px;height:8px;border-radius:50%;flex-shrink:0;margin-top:5px}
.cb-green{background:var(--vd)}.cb-red{background:var(--danger)}.cb-yellow{background:var(--gold)}.cb-blue{background:var(--az)}.cb-purple{background:var(--ft)}

@media(max-width:1200px){.saude-row,.prod-row{flex-direction:column}.gg-row{grid-template-columns:1fr}}
@media print{.hd,.tabs,.chat-btn,.chat-panel,.toast{display:none!important}.pnl{display:block!important;padding:12px}.tw,.chart-box,.bub-wrap{box-shadow:none;border:1px solid #ddd}}

/* WOW DESTAQUES */
.wow-delta{display:inline-flex;align-items:center;gap:4px;font-weight:700;font-size:13px;padding:2px 8px;border-radius:6px}
.wow-delta.up{color:#22543D;background:#C6F6D5}.wow-delta.down{color:#9B2C2C;background:#FED7D7}.wow-delta.flat{color:#7A8599;background:#E2E8F0}
.wow-kpi{background:#fff;border-radius:var(--r12);padding:18px;box-shadow:var(--sh);border-left:4px solid var(--az);position:relative}
.wow-kpi .wow-kpi-label{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;color:#7A8599;margin-bottom:6px}
.wow-kpi .wow-kpi-value{font-size:24px;font-weight:800;color:var(--ae);line-height:1.2}
.wow-kpi .wow-kpi-sub{font-size:11px;color:#7A8599;margin-top:4px;display:flex;align-items:center;gap:6px}
.wow-insight-item{display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #F0F2F5;font-size:12px;line-height:1.6;color:var(--ce)}
.wow-insight-item:last-child{border-bottom:none}
.wow-insight-bullet{width:8px;height:8px;border-radius:50%;flex-shrink:0;margin-top:6px}
.wow-week-bar{display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.wow-week-bar label{font-weight:600;font-size:13px;white-space:nowrap}
.wow-week-bar select{padding:5px 10px;border-radius:6px;border:1px solid #ccc;font-size:13px;cursor:pointer}
.wow-partial-badge{background:#fff3cd;color:#856404;border:1px solid #ffc107;border-radius:6px;padding:4px 10px;font-size:12px;font-weight:600}
.wow-proj-note{font-size:11px;color:#888;margin-top:3px;font-style:italic}
/* PERSPECTIVA */
.persp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px}
.persp-card{border-radius:var(--r12);padding:16px 18px;position:relative;overflow:hidden}
.persp-card.green{background:#f0fff4;border-left:4px solid #38a169}
.persp-card.red{background:#fff5f5;border-left:4px solid var(--danger)}
.persp-card.blue{background:#ebf8ff;border-left:4px solid var(--az)}
.persp-card.orange{background:#fffaf0;border-left:4px solid var(--warn)}
.persp-card.purple{background:#faf5ff;border-left:4px solid #805ad5}
.persp-card .pc-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#7A8599;margin-bottom:4px}
.persp-card .pc-value{font-size:22px;font-weight:800;line-height:1.2;color:var(--ae)}
.persp-card .pc-sub{font-size:11px;color:#7A8599;margin-top:4px;line-height:1.5}
.persp-action{background:#fff;border:1px solid #E2E8F0;border-radius:var(--r8);padding:12px 16px;margin-bottom:8px;display:flex;align-items:flex-start;gap:10px;font-size:12px;line-height:1.6}
.persp-action .pa-icon{font-size:18px;flex-shrink:0;margin-top:1px}
.persp-action strong{color:var(--ae)}
.persp-dormentes{margin-top:10px}
.persp-dormentes summary{cursor:pointer;font-size:12px;font-weight:600;color:var(--az);padding:4px 0}
.persp-dormentes table{margin-top:8px;width:100%;font-size:11px;border-collapse:collapse}
.persp-dormentes td,.persp-dormentes th{padding:4px 8px;border-bottom:1px solid #F0F2F5;text-align:left}
.persp-dormentes th{font-weight:700;color:#7A8599;font-size:10px;text-transform:uppercase}
/* NAME AUTOCOMPLETE */
.name-ac-wrap{position:relative;display:inline-block}
.name-suggest{position:absolute;top:100%;left:0;min-width:260px;max-width:380px;background:#fff;border:1px solid #dde3ec;border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.12);z-index:9999;overflow:hidden;margin-top:2px}
.name-suggest-item{display:flex;align-items:center;justify-content:space-between;padding:7px 12px;cursor:pointer;gap:10px;transition:background .12s}
.name-suggest-item:hover{background:#f0f6ff}
.ns-name{font-size:12px;font-weight:600;color:var(--ae);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px}
.ns-cat{font-size:10px;font-weight:600;padding:1px 6px;border-radius:4px;background:#E2E8F0;color:#7A8599;white-space:nowrap;flex-shrink:0}
\n/* KANBAN PLANNER */\n.kanban-board{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:16px 0}\n.kanban-col{background:#F7F9FC;border-radius:12px;padding:12px;min-height:400px}\n.kanban-col-hd{font-size:11px;font-weight:700;text-transform:uppercase;color:#7A8599;margin-bottom:12px;display:flex;align-items:center;justify-content:space-between}\n.col-cnt{background:#E2E8F0;color:#4A5568;border-radius:10px;padding:1px 7px;font-size:10px;margin-left:6px}\n.task-card{background:#fff;border-radius:8px;padding:12px;margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);cursor:grab;border-left:4px solid #ccc;transition:box-shadow .15s}\n.task-card:hover{box-shadow:0 3px 10px rgba(0,0,0,.12)}\n.task-card[data-prio="Alta"]{border-left-color:#E05353}\n.task-card[data-prio="Média"]{border-left-color:#F5A623}\n.task-card[data-prio="Baixa"]{border-left-color:#4CAF50}\n.task-card-title{font-size:13px;font-weight:700;color:var(--ae);margin-bottom:4px}\n.task-card-desc{font-size:11px;color:#7A8599;margin-bottom:8px;line-height:1.4}\n.task-card-meta{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:10px;color:#9BA5C0}\n.task-prio-badge{padding:2px 7px;border-radius:10px;font-weight:700;font-size:10px}\n.task-prio-badge.Alta{background:#FED7D7;color:#9B2C2C}\n.task-prio-badge.Média{background:#FEEBC8;color:#7B341E}\n.task-prio-badge.Baixa{background:#C6F6D5;color:#22543D}\n.task-del-btn{background:none;border:none;cursor:pointer;color:#CBD5E0;font-size:14px;padding:0;line-height:1;margin-left:auto}\n.task-del-btn:hover{color:#E05353}\n.kanban-dropzone{min-height:40px}\n.kanban-dropzone.drag-over{background:#EBF8FF;border-radius:8px}\n.planner-toolbar{display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap}\n.planner-toolbar input{padding:7px 12px;border:1px solid #dde3ec;border-radius:8px;font-size:13px;min-width:200px}\n.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.45);z-index:10000;display:flex;align-items:center;justify-content:center}\n.modal-box{background:#fff;border-radius:14px;padding:24px;min-width:380px;max-width:500px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.25)}\n.modal-box h3{font-size:16px;font-weight:700;color:var(--ae);margin-bottom:16px}\n.modal-field{margin-bottom:12px}\n.modal-field label{display:block;font-size:11px;font-weight:600;color:#7A8599;text-transform:uppercase;margin-bottom:4px}\n.modal-field input,.modal-field textarea,.modal-field select{width:100%;padding:8px 10px;border:1px solid #dde3ec;border-radius:7px;font-size:13px;box-sizing:border-box;font-family:inherit}\n.modal-field textarea{resize:vertical;min-height:70px}\n.modal-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:16px}\n/* CRM MOCKUP */\n.crm-mock-box{background:linear-gradient(135deg,#F0F4FF,#F7F0FF);border:1px dashed #B0BEE8;border-radius:10px;padding:14px;margin-top:12px}\n.crm-mock-header{font-weight:700;font-size:12px;color:#4A5A8A;margin-bottom:10px;display:flex;align-items:center;gap:6px}\n.crm-badge-tag{background:#6C63FF22;color:#6C63FF;border-radius:20px;padding:2px 8px;font-size:10px;border:1px solid #6C63FF44}\n.crm-mock-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px}\n.crm-field{background:#fff;border-radius:6px;padding:8px;text-align:center}\n.crm-field label{display:block;font-size:9px;color:#9BA5C0;font-weight:600;text-transform:uppercase;margin-bottom:4px}\n.crm-field span{font-size:12px;color:#3A4A6A}\n.crm-note{font-size:10px;color:#8A97B8;font-style:italic;text-align:center}\n/* MOTIVOS REPROVACAO */\n.motivos-box{background:#FFF5F5;border:1px solid #FED7D7;border-radius:8px;padding:10px 14px;margin-top:10px}\n.motivos-box h5{font-size:10px;font-weight:700;text-transform:uppercase;color:#9B2C2C;margin-bottom:8px;letter-spacing:.5px}\n.motivo-item{display:flex;align-items:center;justify-content:space-between;font-size:11px;padding:3px 0;border-bottom:1px solid #FEB2B222}\n.motivo-item:last-child{border-bottom:none}\n.motivo-label{color:#7B341E;flex:1}\n.motivo-cnt{background:#FED7D7;color:#9B2C2C;border-radius:10px;padding:1px 8px;font-size:10px;font-weight:700}\n/* BENCHMARK UF */\n.bench-box{background:#F0FFF4;border:1px solid #C6F6D5;border-radius:8px;padding:10px 14px;margin-top:10px}\n.bench-box h5{font-size:10px;font-weight:700;text-transform:uppercase;color:#276749;margin-bottom:8px;letter-spacing:.5px}\n.bench-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}\n.bench-kpi{background:#fff;border-radius:6px;padding:8px;text-align:center}\n.bench-kpi .bk-label{font-size:9px;color:#7A8599;text-transform:uppercase;font-weight:600;margin-bottom:2px}\n.bench-kpi .bk-value{font-size:16px;font-weight:800;color:var(--ae)}\n.bench-kpi .bk-sub{font-size:10px;color:#7A8599;margin-top:2px}\n.bench-kpi .bk-up{color:#22543D;font-weight:700}\n.bench-kpi .bk-down{color:#9B2C2C;font-weight:700}\n/* SAZONALIDADE PROJETADA */\n.sazon-box{background:#FFFAF0;border:1px solid #FEEBC8;border-radius:8px;padding:10px 14px;margin-top:10px}\n.sazon-box h5{font-size:10px;font-weight:700;text-transform:uppercase;color:#7B341E;margin-bottom:8px;letter-spacing:.5px}\n.sazon-table{width:100%;border-collapse:collapse;font-size:11px}\n.sazon-table th{font-size:9px;text-transform:uppercase;color:#7A8599;font-weight:700;padding:3px 6px;text-align:left}\n.sazon-table td{padding:3px 6px;border-bottom:1px solid #FEEBC822}\n.sazon-table tr:last-child td{border-bottom:none}\n/* CHURN BADGE */\n.churn-badge{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:700;white-space:nowrap}\n.churn-badge.alto{background:#FED7D7;color:#9B2C2C}\n.churn-badge.medio{background:#FEEBC8;color:#7B341E}\n.churn-badge.baixo{background:#C6F6D5;color:#22543D}\n/* PARCEIROS EM RISCO TABLE */\n.risco-table{width:100%;border-collapse:collapse;font-size:12px}\n.risco-table th{font-size:10px;text-transform:uppercase;color:#7A8599;font-weight:700;padding:6px 8px;text-align:left;border-bottom:2px solid #F0F2F5}\n.risco-table td{padding:6px 8px;border-bottom:1px solid #F7F9FC}\n.risco-table tr:last-child td{border-bottom:none}
"""

# ====================================================================
# HTML BODY
# ====================================================================
HTML_BODY = """
<div class="hd">
  <div class="hd-left">
    <img class="hd-logo" src="data:image/png;base64,__LOGO__" alt="PJUS">
    <div class="hd-sep"></div>
    <div class="hd-title">
      <h1>E aí, meu parça</h1>
      <div class="sub">Gestao Estrategica de Parceiros</div>
    </div>
  </div>
  <div class="hd-right" id="refDate"></div>
</div>

<div class="tabs">
  <div class="tab active" data-tab="visao">Visão Geral</div>
  <div class="tab" data-tab="dados">Lista de Dados <span class="cnt" id="expCnt">0</span></div>
  <div class="tab" data-tab="destaques">Destaques da Semana</div>
  <div class="tab" data-tab="glossario">Glossário</div>
  <div class="tab" data-tab="planner">&#128203; Planner</div>
</div>

<!-- VISAO GERAL -->
<div class="pnl active" id="p-visao">

  <!-- FILTROS GLOBAIS -->
  <div class="global-filters" style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;padding:12px 16px;background:#fff;border-radius:var(--r12);box-shadow:var(--sh);align-items:center">
    <div class="ms-wrap" id="msCat"><button class="ms-btn" onclick="toggleMS('msCat')">Categorias <span class="ms-arrow">&#9662;</span></button><div class="ms-dd" style="display:none"><label><input type="checkbox" value="Diamante" onchange="applyGlobalFilters()"> Diamante</label><label><input type="checkbox" value="Prata" onchange="applyGlobalFilters()"> Prata</label><label><input type="checkbox" value="Bronze" onchange="applyGlobalFilters()"> Bronze</label><label><input type="checkbox" value="Novo" onchange="applyGlobalFilters()"> Novo</label><label><input type="checkbox" value="Em Recuperação" onchange="applyGlobalFilters()"> Em Recuperação</label><label><input type="checkbox" value="Inativo" onchange="applyGlobalFilters()"> Inativo</label><label><input type="checkbox" value="Fantasma" onchange="applyGlobalFilters()"> Fantasma</label></div></div>
    <div class="ms-wrap" id="msSaude"><button class="ms-btn" onclick="toggleMS('msSaude')">Saúde <span class="ms-arrow">&#9662;</span></button><div class="ms-dd" style="display:none"><label><input type="checkbox" value="Excelente" onchange="applyGlobalFilters()"> Excelente</label><label><input type="checkbox" value="Bom" onchange="applyGlobalFilters()"> Bom</label><label><input type="checkbox" value="Regular" onchange="applyGlobalFilters()"> Regular</label><label><input type="checkbox" value="Ruim" onchange="applyGlobalFilters()"> Ruim</label><label><input type="checkbox" value="Péssimo" onchange="applyGlobalFilters()"> Péssimo</label><label><input type="checkbox" value="Em Recuperação" onchange="applyGlobalFilters()"> Em Recuperação</label><label><input type="checkbox" value="N/A" onchange="applyGlobalFilters()"> N/A</label></div></div>
    <div class="ms-wrap" id="msEnvio"><button class="ms-btn" onclick="toggleMS('msEnvio')">Envio <span class="ms-arrow">&#9662;</span></button><div class="ms-dd" style="display:none"><label><input type="checkbox" value="Consistente" onchange="applyGlobalFilters()"> Consistente</label><label><input type="checkbox" value="Regular" onchange="applyGlobalFilters()"> Regular</label><label><input type="checkbox" value="Esporadico" onchange="applyGlobalFilters()"> Esporádico</label><label><input type="checkbox" value="Novo" onchange="applyGlobalFilters()"> Novo</label><label><input type="checkbox" value="Sem envio" onchange="applyGlobalFilters()"> Sem envio</label></div></div>
    <div class="ms-wrap" id="msRegional"><button class="ms-btn" onclick="toggleMS('msRegional')">Regional <span class="ms-arrow">&#9662;</span></button><div class="ms-dd" style="display:none"><label><input type="checkbox" value="SP (C/D)" onchange="applyGlobalFilters()"> SP (C/D)</label><label><input type="checkbox" value="Regional A" onchange="applyGlobalFilters()"> Regional A</label><label><input type="checkbox" value="Regional B" onchange="applyGlobalFilters()"> Regional B</label><label><input type="checkbox" value="Regional D" onchange="applyGlobalFilters()"> Regional D</label><label><input type="checkbox" value="N/I" onchange="applyGlobalFilters()"> N/I</label></div></div>
    <div style="display:flex;gap:4px;align-items:center"><label style="font-size:10px;color:#7A8599">De</label><input type="date" class="fi" id="gfDateFrom" onchange="applyGlobalFilters()" style="font-size:11px;padding:4px 6px"><label style="font-size:10px;color:#7A8599">Até</label><input type="date" class="fi" id="gfDateTo" onchange="applyGlobalFilters()" style="font-size:11px;padding:4px 6px"></div>
    <div class="name-ac-wrap"><input type="text" class="fi" id="gfNome" placeholder="Buscar parceiro..." oninput="applyGlobalFilters()" style="min-width:160px" autocomplete="off"><div id="gfNomeSuggest" class="name-suggest" style="display:none"></div></div>
    <button class="btn btn-o" onclick="resetGlobalFilters()">Limpar</button>
    <span style="margin-left:auto;font-size:10px;color:#7A8599" id="gfCount"></span>
  </div>

  <!-- BLOCO 1: PANORAMA -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">1</span><span class="story-label">Panorama Geral</span><span class="story-desc">como esta a operação agora</span></div>
    <div class="kpis" id="kpiGrid"></div>
    <div class="panorama-bar" id="panoramaBar"></div>
  </div>

  <!-- BLOCO 2: SAUDE -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">2</span><span class="story-label">Saude da Base</span><span class="story-desc">como estao os parceiros</span></div>
    <div class="saude-row">
      <div class="chart-box" style="flex:1"><h3>Distribuição de Saude</h3><div id="saudeChart"></div></div>
      <div class="chart-box" style="flex:1"><h3>Matriz Categoria x Saude</h3><div class="bub-wrap"><div class="bg" id="bubGrid"></div></div></div>
    </div>
  </div>

  <!-- BLOCO 3: PRODUCAO -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">3</span><span class="story-label">Produção e Desempenho</span><span class="story-desc">o que esta sendo gerado</span></div>
    <div class="prod-row">
      <div class="chart-box" style="flex:1.2"><h3>Produção por Categoria</h3><div id="prodChart"></div></div>
      <div class="chart-box" style="flex:.8">
        <h3>Top 5 Parceiros</h3><div id="rankTop"></div>
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid #E8EDF2"><h3>Ticket Médio por Categoria</h3><div id="ticketChart"></div></div>
      </div>
    </div>
  </div>

  <!-- BLOCO 4: EVOLUCAO -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">4</span><span class="story-label">Evolução</span><span class="story-desc">como a base se comporta ao longo do tempo</span></div>
    <div class="chart-box">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <div style="display:flex;gap:8px">
          <button class="btn btn-p evo-btn active" data-view="mensal" onclick="setEvoView('mensal')">Mensal</button>
          <button class="btn btn-o evo-btn" data-view="semanal" onclick="setEvoView('semanal')">Semanal</button>
        </div>
        <div style="display:flex;gap:8px;align-items:center">
          <span style="font-size:10px;color:#7A8599">Filtrar categoria:</span>
          <select class="fs" id="evoCatFilter" onchange="renderEvo()" style="min-width:140px">
            <option value="">Todas</option>
            <option>Diamante</option><option>Ouro</option><option>Prata</option><option>Bronze</option><option>Em Recuperação</option><option>Inativo</option>
          </select>
        </div>
      </div>
      <div id="evoChart"></div>
      <h3 style="margin-top:24px;font-size:13px;font-weight:700;color:var(--ae)">Evolução por Regional</h3>
      <div id="evoRegChart" style="margin-top:8px"></div>
      <div id="evoHist" style="margin-top:16px"></div>
    </div>
  </div>

  <!-- BLOCO 5: GARGALOS E GANHOS -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">5</span><span class="story-label">Gargalos e Oportunidades</span><span class="story-desc">onde agir agora</span></div>
    <div class="gg-row">
      <div class="chart-box gg-danger"><h3 style="color:var(--danger)">Gargalos &mdash; Parceiros em Queda</h3><div id="gargalos"></div></div>
      <div class="chart-box gg-gain"><h3 style="color:var(--vd)">Oportunidades &mdash; Parceiros em Alta</h3><div id="ganhos"></div></div>
    </div>
  </div>

  <!-- BLOCO 6: PROPOSTAS DE ACAO -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">6</span><span class="story-label">Propostas de Ação</span><span class="story-desc">3 ações prioritárias com ganho esperado</span></div>
    <div id="conclusao"></div>
  </div>

  <!-- BLOCO 7: VISAO POR REGIONAL -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">7</span><span class="story-label">Visão por Regional</span><span class="story-desc">distribuição geográfica da base</span></div>
    <div class="chart-box" style="margin-bottom:16px"><h3>Indicadores por Regional</h3><div id="regionalTable"></div></div>
    <div class="chart-box" id="brazilMapBox">
      <h3>Distribuição Geográfica da Carteira</h3>
      <div id="brazilMap"></div>
    </div>
  </div>

  <!-- BLOCO 8: PARCEIROS EM RISCO -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num" style="background:#E05353">&#x26A0;</span><span class="story-label">Parceiros em Risco de Churn</span><span class="story-desc">top 5 com maior probabilidade de abandono</span></div>
    <div class="chart-box" id="riscoTable"></div>
  </div>

  <!-- HIGHLIGHTS -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">&#x2605;</span><span class="story-label">Destaques</span><span class="story-desc">flags e sinais especiais</span></div>
    <div class="kpis" id="highlights" style="grid-template-columns:repeat(4,1fr)"></div>
  </div>

</div>

<!-- ACAO IMEDIATA (KANBAN) -->

<!-- EXPLORADOR -->
<div class="pnl" id="p-dados">
  <div class="flt" style="flex-wrap:wrap;gap:8px;align-items:center">
    <div class="name-ac-wrap"><input type="text" class="fi" id="searchName" placeholder="Buscar por nome..." style="min-width:160px" autocomplete="off"><div id="searchNameSuggest" class="name-suggest" style="display:none"></div></div>
    <div class="ms-wrap" id="msCatDados"><button class="ms-btn" onclick="toggleMS('msCatDados')">Categorias <span class="ms-arrow">&#9662;</span></button><div class="ms-dd" style="display:none"><label><input type="checkbox" value="Diamante" onchange="filterExplorer()"> Diamante</label><label><input type="checkbox" value="Prata" onchange="filterExplorer()"> Prata</label><label><input type="checkbox" value="Bronze" onchange="filterExplorer()"> Bronze</label><label><input type="checkbox" value="Novo" onchange="filterExplorer()"> Novo</label><label><input type="checkbox" value="Em Recuperação" onchange="filterExplorer()"> Em Recuperação</label><label><input type="checkbox" value="Inativo" onchange="filterExplorer()"> Inativo</label><label><input type="checkbox" value="Fantasma" onchange="filterExplorer()"> Fantasma</label></div></div>
    <div class="ms-wrap" id="msSaudeDados"><button class="ms-btn" onclick="toggleMS('msSaudeDados')">Saúde <span class="ms-arrow">&#9662;</span></button><div class="ms-dd" style="display:none"><label><input type="checkbox" value="Excelente" onchange="filterExplorer()"> Excelente</label><label><input type="checkbox" value="Bom" onchange="filterExplorer()"> Bom</label><label><input type="checkbox" value="Regular" onchange="filterExplorer()"> Regular</label><label><input type="checkbox" value="Ruim" onchange="filterExplorer()"> Ruim</label><label><input type="checkbox" value="Péssimo" onchange="filterExplorer()"> Péssimo</label><label><input type="checkbox" value="Em Recuperação" onchange="filterExplorer()"> Em Recuperação</label><label><input type="checkbox" value="N/A" onchange="filterExplorer()"> N/A</label></div></div>
    <div class="ms-wrap" id="msRegionalDados"><button class="ms-btn" onclick="toggleMS('msRegionalDados')">Regional <span class="ms-arrow">&#9662;</span></button><div class="ms-dd" style="display:none"><label><input type="checkbox" value="SP (C/D)" onchange="filterExplorer()"> SP (C/D)</label><label><input type="checkbox" value="Regional A" onchange="filterExplorer()"> Regional A</label><label><input type="checkbox" value="Regional B" onchange="filterExplorer()"> Regional B</label><label><input type="checkbox" value="Regional D" onchange="filterExplorer()"> Regional D</label><label><input type="checkbox" value="N/I" onchange="filterExplorer()"> N/I</label></div></div>
    <div style="display:flex;gap:4px;align-items:center"><label style="font-size:10px;color:#7A8599">De</label><input type="date" class="fi" id="dadosDateFrom" onchange="filterExplorer()" style="font-size:11px;padding:4px 6px"><label style="font-size:10px;color:#7A8599">Até</label><input type="date" class="fi" id="dadosDateTo" onchange="filterExplorer()" style="font-size:11px;padding:4px 6px"></div>
    <button class="btn btn-p" onclick="exportCSV()">Exportar CSV</button>
    <button class="btn btn-o" onclick="resetFilters()">Limpar</button>
  </div>
  <div class="tc" id="expInfo"></div>
  <div class="tw" style="max-height:calc(100vh - 200px);overflow-y:auto">
    <table id="expTable">
      <thead><tr>
        <th data-col="nome" title="Nome ajustado do parceiro (normalizado para evitar duplicidades)">Nome</th><th data-col="cat" title="Categoria estratégica: Diamante (top), Prata, Bronze (sem compra), Novo, Em Recuperação, Inativo, Fantasma (compra sem lead)">Cat.</th><th data-col="regional" title="Regional do parceiro baseada na UF dos processos">Reg.</th><th data-col="isp" title="Índice de Saúde do Parceiro (0-100). Composição: Recência 25% + Produção 25% + Volume Ajustado 20% + Consistência 15% + Tendência 10% + Valor 5%">ISP</th><th data-col="saude" title="Classificação de saúde baseada no ISP: Excelente (80-100), Bom (60-79), Regular (40-59), Ruim (20-39), Péssimo (0-19)">Saúde</th><th data-col="leads" title="Total de leads enviados pelo parceiro desde o início do registro na base">Leads</th><th data-col="sem4" title="Leads enviados nas últimas 4 semanas (período mais recente)">4Sem</th><th data-col="pagos" title="Total de processos pagos (precatórios comprados) vinculados a este parceiro">Pagos</th><th data-col="ticket" title="Ticket médio = Valor total de compras ÷ Quantidade de pagos. Indica o valor médio por precatório comprado">Ticket</th><th data-col="taxa_conv" title="Taxa de conversão = Pagos ÷ Leads × 100. Indica quantos leads se transformaram em compra efetiva">Conv.</th><th data-col="tend" title="Tendência semanal: compara leads das últimas 4 semanas vs 4 semanas anteriores. Positivo = crescendo, Negativo = caindo">Tend.</th><th data-col="vlr_dist" title="Valor Bruto total dos processos em andamento deste parceiro, excluindo MIDs (CPF ≥ R$10M ou CNPJ ≥ R$5M). Representa o potencial distribuível atual.">VLR a Distribuir</th><th data-col="churn_score" title="Score de risco de churn (0-100) calculado a partir de tendência, semanas parado, ISP, envio e sazonalidade. Alto ≥ 60, Médio 30-59, Baixo < 30">Risco</th><th title="Visualização do volume de leads enviados por semana nas últimas 12 semanas. Cada barra = 1 semana, número acima = quantidade de leads">Últimas 12 Semanas</th>
      </tr></thead>
      <tbody id="expBody"></tbody>
    </table>
  </div>
</div>

<!-- DESTAQUES DA SEMANA -->
<div class="pnl" id="p-destaques">

  <!-- WEEK SELECTOR BAR -->
  <div class="wow-week-bar">
    <label>&#128197; Semana:</label>
    <select id="wowWeekSelect" onchange="renderWoW()"></select>
    <span id="wowPartialBadge"></span>
  </div>

  <!-- SECTION A: KPI CARDS WoW -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">&#9733;</span><span class="story-label">Resumo Semanal (WoW)</span><span class="story-desc">comparativo semana atual vs anterior</span></div>
    <div class="kpis" id="wowKpis" style="grid-template-columns:repeat(5,1fr)"></div>
  </div>

  <!-- SECTION B: Top 5 AUMENTARAM -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num" style="background:var(--vd)">&#8593;</span><span class="story-label">Top 5 — Parceiros que mais AUMENTARAM envio</span></div>
    <div class="tw">
      <table id="wowUpTable">
        <thead><tr>
          <th>Rank</th><th>Nome</th><th>Categoria</th><th>Sem. Anterior</th><th>Sem. Atual</th><th>Delta</th><th>Delta %</th><th>Impacto no Total (%)</th>
        </tr></thead>
        <tbody id="wowUpBody"></tbody>
      </table>
    </div>
  </div>

  <!-- SECTION C: Top 5 CAIRAM -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num" style="background:var(--danger)">&#8595;</span><span class="story-label">Top 5 — Parceiros que mais CAIRAM</span></div>
    <div class="tw">
      <table id="wowDownTable">
        <thead><tr>
          <th>Rank</th><th>Nome</th><th>Categoria</th><th>Sem. Anterior</th><th>Sem. Atual</th><th>Delta</th><th>Delta %</th><th>Impacto no Total (%)</th>
        </tr></thead>
        <tbody id="wowDownBody"></tbody>
      </table>
    </div>
  </div>

  <!-- SECTION D: Insights Analiticos -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num">&#128161;</span><span class="story-label">Insights Analíticos</span><span class="story-desc">gerados automaticamente</span></div>
    <div class="chart-box" id="wowInsights" style="border-top:3px solid var(--az)"></div>
  </div>

  <!-- SECTION E: Perspectiva da Semana -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num" style="background:#805ad5">&#128269;</span><span class="story-label">Perspectiva da Semana</span><span class="story-desc">projeção e ações necessárias</span></div>
    <div class="chart-box" id="wowPerspectiva" style="border-top:3px solid #805ad5"></div>
  </div>

  <!-- SECTION F: Visao Regional/UF -->
  <div class="story-block">
    <div class="story-hd"><span class="story-num" style="background:#7A8599">&#127758;</span><span class="story-label">Destaques por Regional</span><span class="story-desc">variação semanal por regional</span></div>
    <div class="chart-box" id="wowRegionalSection"></div>
  </div>

</div>

<!-- GLOSSARIO -->
<div class="pnl" id="p-glossario">
  <div style="max-width:900px;margin:0 auto">
    <div class="chart-box" style="margin-bottom:20px">
      <h3 style="font-size:18px;color:var(--ae);margin-bottom:16px">Glossário da Plataforma</h3>
      <p style="font-size:12px;color:#7A8599;margin-bottom:20px">Definições dos principais conceitos, classificações e indicadores utilizados na plataforma. Consulte este glossário para entender com clareza o significado de cada termo e como ele impacta a leitura do painel.</p>

      <div style="background:#D6F1FF;border-left:4px solid #0074FF;padding:12px 16px;border-radius:8px;margin-bottom:20px">
        <p style="font-size:12px;color:#0E2F5D;margin:0;font-weight:600">Metodologia de contagem de leads</p>
        <p style="font-size:11px;color:#2B313B;margin:6px 0 0 0">A contagem de leads considera apenas registros com <strong>Varejo = "sim"</strong>. Cada linha no BD_EnvioParceiros que atende esse critério conta como 1 lead. Registros sem Varejo ou com Varejo diferente de "sim" são desconsiderados em toda a plataforma.</p>
      </div>

      <h3 style="margin-top:20px;margin-bottom:10px;font-size:14px">Categorias de Parceiro</h3>
      <div id="glossCats"></div>

      <h3 style="margin-top:24px;margin-bottom:10px;font-size:14px">ISP &mdash; Índice de Saude do Parceiro</h3>
      <div id="glossISP"></div>

      <h3 style="margin-top:24px;margin-bottom:10px;font-size:14px">Faixas de Saude</h3>
      <div id="glossSaude"></div>

      <h3 style="margin-top:24px;margin-bottom:10px;font-size:14px">Classificacao de Envio</h3>
      <div id="glossEnvio"></div>

      <h3 style="margin-top:24px;margin-bottom:10px;font-size:14px">Termos Gerais</h3>
      <div id="glossTermos"></div>

      <h3 style="margin-top:24px;margin-bottom:10px;font-size:14px">Indicadores Preditivos</h3>
      <div id="glossPreditivos"></div>

      <h3 style="margin-top:24px;margin-bottom:10px;font-size:14px">Métricas Financeiras</h3>
      <div id="glossFinanceiro"></div>
    </div>
  </div>
</div>

<!-- PLANNER -->
<div class="pnl" id="p-planner">
  <div style="max-width:1200px;margin:0 auto">
    <div class="planner-toolbar">
      <button class="btn btn-p" onclick="abrirNovaTask()">+ Nova Tarefa</button>
      <input type="text" id="plannerSearch" placeholder="&#128269; Buscar tarefa..." oninput="renderPlanner()">
      <span id="plannerCount" style="font-size:12px;color:#7A8599;margin-left:4px"></span>
      <span style="font-size:11px;color:#B0B0B0;margin-left:8px">&#128274; Dados salvos localmente | Integração PostgreSQL prevista</span>
    </div>
    <div class="kanban-board">
      <div class="kanban-col" id="col-todo" ondragover="onKanbanDragOver(event)" ondrop="onKanbanDrop(event,'todo')">
        <div class="kanban-col-hd">&#9711; A Fazer <span class="col-cnt" id="cnt-todo">0</span></div>
        <div class="kanban-dropzone" id="cards-todo"></div>
      </div>
      <div class="kanban-col" id="col-doing" ondragover="onKanbanDragOver(event)" ondrop="onKanbanDrop(event,'doing')">
        <div class="kanban-col-hd">&#9654; Em Andamento <span class="col-cnt" id="cnt-doing">0</span></div>
        <div class="kanban-dropzone" id="cards-doing"></div>
      </div>
      <div class="kanban-col" id="col-done" ondragover="onKanbanDragOver(event)" ondrop="onKanbanDrop(event,'done')">
        <div class="kanban-col-hd">&#10003; Conclu&#237;do <span class="col-cnt" id="cnt-done">0</span></div>
        <div class="kanban-dropzone" id="cards-done"></div>
      </div>
    </div>
  </div>
  <!-- Modal nova task -->
  <div id="plannerModal" class="modal-overlay" style="display:none" onclick="fecharModalTask(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <h3>&#128203; Nova Tarefa</h3>
      <div class="modal-field"><label>T&#237;tulo *</label><input type="text" id="taskTitulo" placeholder="Descreva a tarefa..."></div>
      <div class="modal-field"><label>Descri&#231;&#227;o</label><textarea id="taskDesc" placeholder="Detalhes adicionais..."></textarea></div>
      <div class="modal-field"><label>Respons&#225;vel</label><input type="text" id="taskResp" placeholder="Nome do respons&#225;vel..."></div>
      <div class="modal-field"><label>Parceiro (opcional)</label><input type="text" id="taskParceiro" placeholder="Nome do parceiro associado..."></div>
      <div class="modal-field" style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
        <div><label>Prioridade</label><select id="taskPrio"><option value="Alta">&#x1F534; Alta</option><option value="Média" selected>&#x1F7E1; M&#233;dia</option><option value="Baixa">&#x1F7E2; Baixa</option></select></div>
        <div><label>Data</label><input type="date" id="taskData"></div>
      </div>
      <div class="modal-actions">
        <button class="btn btn-o" onclick="document.getElementById(\'plannerModal\').style.display=\'none\'">Cancelar</button>
        <button class="btn btn-p" onclick="salvarTask()">Salvar Tarefa</button>
      </div>
    </div>
  </div>
</div>

<!-- CHATBOT -->
<button class="chat-btn" id="chatToggle" title="Meu parça">__AVATAR_BTN__</button>
<div class="chat-panel" id="chatPanel">
  <div class="chat-hd">
    <div class="avatar">__AVATAR__</div>
    <div class="chat-hd-info"><h3>Meu parça</h3><p>Assistente de parceiros</p></div>
    <button class="chat-close" id="chatClose">&times;</button>
  </div>
  <div class="chat-body" id="chatBody">
    <div class="chat-msg bot"><div class="bubble">E ai! Sou o <strong>Meu parça</strong>, seu assistente de parceiros. Em breve vou poder te ajudar com consultas, histórico e análises. Por enquanto, estou em fase de treinamento.</div><div class="time">agora</div></div>
  </div>
  <div class="chat-input">
    <input type="text" id="chatInput" placeholder="Digite sua mensagem...">
    <button onclick="sendChat()">Enviar</button>
  </div>
</div>

<div class="toast" id="toast"></div>
"""

# ====================================================================
# JAVASCRIPT
# ====================================================================
JS = r"""
var D=__DATA__;
var NF=D.filter(function(p){return p.cat!=='Fantasma'});
var FN=D.filter(function(p){return p.cat==='Fantasma'});
var CR=NF.filter(function(p){return p.prior==='CRITICA'||p.prior==='ALTA'}).sort(function(a,b){
  var po=['CRITICA','ALTA'];return po.indexOf(a.prior)-po.indexOf(b.prior)||(b.compra-a.compra);
});

document.getElementById('refDate').innerHTML='__HOJE__<br>Plataforma de Gestao de Parceiros';
// acaoCnt removido - aba acao nao existe mais
document.getElementById('expCnt').textContent=D.length;
// fanCnt removido - aba fantasma nao existe mais

// TABS
document.querySelectorAll('.tab').forEach(function(t){
  t.addEventListener('click',function(){
    document.querySelectorAll('.tab').forEach(function(x){x.classList.remove('active')});
    document.querySelectorAll('.pnl').forEach(function(x){x.classList.remove('active')});
    t.classList.add('active');
    document.getElementById('p-'+t.dataset.tab).classList.add('active');
  });
});

// HELPERS
var fN=function(v){return v.toLocaleString('pt-BR')};
var fB=function(v){if(Math.abs(v)>=1e6){return 'R$ '+(v/1e6).toFixed(1).replace('.',',')+'M'}else if(Math.abs(v)>=1e3){return 'R$ '+(v/1e3).toFixed(0)+'K'}else{return 'R$ '+Math.round(v)}};
var fP=function(v){return v.toFixed(1)+'%'};
var CM={Diamante:'c-dia',Ouro:'c-our',Prata:'c-pra',Bronze:'c-pip','Em Recuperação':'c-rec',Inativo:'c-ina',Fantasma:'c-fan'};
var SM={'Excelente':'s-sau','Bom':'s-bom','Regular':'s-ate','Ruim':'s-ris-s','Péssimo':'s-cri','Em Recuperação':'s-rec','N/A':'s-na'};
var PM={CRITICA:'p-cri',ALTA:'p-alt',MEDIA:'p-med',BAIXA:'p-bai',OBSERVACAO:'p-obs'};
var catBd=function(p){return '<span class="bd '+(CM[p]||'')+'">'+p+'</span>'};
var sauBd=function(p){return '<span class="bd '+(SM[p]||'')+'">'+p+'</span>'};
var priBd=function(p){return '<span class="bd '+(PM[p]||'')+'">'+p+'</span>'};
var tA=function(v){return v>10?'<span class="tend-up">+'+fP(v)+'</span>':v<-10?'<span class="tend-down">'+fP(v)+'</span>':'<span class="tend-flat">'+fP(v)+'</span>'};
function showToast(m){var t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2500)}

function buildSparkVis(p){
  var sem=p.semanas||{};
  var keys=[];
  var y=new Date().getFullYear();
  var w=getISOWeek();
  for(var i=11;i>=0;i--){
    var wk=w-i;var yr=y;
    if(wk<=0){wk+=52;yr-=1}
    keys.push(yr+'-'+(wk<10?'0':'')+wk);
  }
  var vals=keys.map(function(k){return sem[k]||0});
  var mx=Math.max.apply(null,vals);
  if(mx===0)mx=1;
  var h='<div class="spk-bar" title="Últimas 12 semanas">';
  vals.forEach(function(v){
    var barH=Math.max(2,Math.round(v/mx*26));
    var barColor=v===0?'#E2E8F0':'#0074FF';
    h+='<div class="sb"><div class="sn">'+(v>0?v:'')+'</div><div class="sv" style="height:'+barH+'px;background:'+barColor+'"></div></div>';
  });
  h+='</div>';
  return h;
}
function getISOWeek(){var d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()+3-(d.getDay()+6)%7);var w1=new Date(d.getFullYear(),0,4);return 1+Math.round(((d-w1)/864e5-3+(w1.getDay()+6)%7)/7)}

// ===== 6 CATEGORIAS =====
var C9=['Diamante','Ouro','Prata','Bronze','Em Recuperação','Inativo','Fantasma'];
var C9C={Diamante:'#0E2F5D',Ouro:'#FFD400',Prata:'#B0B0B0',Bronze:'#CD7F32','Em Recuperação':'#17A2B8',Inativo:'#2B313B',Fantasma:'#804080'};
// 8 categories for heatmap (excluding Fantasma)
var C8=C9.filter(function(c){return c!=='Fantasma'});

// ===== REGIONAL MAPPING =====
function getRegional(uf){
  var regA=['MA','PI','CE','RN','PB','PE','AL','SE','BA','AP','PA'];
  var regB=['MG','RJ','ES','GO','MT','TO','DF','AC','AM','RO','RR'];
  var regD=['PR','SC','RS','MS'];
  if(!uf)return 'N/I';
  var u=uf.toUpperCase().trim();
  if(u==='SP')return 'SP (C/D)';
  if(regA.indexOf(u)>=0)return 'Regional A';
  if(regB.indexOf(u)>=0)return 'Regional B';
  if(regD.indexOf(u)>=0)return 'Regional D';
  return 'N/I';
}
var REG_COLORS={'Regional A':'#0074FF','Regional B':'#00A68C','Regional D':'#0E2F5D','SP (C/D)':'#FFD400','N/I':'#B0B0B0'};
var REG_LIST=['SP (C/D)','Regional A','Regional B','Regional D','N/I'];
// Compute regional for each partner
D.forEach(function(p){p.regional=getRegional(p.uf||'')});

var GF=D; // dados filtrados globalmente
var TASKS=JSON.parse(localStorage.getItem('eaimeu_tasks')||'[]'); // PLANNER - definido aqui para estar disponivel no init
var semAtual=""" + str(sem_atual_num) + r""";
var anoISOAtual=""" + str(ano_iso_atual) + r""";
var diaSemanaAtual=""" + str(dia_semana_atual) + r""";
var FERIADOS=new Set(""" + feriados_json + r""");

// Metricas gerais (computed once for NF, used by chatbot/kanban)
var ativos=NF.filter(function(p){return p.sem4>0}).length;
var l4=NF.reduce(function(s,p){return s+p.sem4},0);
var tp=D.reduce(function(s,p){return s+p.pagos},0);
var tc=D.reduce(function(s,p){return s+p.compra},0);
var ispVals=NF.filter(function(p){return p.isp>=0}).map(function(p){return p.isp});
var ispMédio=ispVals.length>0?Math.round(ispVals.reduce(function(s,v){return s+v},0)/ispVals.length):0;
var saudaveis=NF.filter(function(p){return p.saude==='Excelente'||p.saude==='Bom'}).length;
var emRisco=NF.filter(function(p){return p.saude==='Ruim'||p.saude==='Péssimo'}).length;
var criticos=NF.filter(function(p){return p.prior==='CRITICA'}).length;
var topCompra=NF.slice().sort(function(a,b){return b.compra-a.compra}).slice(0,5);
var gargalos=NF.filter(function(p){return p.pagos>0&&p.tend<-30}).sort(function(a,b){return a.tend-b.tend}).slice(0,5);
var oportunidades=NF.filter(function(p){return p.tend>20&&p.sem4>0}).sort(function(a,b){return b.compra-a.compra}).slice(0,5);

// ===== BLOCO 1: PANORAMA =====
function renderKPIs(){
  var gf=GF.filter(function(p){return p.cat!=='Fantasma'});
  var _ativos=gf.filter(function(p){return p.sem4>0}).length;
  var _l4=gf.reduce(function(s,p){return s+p.sem4},0);
  var _tp=GF.reduce(function(s,p){return s+p.pagos},0);
  var _tc=GF.reduce(function(s,p){return s+p.compra},0);
  var _ispVals=gf.filter(function(p){return p.isp>=0}).map(function(p){return p.isp});
  var _ispMédio=_ispVals.length>0?Math.round(_ispVals.reduce(function(s,v){return s+v},0)/_ispVals.length):0;
  var _vlrDist=GF.reduce(function(s,p){return s+(p.vlr_dist||0)},0);
  document.getElementById('kpiGrid').innerHTML=[
    ['Base Total',fN(GF.length),'parceiros mapeados',''],
    ['Ativos (4 sem)',fN(_ativos),gf.length>0?Math.round(_ativos/gf.length*100)+'% da base':'--',''],
    ['Leads (4 sem)',fN(_l4),'enviados recentemente',''],
    ['Processos Pagos',fN(_tp),'compras realizadas','green'],
    ['R$ Compras',fB(_tc),'valor acumulado','green'],
    ['ISP Médio',_ispMédio,'indice de saude do parceiro','orange'],
    ['VLR a Distribuir',fB(_vlrDist),'em andamento (ex-MID)','purple']
  ].map(function(a){return '<div class="kpi '+a[3]+'"><div class="kpi-l">'+a[0]+'</div><div class="kpi-v">'+a[1]+'</div><div class="kpi-d">'+a[2]+'</div></div>'}).join('');

  // Highlights
  var hNovos=GF.filter(function(p){return p.is_novo}).length;
  var hRessus=GF.filter(function(p){return p.is_em_recuperacao}).length;
  var hSazon=GF.filter(function(p){return p.is_sazonal}).length;
  var hFant=GF.filter(function(p){return p.is_fantasma}).length;
  document.getElementById('highlights').innerHTML=[
    ['Novos',hNovos,'parceiros recem-chegados','','#0074FF'],
    ['Em Recuperação',hRessus,'voltaram a enviar','green','#00A68C'],
    ['Sazonais',hSazon,'padrao de envio irregular','orange','#FF8C00'],
    ['Fantasmas',hFant,'compram fora da esteira','purple','#804080']
  ].map(function(a){return '<div class="kpi" style="border-left-color:'+a[4]+'"><div class="kpi-l">'+a[0]+'</div><div class="kpi-v">'+a[1]+'</div><div class="kpi-d">'+a[2]+'</div></div>'}).join('');
}

// Panorama bar (composicao da base com 9 categorias)
function renderPanorama(){
  var pbTotal=GF.length;
  document.getElementById('panoramaBar').innerHTML=C9.map(function(c){
    var n=GF.filter(function(p){return p.cat===c}).length;
    var pct=pbTotal>0?(n/pbTotal*100):0;
    if(n===0)return '';
    return '<div class="panorama-seg" style="flex:'+n+';background:'+C9C[c]+';cursor:pointer" onclick="goToList(\''+c.replace(/\x27/g,"\\'")+'\',\'\')" data-tip="'+c+': '+n+' ('+Math.round(pct)+'%) — clique para ver">'+(pct>=5?c.substring(0,8)+' '+Math.round(pct)+'%':n)+'</div>';
  }).join('');
}

// ===== BLOCO 2: SAUDE =====
var saudes=['Excelente','Bom','Regular','Ruim','Péssimo','Em Recuperação'];
var saudeColors={'Excelente':'#38A169','Bom':'#4299E1','Regular':'#ECC94B','Ruim':'#ED8936','Péssimo':'#E53E3E','Em Recuperação':'#00796B'};

function renderSaude(){
  var gf=GF.filter(function(p){return p.cat!=='Fantasma'});
  var saudeCounts=saudes.map(function(s){return {s:s,n:gf.filter(function(p){return p.saude===s}).length}});
  var smx=Math.max.apply(null,saudeCounts.map(function(x){return x.n}).concat([1]));

  document.getElementById('saudeChart').innerHTML='<div class="saude-meter">'+saudeCounts.map(function(o){
    var w=Math.max(5,Math.round(o.n/smx*100));
    var pct=gf.length>0?Math.round(o.n/gf.length*100):0;
    return '<div class="saude-bar-row" style="cursor:pointer" onclick="goToList(\'\',\''+o.s.replace(/\x27/g,"\\'")+'\')" title="Clique para ver parceiros '+o.s+'"><div class="saude-lbl">'+o.s+'</div><div style="flex:1"><div class="saude-bar" style="width:'+w+'%;background:'+saudeColors[o.s]+'">'+o.n+' ('+pct+'%)</div></div></div>';
  }).join('')+'</div>';

  // Bubble matrix (cat x saude, excluding Fantasma)
  var bData={};
  C8.forEach(function(c){saudes.forEach(function(s){
    bData[c+'|'+s]=gf.filter(function(p){return p.cat===c&&p.saude===s}).length;
  })});
  var bmx=Math.max.apply(null,Object.values(bData).concat([1]));
  var gh='<div class="hc"></div>';
  C8.forEach(function(c){gh+='<div class="hc">'+c.substring(0,10)+'</div>'});
  saudes.forEach(function(s){
    gh+='<div class="rl">'+s+'</div>';
    C8.forEach(function(c){
      var n=bData[c+'|'+s]||0;
      if(n>0){
        var sz=Math.max(22,Math.min(54,Math.round(22+n/bmx*32)));
        gh+='<div class="cell"><div class="bub" style="width:'+sz+'px;height:'+sz+'px;background:'+saudeColors[s]+';cursor:pointer" onclick="goToList(\''+c.replace(/'/g,"\\'")+'\',\''+s.replace(/'/g,"\\'")+'\')">'+n+'<div class="bub-tip">'+c+' | '+s+': '+n+' — clique para ver</div></div></div>';
      } else gh+='<div class="cell"></div>';
    });
  });
  var grid=document.getElementById('bubGrid');
  grid.innerHTML=gh;
  grid.style.gridTemplateColumns='80px repeat('+C8.length+',1fr)';
  grid.style.display='grid';
}

// ===== BLOCO 3: PRODUCAO =====
function renderProd(){
  var prodData=C9.map(function(c){
    var ps=GF.filter(function(p){return p.cat===c});
    return {c:c,n:ps.length,leads:ps.reduce(function(s,p){return s+p.leads},0),s4:ps.reduce(function(s,p){return s+p.sem4},0),pagos:ps.reduce(function(s,p){return s+p.pagos},0),compra:ps.reduce(function(s,p){return s+p.compra},0)};
  });
  document.getElementById('prodChart').innerHTML='<table class="prod-table"><thead><tr><th>Categoria</th><th>Qtd</th><th>Leads Total</th><th>Leads 4sem</th><th>Pagos</th><th>R$ Compra</th><th>Ticket</th></tr></thead><tbody>'+prodData.map(function(o){
    var ticket=o.pagos>0?fB(Math.round(o.compra/o.pagos)):'--';
    return '<tr><td><span class="prod-badge" style="background:'+C9C[o.c]+';cursor:pointer" onclick="goToList(\''+o.c.replace(/'/g,"\\'")+'\',\'\')">'+o.c+'</span></td><td>'+o.n+'</td><td>'+fN(o.leads)+'</td><td>'+fN(o.s4)+'</td><td>'+fN(o.pagos)+'</td><td>'+fB(o.compra)+'</td><td>'+ticket+'</td></tr>';
  }).join('')+'</tbody></table>';

  // Ranking top 5
  var gf=GF.filter(function(p){return p.cat!=='Fantasma'});
  var _topCompra=gf.slice().sort(function(a,b){return b.compra-a.compra}).slice(0,5);
  document.getElementById('rankTop').innerHTML=_topCompra.map(function(p,i){
    var cls=i===0?'g':i===1?'s':i===2?'b':'d';
    return '<div class="rank-item"><div class="rank-pos '+cls+'">'+(i+1)+'</div><div class="rank-name">'+p.nome+'</div><div class="rank-val">'+fB(p.compra)+'</div></div>';
  }).join('');

  // Ticket medio por categoria
  var ticketData=C9.filter(function(c){return prodData.find(function(o){return o.c===c}).pagos>0}).map(function(c){
    var o=prodData.find(function(x){return x.c===c});
    return {c:c,t:Math.round(o.compra/o.pagos)};
  });
  var tmx=Math.max.apply(null,ticketData.map(function(x){return x.t}).concat([1]));
  document.getElementById('ticketChart').innerHTML=ticketData.map(function(o){
    var w=Math.max(8,Math.round(o.t/tmx*100));
    return '<div class="cb-row"><div class="cb-lbl" style="width:90px;font-size:10px">'+o.c.substring(0,12)+'</div><div class="cb-trk"><div class="cb-fill" style="width:'+w+'%;background:'+C9C[o.c]+'">'+fB(o.t)+'</div></div></div>';
  }).join('');
}

// ===== BLOCO 4: EVOLUCAO COM DRILLDOWN (mensal/semanal x categoria) =====
var levels=['\u2581','\u2582','\u2583','\u2584','\u2585','\u2586','\u2587','\u2588'];
var MONTH_NAMES=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];

// Helper: generate all YYYY-WW keys between two dates (or default last 12 weeks)
function getWeekKeysForRange(dateFrom,dateTo){
  var keys=[];
  var now=new Date();
  var curYear=now.getFullYear();
  // getISOWeek helper
  function isoWeek(d){var t=new Date(d.getTime());t.setDate(t.getDate()+3-(t.getDay()+6)%7);var w1=new Date(t.getFullYear(),0,4);return 1+Math.round(((t-w1)/864e5-3+(w1.getDay()+6)%7)/7)}
  function isoYear(d){var t=new Date(d.getTime());t.setDate(t.getDate()+3-(t.getDay()+6)%7);return t.getFullYear()}
  // Monday of ISO week
  function mondayOfWeek(y,w){var jan4=new Date(y,0,4);var dow=jan4.getDay()||7;var mon=new Date(jan4.getTime()+(1-dow)*864e5+(w-1)*7*864e5);return mon}
  if(dateFrom&&dateTo){
    var dFrom=new Date(dateFrom+'T00:00:00');
    var dTo=new Date(dateTo+'T00:00:00');
    var cursor=new Date(dFrom.getTime());
    // rewind cursor to Monday
    var dayOff=(cursor.getDay()+6)%7;
    cursor.setDate(cursor.getDate()-dayOff);
    while(cursor<=dTo){
      var iy=isoYear(cursor);
      var iw=isoWeek(cursor);
      var key=iy+'-'+(iw<10?'0':'')+iw;
      keys.push(key);
      cursor.setDate(cursor.getDate()+7);
    }
  } else {
    // Default: last 12 weeks
    for(var w=semAtual-11;w<=semAtual;w++){
      var wy=w>0?w:w+52;
      var ya=w>0?curYear:curYear-1;
      keys.push(ya+'-'+(wy<10?'0':'')+wy);
    }
  }
  return keys;
}

// Helper: group week keys by month, return [{label,keys}]
function groupWeeksByMonth(weekKeys){
  function mondayOfKey(key){var parts=key.split('-');var y=parseInt(parts[0]);var w=parseInt(parts[1]);var jan4=new Date(y,0,4);var dow=jan4.getDay()||7;return new Date(jan4.getTime()+(1-dow)*864e5+(w-1)*7*864e5)}
  var groups=[];
  var curLabel='';
  var fromStr=document.getElementById('gfDateFrom').value;
  var toStr=document.getElementById('gfDateTo').value;
  var fromMonth=fromStr?parseInt(fromStr.split('-')[1])-1:-1;
  var fromYear=fromStr?parseInt(fromStr.split('-')[0]):-1;
  weekKeys.forEach(function(key){
    var mon=mondayOfKey(key);
    var lbl=MONTH_NAMES[mon.getMonth()]+'/'+mon.getFullYear().toString().substring(2);
    if(fromYear>0&&(mon.getFullYear()<fromYear||(mon.getFullYear()===fromYear&&mon.getMonth()<fromMonth)))return;
    if(lbl!==curLabel){groups.push({label:lbl,keys:[]});curLabel=lbl}
    groups[groups.length-1].keys.push(key);
  });
  return groups;
}

// Get leads count for a partner in a given week key from semanas object
function pLeadsInWeek(p,key){
  if(p.semanas)return p.semanas[key]||0;
  return 0;
}

var evoView='mensal';

function setEvoView(view){
  evoView=view;
  document.querySelectorAll('.evo-btn').forEach(function(b){b.classList.remove('active');b.classList.remove('btn-p');b.classList.add('btn-o')});
  var btn=document.querySelector('.evo-btn[data-view="'+view+'"]');
  if(btn){btn.classList.add('active');btn.classList.add('btn-p');btn.classList.remove('btn-o')}
  renderEvo();
}

function renderEvo(){
  var gf=GF.filter(function(p){return p.cat!=='Fantasma'});

  // Determine week keys from date filter
  var dateFrom=document.getElementById('gfDateFrom').value;
  var dateTo=document.getElementById('gfDateTo').value;
  var weekKeys=getWeekKeysForRange(dateFrom,dateTo);
  var monthGroups=groupWeeksByMonth(weekKeys);

  // Check if semanas data is available (new format)
  var hasSemanas=gf.length>0&&gf[0].semanas!==undefined;

  // Compute leads per week per category from semanas data
  var evoWeekData={};
  C8.forEach(function(c){
    evoWeekData[c]=new Array(weekKeys.length).fill(0);
    gf.filter(function(p){return p.cat===c}).forEach(function(p){
      if(hasSemanas&&p.semanas){
        weekKeys.forEach(function(key,i){evoWeekData[c][i]+=(p.semanas[key]||0)});
      } else if(p.spark){
        // Fallback: sparkline only covers last 12 weeks
        var chars=p.spark.split(' ').filter(function(x){return x.length>0});
        var offset=weekKeys.length-12;
        chars.forEach(function(ch,ci){
          var idx=ci+offset;
          if(idx>=0&&idx<weekKeys.length){var lvl=levels.indexOf(ch);evoWeekData[c][idx]+=Math.max(lvl,0)}
        });
      }
    });
  });

  // Compute monthly aggregation
  var evoMonthData={};
  var monthLabels=monthGroups.map(function(g){return g.label});
  C8.forEach(function(c){
    evoMonthData[c]=monthGroups.map(function(g){
      var sum=0;
      g.keys.forEach(function(key){
        var wi=weekKeys.indexOf(key);
        if(wi>=0)sum+=evoWeekData[c][wi]||0;
      });
      return sum;
    });
  });

  // Build weekly labels
  var weekLabels=weekKeys.map(function(k){var parts=k.split('-');return 'S'+parseInt(parts[1])});

  var catFilter=document.getElementById('evoCatFilter').value;
  var cats=catFilter?[catFilter]:C8;
  var isMonth=evoView==='mensal';
  var cols=isMonth?monthLabels:weekLabels;
  var data=isMonth?evoMonthData:evoWeekData;

  // Find max for color scaling
  var mx=1;
  cats.forEach(function(c){
    var arr=data[c]||[];
    arr.forEach(function(v){if(v>mx)mx=v});
  });

  var ncols=cols.length;
  var html='<div class="evo-grid" style="grid-template-columns:120px repeat('+ncols+',1fr);display:grid">';

  // Header
  html+='<div class="evo-hd"></div>';
  cols.forEach(function(w){html+='<div class="evo-hd">'+w+'</div>'});

  // Totals row
  html+='<div class="evo-lbl" style="font-weight:700;font-size:11px">TOTAL</div>';
  var totals=new Array(ncols).fill(0);
  cats.forEach(function(c){
    var arr=data[c]||[];
    for(var i=0;i<ncols;i++)totals[i]+=(arr[i]||0);
  });
  var tmx=Math.max.apply(null,totals.concat([1]));
  totals.forEach(function(v,i){
    var pct=v/tmx;
    var bg=pct<.05?'#F0F4F8':pct<.3?'#D6F1FF':pct<.6?'var(--az)':'var(--ae)';
    var fc=pct>.4?'#fff':'#333';
    html+='<div class="evo-cell" style="background:'+bg+';color:'+fc+';font-weight:700" data-tip="Total '+cols[i]+': '+v+'">'+v+'</div>';
  });

  // Category rows
  cats.forEach(function(c){
    html+='<div class="evo-lbl"><span class="prod-badge" style="background:'+C9C[c]+';font-size:9px;cursor:pointer" onclick="goToList(\''+c.replace(/\x27/g,"\\'")+'\',\'\')">'+c.substring(0,12)+'</span></div>';
    var arr=data[c]||[];
    for(var i=0;i<ncols;i++){
      var v=arr[i]||0;
      var intensity=v/mx;
      var r,g,b;
      if(intensity<=.6){r=Math.round(230-intensity*190);g=Math.round(240-intensity*160);b=Math.round(250-intensity*100)}
      else{r=Math.round(14+intensity*20);g=Math.round(47+intensity*30);b=Math.round(93+intensity*50)}
      var color=intensity<.05?'#F0F4F8':'rgb('+r+','+g+','+b+')';
      var fc=intensity>.5?'#fff':'#555';
      html+='<div class="evo-cell" style="background:'+color+';color:'+fc+'" data-tip="'+c+' '+cols[i]+': '+v+'">'+(v>0?v:'')+'</div>';
    }
  });

  // Variação row (delta entre periodos)
  if(ncols>=2){
    html+='<div class="evo-lbl" style="font-size:10px;font-style:italic;color:#7A8599">Variação</div>';
    for(var i=0;i<ncols;i++){
      if(i===0){html+='<div class="evo-cell" style="font-size:9px;color:#7A8599">--</div>';continue}
      var delta=totals[i]-totals[i-1];
      var pct=totals[i-1]>0?Math.round(delta/totals[i-1]*100):0;
      var cls=delta>0?'tend-up':delta<0?'tend-down':'tend-flat';
      var sign=delta>0?'+':'';
      html+='<div class="evo-cell" style="font-size:9px"><span class="'+cls+'">'+sign+delta+' ('+sign+pct+'%)</span></div>';
    }
  }

  html+='</div>';
  document.getElementById('evoChart').innerHTML=html;

  // Render historical mini-charts
  renderEvoHist(weekKeys,monthGroups,gf);
  // Render regional heatmap
  renderEvoRegional(weekKeys,monthGroups,gf);
}

// ===== EVOLUCAO POR REGIONAL (heatmap igual ao de categoria) =====
function renderEvoRegional(weekKeys,monthGroups,gf){
  var nf=gf.filter(function(p){return p.cat!=='Fantasma'});
  var regs=['Regional A','Regional B','Regional D','SP (C/D)','N/I'];
  var regC={'Regional A':'#0074FF','Regional B':'#00A68C','Regional D':'#0E2F5D','SP (C/D)':'#FFD400','N/I':'#B0B0B0'};
  var isMonthly=evoView==='mensal';
  var periods=isMonthly?monthGroups.map(function(m){return m}):weekKeys.map(function(k){var pts=k.split('-');return {label:'S'+pts[1],keys:[k]}});

  // Compute data per regional per period
  var data={};
  regs.forEach(function(reg){data[reg]=[]});
  var totals=[];

  periods.forEach(function(period){
    var pkeys=period.keys||[period];
    var total=0;
    regs.forEach(function(reg){
      var cnt=0;
      nf.forEach(function(p){
        if(p.regional!==reg)return;
        var sem=p.semanas||{};
        pkeys.forEach(function(k){cnt+=(sem[k]||0)});
      });
      data[reg].push(cnt);
      total+=cnt;
    });
    totals.push(total);
  });

  var maxVal=Math.max.apply(null,totals.concat([1]));

  var html='<div style="overflow-x:auto"><table class="prod-table" style="min-width:600px;font-size:11px">';
  html+='<thead><tr><th style="min-width:100px"></th>';
  periods.forEach(function(p){html+='<th style="text-align:center;font-size:10px">'+p.label+'</th>'});
  html+='</tr></thead><tbody>';

  // Total row
  html+='<tr style="font-weight:700;background:#F0F4F8"><td style="font-weight:700">TOTAL</td>';
  totals.forEach(function(v){
    var op=Math.max(0.15,v/maxVal);
    html+='<td style="text-align:center;background:rgba(14,47,93,'+op+');color:'+(op>0.5?'#fff':'#0E2F5D')+';font-weight:700">'+v+'</td>';
  });
  html+='</tr>';

  // Regional rows
  regs.forEach(function(reg){
    var vals=data[reg];
    var hasData=vals.some(function(v){return v>0});
    if(!hasData)return;
    var regMax=Math.max.apply(null,vals.concat([1]));
    html+='<tr><td><span class="prod-badge" style="background:'+regC[reg]+';color:'+(reg==='SP (C/D)'||reg==='N/I'?'#333':'#fff')+'">'+reg+'</span></td>';
    vals.forEach(function(v){
      var op=v>0?Math.max(0.1,v/regMax):0;
      html+='<td style="text-align:center;background:rgba(14,47,93,'+op+');color:'+(op>0.4?'#fff':'#2B313B')+'">'+v+'</td>';
    });
    html+='</tr>';
  });

  // Variation row
  html+='<tr style="font-style:italic;font-size:10px;color:#7A8599"><td style="font-style:italic">Variação</td>';
  for(var i=0;i<totals.length;i++){
    if(i===0){html+='<td style="text-align:center">--</td>';continue}
    var prev=totals[i-1];var cur=totals[i];var delta=cur-prev;
    var pct=prev>0?Math.round(delta/prev*100):cur>0?100:0;
    var cls=delta>0?'color:#00A68C':delta<0?'color:#E53E3E':'';
    html+='<td style="text-align:center;'+cls+'">'+(delta>0?'+':'')+delta+' ('+(pct>0?'+':'')+pct+'%)</td>';
  }
  html+='</tr>';

  html+='</tbody></table></div>';
  document.getElementById('evoRegChart').innerHTML=html;
}

// ===== EVOLUCAO HISTORICA (ISP medio + % ativos + leads por mes/semana) =====
var evoHistView='mensal';
function setEvoHistView(v){evoHistView=v;renderEvo()}

function renderEvoHist(weekKeys,monthGroups,gf){
  var hasSemanas=gf.length>0&&gf[0].semanas!==undefined;

  if(evoHistView==='semanal'){
    // Weekly view: show each week in the range
    var wLabels=weekKeys.map(function(k){var parts=k.split('-');return 'S'+parseInt(parts[1])});

    var ispPerWeek=new Array(weekKeys.length).fill(0);
    var ispCountWeek=new Array(weekKeys.length).fill(0);
    var ativosPerWeek=new Array(weekKeys.length).fill(0);
    var leadsPerWeek=new Array(weekKeys.length).fill(0);

    gf.forEach(function(p){
      if(hasSemanas&&p.semanas){
        weekKeys.forEach(function(key,wi){
          var cnt=p.semanas[key]||0;
          if(cnt>0){
            ativosPerWeek[wi]++;
            leadsPerWeek[wi]+=cnt;
            if(p.isp>=0){ispPerWeek[wi]+=p.isp;ispCountWeek[wi]++}
          }
        });
      } else if(p.spark){
        // Fallback to sparkline for last 12 weeks
        var sparkLevels=['\u2581','\u2582','\u2584','\u2586','\u2588'];
        var chars=p.spark.split(' ').filter(function(x){return x.length>0});
        var offset=weekKeys.length-12;
        for(var w=0;w<12;w++){
          var idx=w+offset;
          if(idx>=0&&idx<weekKeys.length&&w<chars.length){
            var lvl=sparkLevels.indexOf(chars[w]);
            var leadsEst=lvl<=0?0:lvl===1?1:lvl===2?4:lvl===3?8:15;
            if(lvl>0){
              ativosPerWeek[idx]++;
              leadsPerWeek[idx]+=leadsEst;
              if(p.isp>=0){ispPerWeek[idx]+=p.isp;ispCountWeek[idx]++}
            }
          }
        }
      }
    });

    var ispAvgWeek=ispPerWeek.map(function(v,i){return ispCountWeek[i]>0?Math.round(v/ispCountWeek[i]):0});
    var pctAtivosWeek=ativosPerWeek.map(function(v){return gf.length>0?Math.round(v/gf.length*100):0});
    var leadsPerParcWeek=leadsPerWeek.map(function(v,i){return ativosPerWeek[i]>0?(v/ativosPerWeek[i]).toFixed(1):'0'});

    renderHistCards(wLabels,ispAvgWeek,pctAtivosWeek,leadsPerWeek,leadsPerParcWeek,'semanal');
  } else {
    // Monthly view: group by month
    var mLabels=monthGroups.map(function(g){return g.label});

    var leadsPerMonth=new Array(monthGroups.length).fill(0);
    var ispPerMonth=new Array(monthGroups.length).fill(0);
    var ispCountMonth=new Array(monthGroups.length).fill(0);
    var ativosPerMonth=new Array(monthGroups.length).fill(0);

    monthGroups.forEach(function(g,mi){
      gf.forEach(function(p){
        var hasActivity=false;
        var totalLeads=0;
        if(hasSemanas&&p.semanas){
          g.keys.forEach(function(key){
            var cnt=p.semanas[key]||0;
            if(cnt>0){hasActivity=true;totalLeads+=cnt}
          });
        } else if(p.spark){
          var sparkLevels=['\u2581','\u2582','\u2584','\u2586','\u2588'];
          var chars=p.spark.split(' ').filter(function(x){return x.length>0});
          g.keys.forEach(function(key){
            var wi=weekKeys.indexOf(key);
            var offset=weekKeys.length-12;
            var ci=wi-offset;
            if(ci>=0&&ci<chars.length){
              var lvl=sparkLevels.indexOf(chars[ci]);
              if(lvl>0){hasActivity=true;totalLeads+=lvl<=0?0:lvl===1?1:lvl===2?4:lvl===3?8:15}
            }
          });
        }
        leadsPerMonth[mi]+=totalLeads;
        if(hasActivity){
          ativosPerMonth[mi]++;
          if(p.isp>=0){ispPerMonth[mi]+=p.isp;ispCountMonth[mi]++}
        }
      });
    });

    var ispAvgMonth=ispPerMonth.map(function(v,i){return ispCountMonth[i]>0?Math.round(v/ispCountMonth[i]):0});
    var pctAtivosPerMonth=mLabels.map(function(m,i){return gf.length>0?Math.round(ativosPerMonth[i]/gf.length*100):0});
    var leadsPerParcMonth=leadsPerMonth.map(function(v,i){return ativosPerMonth[i]>0?(v/ativosPerMonth[i]).toFixed(1):'0'});

    renderHistCards(mLabels,ispAvgMonth,pctAtivosPerMonth,leadsPerMonth,leadsPerParcMonth,'mensal');
  }
}

function renderHistCards(labels,ispArr,pctArr,leadsArr,leadsPerParcArr,activeView){
  function miniBar(label,values,unit,color,labels2){
    var mx=Math.max.apply(null,values.map(function(v){return parseFloat(v)}).concat([1]));
    var isCompact=labels2.length>6;
    var maxH=60;
    var h='<div style="flex:1;background:#fff;border-radius:8px;padding:14px '+(isCompact?'10px':'16px')+';box-shadow:0 1px 4px rgba(0,0,0,.06)">';
    h+='<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#7A8599;margin-bottom:8px">'+label+'</div>';
    h+='<div style="display:flex;align-items:flex-end;gap:'+(isCompact?'2px':'6px')+';height:'+maxH+'px">';
    labels2.forEach(function(lbl,i){
      var v=parseFloat(values[i])||0;
      var barH=mx>0?Math.max(3,Math.round(v/mx*maxH)):3;
      h+='<div style="flex:1;text-align:center;display:flex;flex-direction:column;justify-content:flex-end;height:100%">';
      h+='<div style="font-size:'+(isCompact?'8px':'11px')+';font-weight:700;color:'+color+';margin-bottom:2px">'+values[i]+unit+'</div>';
      h+='<div style="height:'+barH+'px;background:'+color+';border-radius:3px 3px 0 0;margin:0 auto;width:'+(isCompact?'80%':'65%')+';opacity:.85"></div>';
      h+='<div style="font-size:'+(isCompact?'7px':'9px')+';color:#7A8599;margin-top:3px">'+lbl+'</div>';
      h+='</div>';
    });
    h+='</div></div>';
    return h;
  }

  var toggleH='<div style="display:flex;gap:6px;margin-bottom:10px;align-items:center">';
  toggleH+='<span style="font-size:10px;font-weight:600;color:#7A8599;text-transform:uppercase;letter-spacing:.5px">Visao:</span>';
  toggleH+='<button onclick="setEvoHistView(\'mensal\')" style="padding:3px 10px;border-radius:4px;border:1px solid var(--az);font-size:10px;cursor:pointer;background:'+(activeView==='mensal'?'var(--az)':'#fff')+';color:'+(activeView==='mensal'?'#fff':'var(--az)')+'">Mensal</button>';
  toggleH+='<button onclick="setEvoHistView(\'semanal\')" style="padding:3px 10px;border-radius:4px;border:1px solid var(--az);font-size:10px;cursor:pointer;background:'+(activeView==='semanal'?'var(--az)':'#fff')+';color:'+(activeView==='semanal'?'#fff':'var(--az)')+'">Semanal</button>';
  toggleH+='</div>';

  var out=toggleH;
  out+='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">';
  out+=miniBar('ISP Médio',ispArr,'','var(--az)',labels);
  out+=miniBar('% Parceiros Ativos',pctArr,'%','var(--vd)',labels);
  out+=miniBar('Total Leads',leadsArr,'','var(--ae)',labels);
  out+=miniBar('Leads por Parceiro',leadsPerParcArr,'','#8B5CF6',labels);
  out+='</div>';
  document.getElementById('evoHist').innerHTML=out;
}

// ===== BLOCO 5: GARGALOS E OPORTUNIDADES =====
function renderGG(){
  var gf=GF.filter(function(p){return p.cat!=='Fantasma'});
  var _gargalos=gf.filter(function(p){return p.pagos>0&&p.tend<-30}).sort(function(a,b){return a.tend-b.tend}).slice(0,3);
  var _oportunidades=gf.filter(function(p){return p.tend>20&&p.sem4>0}).sort(function(a,b){return b.compra-a.compra}).slice(0,3);

  function ggCard(p,tipo){
    var cor=tipo==='gargalo'?'var(--danger)':'var(--vd)';
    var icon=tipo==='gargalo'?'&#9888;':'&#9650;';
    var badge=CM[p.cat]||'';
    var sauBadge=SM[p.saude]||'';
    var semParado=p.semanas_parado||0;
    var detail='';
    if(tipo==='gargalo'){
      detail=p.pagos+' pagos | '+fB(p.compra)+' em compras';
      if(semParado>0)detail+=' | Parado h\u00e1 '+semParado+' sem';
      if(p.tend<-50)detail+=' | Queda severa de '+Math.abs(Math.round(p.tend))+'%';
      else detail+=' | Queda de '+Math.abs(Math.round(p.tend))+'%';
    } else {
      detail=p.sem4+' leads (4sem) | Tend\u00eancia +'+Math.round(p.tend)+'%';
      if(p.pagos>0)detail+=' | '+p.pagos+' pagos ('+fB(p.compra)+')';
      else detail+=' | Sem compra ainda \u2014 potencial';
    }
    return '<div class="gg-card" style="border-left:3px solid '+cor+';background:#fff;border-radius:8px;padding:10px 14px;margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,.06);cursor:pointer" onclick="goToPartner(\''+p.nome.replace(/\x27/g,"\\'").substring(0,30)+'\')">'
      +'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'
      +'<strong style="font-size:12px;color:var(--ce)">'+icon+' '+p.nome.substring(0,35)+'</strong>'
      +'<span style="font-size:10px;font-weight:700;color:'+cor+'">'+fP(p.tend)+'</span>'
      +'</div>'
      +'<div style="display:flex;gap:6px;align-items:center;margin-bottom:4px">'
      +'<span class="bd '+badge+'" style="font-size:9px">'+p.cat+'</span>'
      +'<span class="bd '+sauBadge+'" style="font-size:9px">'+p.saude+'</span>'
      +'<span style="font-size:10px;color:#7A8599">ISP '+p.isp+'</span>'
      +'</div>'
      +'<div style="font-size:11px;color:#7A8599;line-height:1.4">'+detail+'</div>'
      +'</div>';
  }

  document.getElementById('gargalos').innerHTML=_gargalos.length===0?'<div style="color:#7A8599;font-size:12px;padding:8px">Nenhum gargalo identificado</div>':_gargalos.map(function(p){return ggCard(p,'gargalo')}).join('');

  document.getElementById('ganhos').innerHTML=_oportunidades.length===0?'<div style="color:#7A8599;font-size:12px;padding:8px">Nenhuma oportunidade destacada</div>':_oportunidades.map(function(p){return ggCard(p,'oportunidade')}).join('');
}

// ===== BLOCO 6: PROPOSTAS DE ACAO =====
function renderConclusão(){
  // --- ACAO 1: Reativar Diamante em queda ---
  var topQueda=GF.filter(function(p){return p.cat==='Diamante'&&p.tend<-30&&p.pagos>0});
  topQueda.sort(function(a,b){return b.compra-a.compra});
  var valQueda=topQueda.reduce(function(s,p){return s+p.compra},0);
  var topQuedaNomes=topQueda.slice(0,3).map(function(p){return p.nome.substring(0,30)+' ('+fB(p.compra)+')'}).join(', ');
  var ticketMedQueda=topQueda.length>0?Math.round(valQueda/topQueda.reduce(function(s,p){return s+p.pagos},0)):0;
  var ganhoQueda=topQueda.length>0?Math.round(topQueda.length*0.5*ticketMedQueda):0;

  // --- ACAO 2: Converter Bronze alto volume ---
  var pipeAlto=GF.filter(function(p){return p.cat==='Bronze'&&p.leads>=10&&p.sem4>0});
  pipeAlto.sort(function(a,b){return b.leads-a.leads});
  var leadsTotal=pipeAlto.reduce(function(s,p){return s+p.leads},0);
  var ticketGeral=0;var pgTotal=0;var compTotal=0;
  GF.forEach(function(p){if(p.pagos>0){pgTotal+=p.pagos;compTotal+=p.compra}});
  if(pgTotal>0)ticketGeral=Math.round(compTotal/pgTotal);
  var ganhoPipe=Math.round(leadsTotal*0.10*ticketGeral);
  var pipeNomes=pipeAlto.slice(0,3).map(function(p){return p.nome.substring(0,30)+' ('+p.leads+' leads)'}).join(', ');

  // --- ACAO 3: Trazer Fantasmas para esteira ---
  var fant=GF.filter(function(p){return p.cat==='Fantasma'&&p.pagos>=2});
  fant.sort(function(a,b){return b.compra-a.compra});
  var valFant=fant.reduce(function(s,p){return s+p.compra},0);
  var fantNomes=fant.slice(0,3).map(function(p){return p.nome.substring(0,30)+' ('+fB(p.compra)+')'}).join(', ');

  var acoes=[
    {
      num:'1',
      titulo:'Reativar parceiros estratégicos em queda',
      cor:'var(--danger)',
      icone:'\u26A0\uFE0F',
      gargalo:'<strong>'+topQueda.length+' parceiros Diamante</strong> apresentam queda superior a 30% no envio de leads. Juntos, concentram <strong>'+fB(valQueda)+'</strong> em compras históricas e ticket médio de <strong>'+fB(ticketMedQueda)+'</strong>.',
      nomes:topQuedaNomes||'Nenhum no filtro atual',
      acao:'Contato direto em até 48h com os 5 maiores. Reunião consultiva para entender causa da queda (concorrência, insatisfação, mudança operacional). Propor plano de retomada com acompanhamento semanal.',
      ganho:'<strong>'+fB(ganhoQueda)+'</strong> em potencial de retenção (estimativa: 50% reativação ao ticket médio)',
      prazo:'Imediato — primeiras ações em 48h, resultado esperado em 4-6 semanas'
    },
    {
      num:'2',
      titulo:'Converter Bronze de alto volume em compradores',
      cor:'var(--vd)',
      icone:'\uD83C\uDFAF',
      gargalo:'<strong>'+pipeAlto.length+' parceiros no Bronze</strong> enviam leads ativamente (10+ leads) mas nunca converteram. Acumulam <strong>'+fN(leadsTotal)+' leads</strong> sem nenhum processo pago.',
      nomes:pipeNomes||'Nenhum no filtro atual',
      acao:'Auditar qualidade dos últimos 10 leads de cada parceiro. Identificar se o perfil de envio é compatível com os critérios de compra. Reunião com os 5 maiores para alinhar expectativas e apresentar critérios de aprovação.',
      ganho:'<strong>'+fB(ganhoPipe)+'</strong> em potencial de conversão (estimativa: 10% dos leads ao ticket médio de '+fB(ticketGeral)+')',
      prazo:'Curto prazo — auditoria em 2 semanas, primeiras conversões em 30-60 dias'
    },
    {
      num:'3',
      titulo:'Integrar Fantasmas à esteira oficial',
      cor:'#804080',
      icone:'\uD83D\uDC7B',
      gargalo:'<strong>'+fant.length+' parceiros Fantasma</strong> compram precatórios ('+fB(valFant)+' acumulados) mas não enviam leads pela esteira. Operação invisível, sem rastreabilidade nem controle de funil.',
      nomes:fantNomes||'Nenhum no filtro atual',
      acao:'Mapear os 10 maiores por valor. Contato para entender o canal atual de envio. Oferecer onboarding na esteira com suporte dedicado. Monitorar adesão por 4 semanas.',
      ganho:'<strong>'+fB(valFant)+'</strong> em valor já existente que passaria a ser rastreável. Ganho indireto: visibilidade do funil, previsibilidade e controle operacional.',
      prazo:'Médio prazo — onboarding em 2-4 semanas, adesão completa em 60-90 dias'
    }
  ];

  var html='<div style="display:grid;gap:16px">';
  acoes.forEach(function(a){
    html+='<div style="background:#fff;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06);border-left:5px solid '+a.cor+'">';
    html+='<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px"><span style="font-size:20px">'+a.icone+'</span><span style="font-size:15px;font-weight:700;color:var(--ae)">Ação '+a.num+': '+a.titulo+'</span></div>';
    html+='<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">';
    html+='<div style="background:#FFF5F5;padding:10px 14px;border-radius:8px"><div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--danger);margin-bottom:4px">Gargalo identificado</div><div style="font-size:12px;line-height:1.5">'+a.gargalo+'</div></div>';
    html+='<div style="background:#F0FFF4;padding:10px 14px;border-radius:8px"><div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--vd);margin-bottom:4px">Ganho esperado</div><div style="font-size:12px;line-height:1.5">'+a.ganho+'</div></div>';
    html+='<div style="background:#F7FAFC;padding:10px 14px;border-radius:8px"><div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--az);margin-bottom:4px">Ação recomendada</div><div style="font-size:12px;line-height:1.5">'+a.acao+'</div></div>';
    html+='<div style="background:#F7FAFC;padding:10px 14px;border-radius:8px"><div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:#7A8599;margin-bottom:4px">Prazo e horizonte</div><div style="font-size:12px;line-height:1.5">'+a.prazo+'</div></div>';
    html+='</div>';
    html+='<div style="margin-top:8px;font-size:11px;color:#7A8599"><strong>Parceiros prioritários:</strong> '+a.nomes+'</div>';
    html+='</div>';
  });
  html+='</div>';
  document.getElementById('conclusao').innerHTML=html;
}

// ===== DESTAQUES DA SEMANA (WoW) =====
function getWeekKey(yr, wk) {
  if (wk <= 0) { wk += 52; yr -= 1; }
  return yr + '-' + (wk < 10 ? '0' : '') + wk;
}

// Retorna a segunda-feira ISO de uma dada semana ISO (year, week)
function getMondayOfWeek(year, week){
  // ISO week 1 contém sempre 4 de janeiro
  var jan4 = new Date(year, 0, 4);
  var dow4 = jan4.getDay() || 7; // 1=Seg…7=Dom
  var monday1 = new Date(jan4);
  monday1.setDate(jan4.getDate() - dow4 + 1);
  var monday = new Date(monday1);
  monday.setDate(monday1.getDate() + (week - 1) * 7);
  monday.setHours(0,0,0,0);
  return monday;
}

// Formata Date como 'YYYY-MM-DD'
function toISODate(d){
  return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2);
}

// Retorna {decorridos, total} de dias úteis da semana (excluindo feriados)
// decorridos = dias úteis de Seg até hoje (inclusive)
// total      = dias úteis da semana inteira
function getInfoSemana(year, week){
  var monday = getMondayOfWeek(year, week);
  var hoje = new Date(); hoje.setHours(0,0,0,0);
  var total = 0, decorridos = 0;
  for(var i = 0; i < 5; i++){
    var d = new Date(monday);
    d.setDate(monday.getDate() + i);
    var ds = toISODate(d);
    if(!FERIADOS.has(ds)){
      total++;
      if(d <= hoje) decorridos++;
    }
  }
  return {decorridos: Math.min(decorridos, total), total: Math.max(total, 1)};
}

// Populates the week selector with last 12 weeks that have data in JSON
function populateWowSelect(){
  var sel=document.getElementById('wowWeekSelect');
  if(!sel||sel.options.length>0) return; // already populated
  var keys=new Set();
  D.forEach(function(p){Object.keys(p.semanas||{}).forEach(function(k){keys.add(k);});});
  var arr=Array.from(keys).sort().reverse().slice(0,12);
  var curKey=getWeekKey(anoISOAtual,semAtual);
  arr.forEach(function(k){
    var opt=document.createElement('option');
    opt.value=k;
    var parts=k.split('-');
    opt.text='Semana '+parts[1]+' / '+parts[0];
    if(k===curKey) opt.selected=true;
    sel.appendChild(opt);
  });
}

function renderWoW() {
  // --- Populate and read week selector ---
  populateWowSelect();
  var sel=document.getElementById('wowWeekSelect');
  var curKey=getWeekKey(anoISOAtual,semAtual);
  var selKey=sel&&sel.value?sel.value:curKey;
  var parts=selKey.split('-');
  var selAno=parseInt(parts[0]), selSem=parseInt(parts[1]);
  var semAntAno=selAno, semAntNum=selSem-1;
  if(semAntNum<1){semAntAno--;semAntNum=52;}
  var semAtualKey=selKey;
  var semAntKey=getWeekKey(semAntAno,semAntNum);

  // --- Partial week correction (holidays-aware) ---
  var isCurrentWeek=(selKey===curKey);
  var infoSem = getInfoSemana(selAno, selSem);
  var diasUteis      = isCurrentWeek ? infoSem.decorridos : infoSem.total;
  var totalDiasUteis = infoSem.total;   // pode ser <5 se houver feriado na semana
  var fator = totalDiasUteis > 0 ? diasUteis / totalDiasUteis : 1;
  var semanaEmAndamento = isCurrentWeek && diasUteis < totalDiasUteis;

  // --- Partial badge ---
  var badge=document.getElementById('wowPartialBadge');
  if(badge){
    if(semanaEmAndamento){
      var feriadoEssaSem = totalDiasUteis < 5 ? ' (semana com feriado)' : '';
      badge.innerHTML='<span class="wow-partial-badge">&#9203; Semana em andamento \u2013 '+diasUteis+'/'+totalDiasUteis+' dias \u00fateis'+feriadoEssaSem+' | compara\u00e7\u00e3o ajustada proporcionalmente</span>';
    } else if(isCurrentWeek && totalDiasUteis < 5){
      badge.innerHTML='<span class="wow-partial-badge" style="background:#e9d8fd;border-color:#805ad5;color:#553c9a">&#127919; Semana com feriado \u2013 '+totalDiasUteis+'/5 dias \u00fateis \u00fateis</span>';
    } else {
      badge.innerHTML='';
    }
  }

  var w=selSem;

  // Compute per-partner data
  // anteriorAdj = anterior ajustado pelo fator de dias úteis (para comparação justa com semana parcial)
  var parceiros = D.map(function(p) {
    var sem = p.semanas || {};
    var atual = sem[semAtualKey] || 0;
    var anterior = sem[semAntKey] || 0;
    var anteriorAdj = Math.round(anterior * fator); // proporcional ao recorte da semana atual
    var delta = atual - anteriorAdj;
    var deltaPct = anteriorAdj > 0 ? ((delta / anteriorAdj) * 100) : (atual > 0 ? 100 : 0);
    return {
      nome: p.nome,
      cat: p.cat,
      isp: p.isp,
      is_sazonal: p.is_sazonal,
      atual: atual,
      anterior: anterior,
      anteriorAdj: anteriorAdj,
      delta: delta,
      deltaPct: deltaPct
    };
  });

  // Totals
  var totalAtual = parceiros.reduce(function(s, p) { return s + p.atual; }, 0);
  var totalAnterior = parceiros.reduce(function(s, p) { return s + p.anterior; }, 0);
  var totalAnteriorAdj = parceiros.reduce(function(s, p) { return s + p.anteriorAdj; }, 0);
  var totalDelta = totalAtual - totalAnteriorAdj;
  var totalDeltaPct = totalAnteriorAdj > 0 ? ((totalDelta / totalAnteriorAdj) * 100) : 0;

  // Active partners (sent > 0)
  var ativosAtual = parceiros.filter(function(p) { return p.atual > 0; }).length;
  var ativosAnterior = parceiros.filter(function(p) { return p.anterior > 0; }).length;
  var ativosDelta = ativosAtual - ativosAnterior;

  // Average per active partner
  var avgAtual = ativosAtual > 0 ? (totalAtual / ativosAtual) : 0;
  var avgAnteriorAdj = ativosAnterior > 0 ? (totalAnteriorAdj / ativosAnterior) : 0;
  var avgDelta = avgAtual - avgAnteriorAdj;
  var avgDeltaPct = avgAnteriorAdj > 0 ? ((avgDelta / avgAnteriorAdj) * 100) : 0;

  // ISP medio variation (use current filtered data)
  var nfParceiros = parceiros.filter(function(p) { return p.cat !== 'Fantasma'; });
  var ispValsNow = D.filter(function(p) { return p.cat !== 'Fantasma' && p.isp >= 0; }).map(function(p) { return p.isp; });
  var ispMedNow = ispValsNow.length > 0 ? Math.round(ispValsNow.reduce(function(s, v) { return s + v; }, 0) / ispValsNow.length) : 0;

  // Helper to build delta badge
  function deltaBadge(val, pct, isInt) {
    var cls = val > 0 ? 'up' : (val < 0 ? 'down' : 'flat');
    var arrow = val > 0 ? '\u25B2' : (val < 0 ? '\u25BC' : '\u25CF');
    var display = isInt ? (val > 0 ? '+' : '') + val : (val > 0 ? '+' : '') + val.toFixed(1);
    var pctStr = pct !== null ? ' (' + (pct > 0 ? '+' : '') + pct.toFixed(1) + '%)' : '';
    return '<span class="wow-delta ' + cls + '">' + arrow + ' ' + display + pctStr + '</span>';
  }

  // Projection note for partial week
  var projNote = '';
  if(semanaEmAndamento && fator > 0){
    var proj = Math.round(totalAtual / fator);
    projNote = '<p class="wow-proj-note">Proje\u00e7\u00e3o semana completa: ~' + fN(proj) + ' leads</p>';
  }

  // Section A: KPI Cards
  var adjLabel = semanaEmAndamento ? ' (ajust. ' + diasUteis + '/' + totalDiasUteis + ' du)' : (totalDiasUteis < 5 ? ' (sem. c/ feriado \u2013 ' + totalDiasUteis + ' du)' : '');

  // VLR a distribuir por semana
  var vlrAtual=0, vlrAnterior=0;
  D.forEach(function(p){
    vlrAtual   += ((p.vlr_dist_semanas||{})[semAtualKey]||0);
    vlrAnterior += ((p.vlr_dist_semanas||{})[semAntKey]||0);
  });
  var vlrAntAdj   = Math.round(vlrAnterior * fator);
  var vlrDelta    = vlrAtual - vlrAntAdj;
  var vlrDeltaPct = vlrAntAdj > 0 ? (vlrDelta / vlrAntAdj * 100) : 0;

  var kpiHtml = '';
  kpiHtml += '<div class="wow-kpi" style="border-left-color:var(--az)"><div class="wow-kpi-label">Total de Leads</div><div class="wow-kpi-value">' + fN(totalAtual) + '</div><div class="wow-kpi-sub">vs ' + fN(totalAnteriorAdj) + adjLabel + ' sem. anterior ' + deltaBadge(totalDelta, totalDeltaPct, true) + '</div>' + projNote + '</div>';
  kpiHtml += '<div class="wow-kpi" style="border-left-color:var(--vd)"><div class="wow-kpi-label">Parceiros Ativos</div><div class="wow-kpi-value">' + ativosAtual + '</div><div class="wow-kpi-sub">vs ' + ativosAnterior + ' sem. anterior ' + deltaBadge(ativosDelta, null, true) + '</div></div>';
  kpiHtml += '<div class="wow-kpi" style="border-left-color:#FFD400"><div class="wow-kpi-label">M\u00e9dia por Ativo</div><div class="wow-kpi-value">' + avgAtual.toFixed(1) + '</div><div class="wow-kpi-sub">vs ' + avgAnteriorAdj.toFixed(1) + adjLabel + ' sem. anterior ' + deltaBadge(avgDelta, avgDeltaPct, false) + '</div></div>';
  kpiHtml += '<div class="wow-kpi" style="border-left-color:var(--warn)"><div class="wow-kpi-label">ISP M\u00e9dio</div><div class="wow-kpi-value">' + ispMedNow + '</div><div class="wow-kpi-sub">\u00edndice de sa\u00fade atual da base</div></div>';
  kpiHtml += '<div class="wow-kpi" style="border-left-color:#805ad5"><div class="wow-kpi-label">VLR a Distribuir</div><div class="wow-kpi-value" style="color:#805ad5;font-size:18px">' + fB(vlrAtual) + '</div><div class="wow-kpi-sub">vs ' + fB(vlrAntAdj) + adjLabel + ' sem. anterior ' + deltaBadge(vlrDelta, vlrDeltaPct, false) + '</div></div>';
  document.getElementById('wowKpis').innerHTML = kpiHtml;

  // Sort for top increases and decreases
  var sorted = parceiros.slice().sort(function(a, b) { return b.delta - a.delta; });
  var topUp = sorted.filter(function(p) { return p.delta > 0; }).slice(0, 5);
  var topDown = sorted.filter(function(p) { return p.delta < 0; }).sort(function(a, b) { return a.delta - b.delta; }).slice(0, 5);

  // Section B: Top increases
  function buildWowRow(list, bodyId) {
    var html = '';
    if (list.length === 0) {
      html = '<tr><td colspan="8" style="text-align:center;color:#7A8599;padding:16px">Sem variações significativas nesta semana</td></tr>';
    } else {
      list.forEach(function(p, i) {
        var impacto = totalAtual > 0 ? Math.abs(p.delta) / totalAtual * 100 : 0;
        var cls = p.delta > 0 ? 'tend-up' : (p.delta < 0 ? 'tend-down' : 'tend-flat');
        var arrow = p.delta > 0 ? '\u25B2' : (p.delta < 0 ? '\u25BC' : '');
        html += '<tr>';
        html += '<td style="font-weight:700;text-align:center">' + (i + 1) + '</td>';
        html += '<td style="font-weight:600">' + p.nome + '</td>';
        html += '<td>' + catBd(p.cat) + '</td>';
        html += '<td style="text-align:center">' + p.anterior + '</td>';
        html += '<td style="text-align:center;font-weight:700">' + p.atual + '</td>';
        html += '<td style="text-align:center" class="' + cls + '">' + arrow + ' ' + (p.delta > 0 ? '+' : '') + p.delta + '</td>';
        html += '<td style="text-align:center" class="' + cls + '">' + (p.deltaPct > 0 ? '+' : '') + p.deltaPct.toFixed(1) + '%</td>';
        html += '<td style="text-align:center">' + impacto.toFixed(1) + '%</td>';
        html += '</tr>';
      });
    }
    document.getElementById(bodyId).innerHTML = html;
  }

  buildWowRow(topUp, 'wowUpBody');
  buildWowRow(topDown, 'wowDownBody');

  // Section D: Insights
  var insights = [];
  var bulletColors = ['var(--az)', 'var(--vd)', 'var(--danger)', 'var(--warn)', '#804080'];

  // Insight 1: Overall trend
  if (totalDelta < 0) {
    var biggestDrop = topDown.length > 0 ? topDown[0] : null;
    if (biggestDrop) {
      insights.push('A queda de ' + Math.abs(totalDelta) + ' leads (' + totalDeltaPct.toFixed(1) + '%) foi puxada principalmente por <strong>' + biggestDrop.nome + '</strong>, que reduziu de ' + biggestDrop.anterior + ' para ' + biggestDrop.atual + ' leads.');
    } else {
      insights.push('Houve uma queda de ' + Math.abs(totalDelta) + ' leads (' + totalDeltaPct.toFixed(1) + '%) em relação à semana anterior.');
    }
  } else if (totalDelta > 0) {
    var aumentaram = parceiros.filter(function(p) { return p.delta > 0; }).length;
    insights.push('O aumento de ' + totalDelta + ' leads (+' + totalDeltaPct.toFixed(1) + '%) foi distribuído: <strong>' + aumentaram + ' parceiros</strong> aumentaram envio esta semana.');
  } else {
    insights.push('O volume de leads permaneceu estável em relação à semana anterior (' + totalAtual + ' leads).');
  }

  // Insight 2: Concentration
  var topN = parceiros.slice().sort(function(a, b) { return b.atual - a.atual; }).slice(0, 3);
  var top3Sum = topN.reduce(function(s, p) { return s + p.atual; }, 0);
  var top3Pct = totalAtual > 0 ? (top3Sum / totalAtual * 100) : 0;
  if (totalAtual > 0) {
    insights.push('Concentração: os 3 maiores parceiros (<strong>' + topN.map(function(p) { return p.nome; }).join(', ') + '</strong>) representam <strong>' + top3Pct.toFixed(1) + '%</strong> do total da semana.');
  }

  // Insight 3: Seasonal partners
  var sazonaisQueda = parceiros.filter(function(p) { return p.is_sazonal && p.delta < 0; });
  if (sazonaisQueda.length > 0) {
    insights.push(sazonaisQueda.length + ' parceiro(s) sazonal(is) apresentaram queda: <strong>' + sazonaisQueda.slice(0, 3).map(function(p) { return p.nome; }).join(', ') + '</strong> — a queda era esperada pelo padrão de envio irregular.');
  }

  // Insight 4: New active partners
  var novosAtivos = parceiros.filter(function(p) { return p.atual > 0 && p.anterior === 0; });
  if (novosAtivos.length > 0) {
    insights.push('<strong>' + novosAtivos.length + ' parceiro(s)</strong> enviaram leads esta semana pela primeira vez (ou retomaram após pausa): ' + novosAtivos.slice(0, 3).map(function(p) { return p.nome; }).join(', ') + '.');
  }

  // Insight 5: Partners that stopped
  var pararam = parceiros.filter(function(p) { return p.atual === 0 && p.anterior > 0; });
  if (pararam.length > 0) {
    insights.push('<strong>' + pararam.length + ' parceiro(s)</strong> que enviavam na semana anterior não enviaram nesta semana: ' + pararam.slice(0, 3).map(function(p) { return p.nome + ' (' + p.anterior + ' leads)'; }).join(', ') + '.');
  }

  var semLabel = semanaEmAndamento ? ' ('+diasUteis+'/'+totalDiasUteis+' dias \u00fateis)' : (isCurrentWeek && totalDiasUteis<5 ? ' (semana c/ feriado \u2013 '+totalDiasUteis+' du)' : '');
  var insHtml = '<h3 style="font-size:13px;font-weight:700;color:var(--ae);margin-bottom:12px">An\u00e1lise Autom\u00e1tica \u2014 Semana ' + w + semLabel + '</h3>';
  insights.forEach(function(txt, idx) {
    var col = bulletColors[idx % bulletColors.length];
    insHtml += '<div class="wow-insight-item"><div class="wow-insight-bullet" style="background:' + col + '"></div><div>' + txt + '</div></div>';
  });
  document.getElementById('wowInsights').innerHTML = insHtml;

  // ===== SECTION E: PERSPECTIVA DA SEMANA =====
  var perspEl = document.getElementById('wowPerspectiva');
  if(perspEl){
    var pH = '';

    if(semanaEmAndamento){
      // ---- Semana em andamento ----
      var diasRestantes = totalDiasUteis - diasUteis;
      var ritmoAtual = diasUteis > 0 ? (totalAtual / diasUteis) : 0;
      var projecaoFechamento = Math.round(ritmoAtual * 5);
      var gapProj = projecaoFechamento - totalAnterior; // projetado vs semana anterior (completa)
      var gapPct = totalAnterior > 0 ? Math.round(gapProj / totalAnterior * 100) : 0;
      var leadsParaIgualar = Math.max(0, totalAnterior - totalAtual);
      var ritmoNecessario = diasRestantes > 0 ? Math.ceil(leadsParaIgualar / diasRestantes) : null;
      var ritmoParaSuperarPct = Math.ceil(totalAnterior * 1.1 / 5); // ritmo p/ +10% vs ant
      var tendCorStr = gapProj >= 0 ? 'green' : 'red';
      var tendCorEmoji = gapProj >= 0 ? '\u2197\ufe0f' : '\u2198\ufe0f';

      // Cards de métricas
      pH += '<div class="persp-grid">';
      var feriadoNote = totalDiasUteis < 5 ? ' \u2014 semana com feriado (' + totalDiasUteis + ' du)' : '';
      pH += '<div class="persp-card blue"><div class="pc-label">Ritmo Atual</div><div class="pc-value">' + ritmoAtual.toFixed(1) + ' leads/dia</div><div class="pc-sub">m\u00e9dia dos ' + diasUteis + '/' + totalDiasUteis + ' dia(s) \u00fatil(eis) decorridos'+feriadoNote+'</div></div>';
      pH += '<div class="persp-card ' + tendCorStr + '"><div class="pc-label">Proje\u00e7\u00e3o de Fechamento</div><div class="pc-value">' + fN(projecaoFechamento) + ' leads</div><div class="pc-sub">' + tendCorEmoji + ' ' + (gapProj >= 0 ? '+' : '') + fN(gapProj) + ' (' + (gapPct >= 0 ? '+' : '') + gapPct + '%) vs sem. anterior</div></div>';
      pH += '<div class="persp-card orange"><div class="pc-label">Leads Restantes para Igualar</div><div class="pc-value">' + fN(leadsParaIgualar) + '</div><div class="pc-sub">em ' + diasRestantes + ' dia(s) \u00fatil(eis) restante(s)</div></div>';
      if(ritmoNecessario !== null){
        pH += '<div class="persp-card purple"><div class="pc-label">Ritmo Necess\u00e1rio</div><div class="pc-value">' + ritmoNecessario + ' leads/dia</div><div class="pc-sub">para fechar igual \u00e0 semana anterior</div></div>';
      }
      pH += '</div>';

      // Ações textuais
      pH += '<div>';

      var feriadoCtx = totalDiasUteis < 5 ? ' Esta semana tem feriado (' + totalDiasUteis + ' dias \u00fateis no total).' : '';
      if(gapProj < 0){
        pH += '<div class="persp-action"><span class="pa-icon">\u26a0\ufe0f</span><div>No ritmo atual (<strong>' + ritmoAtual.toFixed(1) + ' leads/dia</strong>), a semana deve fechar com <strong>' + fN(projecaoFechamento) + ' leads</strong> \u2014 <strong>' + fN(Math.abs(gapProj)) + ' a menos</strong> que a semana anterior (' + fN(totalAnterior) + ').' + feriadoCtx + ' Para recuperar, ser\u00e1 preciso acelerar para pelo menos <strong>' + (ritmoNecessario !== null ? ritmoNecessario : '\u2014') + ' leads/dia</strong> nos pr\u00f3ximos ' + diasRestantes + ' dia(s) \u00fatil(eis).</div></div>';
      } else {
        pH += '<div class="persp-action"><span class="pa-icon">\u2705</span><div>No ritmo atual (<strong>' + ritmoAtual.toFixed(1) + ' leads/dia</strong>), a semana deve fechar com <strong>' + fN(projecaoFechamento) + ' leads</strong> \u2014 <strong>' + fN(gapProj) + ' a mais</strong> que a semana anterior (' + fN(totalAnterior) + ').' + feriadoCtx + ' Para superar +10%, o objetivo seria <strong>' + fN(Math.ceil(totalAnterior*1.1)) + ' leads</strong> na semana.</div></div>';
      }

      // Parceiros adormecidos (enviaram na sem. anterior mas ainda não enviaram nessa)
      var adormecidos = parceiros.filter(function(p){ return p.anterior > 0 && p.atual === 0; })
        .sort(function(a,b){ return b.anterior - a.anterior; });
      if(adormecidos.length > 0){
        var potencial = adormecidos.reduce(function(s,p){return s+p.anterior;},0);
        var potencialAdj = Math.round(potencial * fator);
        pH += '<div class="persp-action"><span class="pa-icon">\ud83d\udca4</span><div><strong>' + adormecidos.length + ' parceiro(s)</strong> que enviaram na semana anterior ainda n\u00e3o registraram leads esta semana. Potencial represado: <strong>~' + fN(potencialAdj) + ' leads</strong> (proporcional ao recorte atual). Acionar esses parceiros pode ser suficiente para recuperar a semana.</div></div>';
        pH += '<details class="persp-dormentes"><summary>Ver parceiros adormecidos (' + adormecidos.length + ')</summary>';
        pH += '<table><thead><tr><th>Parceiro</th><th>Cat.</th><th>Leads s. ant. (total)</th><th title="Leads da semana anterior multiplicados pelo fator de dias \u00fateis decorridos. Ex: se a semana atual tem 3/5 dias \u00fateis, o esperado \u00e9 60% do que o parceiro enviou na semana anterior.">Esperado esta semana \u2139\ufe0f</th></tr></thead><tbody>';
        adormecidos.slice(0,15).forEach(function(p){
          pH += '<tr><td><strong>'+p.nome+'</strong></td><td>'+catBd(p.cat)+'</td><td style="text-align:center">'+p.anterior+'</td><td style="text-align:center">'+Math.round(p.anterior*fator)+'</td></tr>';
        });
        if(adormecidos.length>15) pH+='<tr><td colspan="4" style="color:#7A8599;font-style:italic">...e mais '+(adormecidos.length-15)+' parceiros</td></tr>';
        pH += '</tbody></table></details>';
      }

      // Parceiros em aceleração (enviando acima do ritmo médio da semana anterior)
      var acelerando = parceiros.filter(function(p){ return p.atual > 0 && p.atual > p.anteriorAdj; })
        .sort(function(a,b){ return (b.atual - b.anteriorAdj) - (a.atual - a.anteriorAdj); }).slice(0,5);
      if(acelerando.length > 0){
        pH += '<div class="persp-action"><span class="pa-icon">\ud83d\ude80</span><div><strong>' + acelerando.length + ' parceiro(s)</strong> j\u00e1 est\u00e3o acima do proporcional da semana anterior: <strong>' + acelerando.map(function(p){return p.nome+' (+'+( p.atual - p.anteriorAdj )+')'}).join(', ') + '</strong>. S\u00e3o os destaques positivos da semana.</div></div>';
      }

      pH += '</div>';

    } else {
      // ---- Semana passada (j\u00e1 fechada) ----
      var semFechouStr = gapProj >= 0 ? 'green' : 'red';
      // Para semana passada, totalAnterior = completo, totalAtual = completo, fator=1
      var deltaFinal = totalAtual - totalAnterior;
      var deltaPctFinal = totalAnterior > 0 ? Math.round(deltaFinal / totalAnterior * 100) : 0;
      var corCard = deltaFinal >= 0 ? 'green' : 'red';
      var emojiCard = deltaFinal >= 0 ? '\u2197\ufe0f' : '\u2198\ufe0f';

      pH += '<div class="persp-grid">';
      pH += '<div class="persp-card blue"><div class="pc-label">Fechamento da Semana</div><div class="pc-value">' + fN(totalAtual) + ' leads</div><div class="pc-sub">semana ' + w + ' completa</div></div>';
      pH += '<div class="persp-card ' + corCard + '"><div class="pc-label">Varia\u00e7\u00e3o vs Semana Anterior</div><div class="pc-value">' + (deltaFinal >= 0 ? '+' : '') + fN(deltaFinal) + '</div><div class="pc-sub">' + emojiCard + ' ' + (deltaPctFinal >= 0 ? '+' : '') + deltaPctFinal + '% vs sem. ' + (w-1) + '</div></div>';
      var top1 = parceiros.slice().sort(function(a,b){return b.atual-a.atual})[0];
      if(top1) pH += '<div class="persp-card orange"><div class="pc-label">Maior Parceiro</div><div class="pc-value">' + fN(top1.atual) + '</div><div class="pc-sub">' + top1.nome + '</div></div>';
      pH += '</div>';

      pH += '<div>';
      if(deltaFinal < 0){
        var causadores = parceiros.filter(function(p){return p.delta < 0;}).sort(function(a,b){return a.delta-b.delta;}).slice(0,3);
        pH += '<div class="persp-action"><span class="pa-icon">\ud83d\udcca</span><div>A semana fechou com <strong>' + fN(Math.abs(deltaFinal)) + ' leads a menos</strong> (' + deltaPctFinal + '%) que a anterior. Principais respons\u00e1veis pela queda: <strong>' + causadores.map(function(p){return p.nome+' ('+p.delta+')'}).join(', ') + '</strong>.</div></div>';
      } else {
        var impulsores = parceiros.filter(function(p){return p.delta > 0;}).sort(function(a,b){return b.delta-a.delta;}).slice(0,3);
        pH += '<div class="persp-action"><span class="pa-icon">\ud83c\udfc6</span><div>A semana fechou <strong>' + fN(deltaFinal) + ' leads acima</strong> da anterior (+' + deltaPctFinal + '%). Principais impulsores: <strong>' + impulsores.map(function(p){return p.nome+' (+'+p.delta+')'}).join(', ') + '</strong>.</div></div>';
      }
      var parou = parceiros.filter(function(p){return p.atual===0&&p.anterior>0;});
      if(parou.length > 0){
        pH += '<div class="persp-action"><span class="pa-icon">\ud83d\udd34</span><div><strong>' + parou.length + ' parceiro(s)</strong> que enviaram na semana anterior n\u00e3o enviaram nessa semana: ' + parou.slice(0,5).map(function(p){return p.nome+' ('+p.anterior+' leads)'}).join(', ') + '. Aten\u00e7\u00e3o para reativação na pr\u00f3xima semana.</div></div>';
      }
      pH += '</div>';
    }

    perspEl.innerHTML = pH;
  }

  // Render regional WoW section
  renderWoWRegional(semAtualKey, semAntKey, fator);
}

// ===== DEFAULT DATES (mes vigente + 2 anteriores = 3 meses) =====
(function(){
  var now=new Date();
  var toDate=new Date(now.getFullYear(),now.getMonth(),now.getDate());
  var curMonth=now.getMonth();
  var curYear=now.getFullYear();
  var fromMonth=curMonth-2;
  var fromYear=curYear;
  if(fromMonth<0){fromMonth+=12;fromYear-=1}
  var fromDate=new Date(fromYear,fromMonth,1);
  var fmt=function(d){var y=d.getFullYear();var m=('0'+(d.getMonth()+1)).slice(-2);var dd=('0'+d.getDate()).slice(-2);return y+'-'+m+'-'+dd};
  var fromStr=fmt(fromDate), toStr=fmt(toDate);
  document.getElementById('gfDateFrom').value=fromStr;
  document.getElementById('gfDateTo').value=toStr;
  // Segunda aba (Explorador) usa o mesmo período por padrão
  document.getElementById('dadosDateFrom').value=fromStr;
  document.getElementById('dadosDateTo').value=toStr;
})();

// ===== BLOCO 7: VISAO POR REGIONAL =====
function renderRegional(){
  var gf=GF;
  var totalAll=gf.length;
  var html='<table class="prod-table"><thead><tr><th>Regional</th><th>Parceiros</th><th>% Total</th><th>Leads (4 sem)</th><th>Pagos</th><th>R$ Compra</th><th>ISP Médio</th></tr></thead><tbody>';
  REG_LIST.forEach(function(reg){
    var ps=gf.filter(function(p){return p.regional===reg});
    var n=ps.length;
    var pct=totalAll>0?Math.round(n/totalAll*100):0;
    var l4=ps.reduce(function(s,p){return s+p.sem4},0);
    var pg=ps.reduce(function(s,p){return s+p.pagos},0);
    var comp=ps.reduce(function(s,p){return s+p.compra},0);
    var ispArr=ps.filter(function(p){return p.isp>=0&&p.cat!=='Fantasma'}).map(function(p){return p.isp});
    var ispM=ispArr.length>0?Math.round(ispArr.reduce(function(s,v){return s+v},0)/ispArr.length):0;
    html+='<tr><td><span class="prod-badge" style="background:'+(REG_COLORS[reg]||'#B0B0B0')+';color:'+(reg==='SP (C/D)'||reg==='N/I'?'#333':'#fff')+'">'+reg+'</span></td><td>'+n+'</td><td>'+pct+'%</td><td>'+fN(l4)+'</td><td>'+fN(pg)+'</td><td>'+fB(comp)+'</td><td>'+ispM+'</td></tr>';
  });
  html+='</tbody></table>';
  document.getElementById('regionalTable').innerHTML=html;
}

// ===== CHURN SCORE =====
function calcChurnScore(p){
  var score=0;
  if(p.tend<-20)score+=30;else if(p.tend<-10)score+=20;else if(p.tend<0)score+=10;
  var sp=p.semanas_parado||0;
  if(sp>=8)score+=30;else if(sp>=4)score+=20;else if(sp>=2)score+=10;
  if(p.isp<20)score+=20;else if(p.isp<40)score+=10;
  if(p.envio_class==='Sem envio')score+=10;else if(p.envio_class==='Regular')score+=5;
  if(p.is_sazonal&&sp<6)score=Math.max(0,score-10);
  return Math.min(100,score);
}

// ===== BENCHMARK UF =====
function calcBenchmarkUF(p){
  if(!p.uf||p.uf==='')return null;
  var peers=D.filter(function(x){return x.uf===p.uf&&x.nome!==p.nome&&x.cat!=='Fantasma'});
  if(peers.length<2)return null;
  var ispArr=peers.map(function(x){return x.isp}).filter(function(v){return v>=0}).sort(function(a,b){return a-b});
  var l4Arr=peers.map(function(x){return x.sem4}).sort(function(a,b){return a-b});
  var median=function(arr){if(!arr.length)return 0;var m=Math.floor(arr.length/2);return arr.length%2?arr[m]:(arr[m-1]+arr[m])/2};
  return{
    isp_med:median(ispArr),l4_med:median(l4Arr),peers_n:peers.length,
    isp_pct:ispArr.length?ispArr.filter(function(v){return v<=(p.isp>=0?p.isp:0)}).length/ispArr.length*100:50,
    l4_pct:l4Arr.length?l4Arr.filter(function(v){return v<=p.sem4}).length/l4Arr.length*100:50
  };
}

// ===== SAZONALIDADE PROJETADA =====
function calcSazonProjecao(p){
  var projs=[];
  for(var d=1;d<=4;d++){
    var futSem=semAtual+d;var futAno=anoISOAtual;
    if(futSem>52){futSem-=52;futAno+=1}
    var keyAnt=(futAno-1)+'-'+(futSem<10?'0':'')+futSem;
    var val=(p.semanas||{})[keyAnt];
    projs.push({sem:futAno+'-'+(futSem<10?'0':'')+futSem,base:(val!==undefined?val:null)});
  }
  return projs;
}

// ===== LERP COLOR (para mapa coroplético) =====
function lerpColor(a,b,t){
  var ah=parseInt(a.slice(1),16),bh=parseInt(b.slice(1),16);
  var ar=(ah>>16)&255,ag=(ah>>8)&255,ab2=ah&255;
  var br=(bh>>16)&255,bg=(bh>>8)&255,bb2=bh&255;
  var rr=Math.round(ar+(br-ar)*t),rg=Math.round(ag+(bg-ag)*t),rb3=Math.round(ab2+(bb2-ab2)*t);
  return'#'+(rr<16?'0':'')+rr.toString(16)+(rg<16?'0':'')+rg.toString(16)+(rb3<16?'0':'')+rb3.toString(16);
}

// ===== PARCEIROS EM RISCO =====
// DISTINÇÃO IMPORTANTE:
// "Inativo" = STATUS ATUAL (retrospectivo): parceiro que já parou há 8+ semanas. Já aconteceu.
// "Score de Risco de Churn" = PREDIÇÃO (prospectivo): identifica parceiros AINDA ATIVOS com
// sinais de deterioração que podem se tornar inativos em breve. Inativos e Fantasmas são
// excluídos daqui — o score serve para AGIR ANTES da inatividade se consolidar.
function renderRisco(){
  var candidatos=GF.filter(function(p){return p.cat!=='Inativo'&&p.cat!=='Fantasma'});
  var lista=candidatos.map(function(p){return{p:p,score:calcChurnScore(p)}})
    .filter(function(item){return item.score>=25})
    .sort(function(a,b){return b.score-a.score}).slice(0,5);
  var el=document.getElementById('riscoTable');
  if(!el)return;
  if(!lista.length){
    el.innerHTML='<div style="display:flex;gap:10px;align-items:flex-start;padding:12px;background:#F0FFF4;border-radius:8px;border-left:3px solid #38a169">'
      +'<span style="font-size:20px">\uD83D\uDFE2</span>'
      +'<div style="font-size:12px;color:#276749"><strong>Nenhum parceiro ativo com risco significativo detectado.</strong><br>'
      +'<span style="font-weight:400;color:#48BB78">Lembre: o Score de Risco monitora parceiros <em>ainda ativos</em> com sinais de deteriora\u00e7\u00e3o. '
      +'Parceiros Inativos j\u00e1 consolidados s\u00e3o monitorados na Perspectiva da Semana.</span></div>'
      +'</div>';
    return;
  }
  var h='<div style="font-size:11px;color:#7A8599;margin-bottom:12px;padding:8px 12px;background:#FFFAF0;border-left:3px solid #F6AD55;border-radius:0 6px 6px 0">'
    +'\u26A0\uFE0F <strong>Score de Risco de Churn</strong> \u2014 monitora parceiros <em>ainda ativos</em> com sinais de deteriora\u00e7\u00e3o. '
    +'Inativos j\u00e1 consolidados aparecem na Perspectiva da Semana. '
    +'Score \u2265\u202f60\u202f=\u202finterven\u00e7\u00e3o urgente \u00b7 30\u201359\u202f=\u202faten\u00e7\u00e3o redobrada.'
    +'</div>';
  h+='<table class="risco-table"><thead><tr>'
    +'<th>Parceiro</th><th>Categoria</th><th>ISP</th><th>Sem. Parado</th><th>Tend.</th><th>Score de Risco</th>'
    +'</tr></thead><tbody>';
  lista.forEach(function(item){
    var p=item.p,s=item.score;
    var cls=s>=60?'alto':s>=30?'medio':'baixo';
    var icon=s>=60?'\uD83D\uDD34':s>=30?'\uD83D\uDFE1':'\uD83D\uDFE2';
    h+='<tr>'
      +'<td><strong>'+p.nome+'</strong></td>'
      +'<td>'+catBd(p.cat)+'</td>'
      +'<td>'+(p.isp>=0?p.isp:'--')+'</td>'
      +'<td>'+(p.semanas_parado||0)+'</td>'
      +'<td>'+tA(p.tend)+'</td>'
      +'<td><span class="churn-badge '+cls+'">'+icon+' '+s+'/100</span></td>'
      +'</tr>';
  });
  h+='</tbody></table>';
  el.innerHTML=h;
}

// ===== BRAZIL MAP =====
var BP={"AC":"M14,688L23,705L46,726L84,797L80,811L76,815L73,828L69,827L68,838L65,844L56,837L51,837L47,843L45,837L44,840L44,793L45,777L38,799L28,800L28,792L26,780L18,776L21,760L17,745L17,739L15,734L12,716L13,711L10,702L10,694L13,692L12,684L14,688Z","AL":"M395,753L398,757L386,820L380,799L368,773L372,754L380,775L381,771L384,774L388,767L389,757L395,753Z M397,766L397,766Z","AM":"M77,319L79,331L79,353L81,351L87,370L94,360L95,374L97,363L98,363L99,354L102,347L103,351L106,339L107,345L109,335L110,321L116,312L119,313L120,319L123,322L122,336L126,361L125,380L128,413L127,426L125,430L130,445L131,456L135,463L134,456L134,437L135,427L138,420L141,422L143,436L147,429L146,420L150,389L161,389L161,414L167,446L168,449L170,444L170,456L176,469L178,469L180,476L183,481L183,488L189,481L185,497L167,659L165,668L169,694L166,714L167,725L166,751L134,752L133,747L130,755L122,719L114,719L112,733L111,733L111,743L109,749L109,758L102,760L99,777L98,770L96,773L96,779L94,777L92,783L90,777L86,776L85,785L82,793L46,726L23,705L12,684L14,670L19,660L18,641L20,626L22,604L31,581L41,575L43,565L47,566L48,575L50,572L56,445L54,430L54,420L49,407L50,378L55,371L56,375L59,374L57,357L52,357L52,331L68,331L67,327L68,322L71,327L76,310L77,319Z","AP":"M238,240L243,314L246,312L248,328L251,332L251,352L249,372L246,375L243,393L238,405L233,431L233,443L229,449L226,442L225,424L224,423L223,412L221,406L218,385L219,373L216,363L216,350L209,340L207,330L203,329L201,303L203,302L206,312L210,311L212,305L215,310L217,306L217,313L221,313L224,299L227,273L234,238L235,223L238,240Z","BA":"M357,743L358,748L362,752L363,759L364,753L365,760L367,761L368,777L370,780L370,797L372,800L373,813L371,817L372,828L368,828L368,837L372,861L377,858L370,905L367,918L364,917L360,931L361,946L360,950L361,958L359,988L361,1034L358,1087L359,1108L354,1124L353,1134L348,1119L348,1109L344,1096L345,1075L347,1076L347,1063L348,1063L351,1045L348,1032L344,1032L342,1026L337,1030L336,1020L332,1004L329,1007L318,986L315,993L311,986L312,974L308,969L289,1011L290,999L290,977L291,974L287,964L288,944L288,937L290,931L287,932L287,924L289,917L287,918L287,903L288,899L286,893L286,882L288,876L286,875L287,865L289,865L285,861L284,852L288,826L292,817L294,804L298,833L301,837L304,825L307,822L309,825L313,800L312,782L315,771L317,777L320,776L322,785L328,772L332,770L336,748L339,748L343,766L342,778L344,779L347,774L347,762L350,762L351,753L353,751L353,746L357,743Z M354,1124L354,1124Z","CE":"M350,513L365,548L370,570L377,593L374,597L368,638L364,651L364,671L362,680L365,692L360,714L359,714L353,692L345,696L346,672L343,666L341,642L341,607L338,595L339,567L339,562L337,561L338,548L336,535L337,524L337,517L345,511L350,513Z M350,513L350,513Z","DF":"M277,1041L267,1042L268,1020L276,1020L277,1024L277,1041Z","ES":"M343,1234L340,1252L333,1245L333,1235L331,1230L331,1215L332,1208L336,1208L338,1187L341,1179L340,1159L338,1154L341,1153L338,1132L339,1127L342,1126L341,1119L343,1121L345,1116L353,1133L353,1172L352,1186L349,1198L346,1225L343,1234Z M345,1226L345,1226Z M345,1227L345,1227Z M345,1226L345,1226Z M343,1234L343,1234Z","GO":"M248,896L247,914L256,931L259,912L260,918L262,912L264,922L264,933L265,925L266,932L268,926L268,932L272,932L273,939L274,924L276,932L282,919L285,919L286,913L286,920L289,917L287,924L287,934L290,931L288,937L288,944L287,964L291,974L290,977L289,997L287,997L285,988L285,1002L281,1002L282,1013L281,1022L282,1035L277,1041L277,1024L276,1020L268,1020L267,1042L277,1042L275,1060L279,1079L275,1098L277,1104L276,1113L277,1122L270,1140L267,1133L261,1132L256,1146L255,1140L247,1148L245,1164L242,1172L242,1180L226,1148L221,1146L220,1142L222,1134L219,1132L219,1119L218,1101L220,1074L224,1061L223,1052L227,1036L231,1033L235,1003L239,997L242,964L241,949L244,932L245,908L248,896Z","MA":"M280,759L282,736L285,733L285,723L284,716L280,722L274,698L275,692L273,688L275,679L276,651L275,621L271,610L266,607L262,614L274,582L279,554L280,543L284,514L283,508L286,501L286,490L287,486L288,473L287,471L288,467L288,449L290,442L291,450L292,442L291,451L293,446L293,456L294,450L295,456L296,452L296,462L297,453L296,469L299,454L299,461L302,457L301,465L304,465L302,473L304,470L304,474L305,474L304,476L305,478L307,500L310,496L309,499L310,499L310,503L314,489L315,495L318,495L325,508L332,509L332,519L331,527L328,537L325,538L320,569L321,579L321,592L322,607L319,625L319,642L322,653L321,667L316,674L313,668L310,670L303,696L295,707L292,744L290,757L292,779L291,810L286,807L284,789L284,779L282,776L280,759Z M302,472L302,472Z M304,477L304,477Z M293,455L293,455Z M291,447L291,447Z M292,452L292,452Z M303,473L303,473Z M296,468L296,468Z M302,465L302,465Z M299,462L299,462Z M292,450L292,450Z M294,453L294,453Z M292,453L292,453Z M302,473L302,473Z M296,457L296,457Z M291,450L291,450Z M294,454L294,454Z M296,463L296,463Z M300,454L302,453L300,454Z M301,454L301,454Z M301,453L301,453Z M293,452L294,445L293,452Z M293,452L293,452Z M302,461L302,461Z M302,461L302,461Z M293,448L293,448Z M295,448L295,448Z M304,472L304,472Z M303,462L303,462Z M292,445L292,445Z M292,448L292,448Z M294,453L294,453Z M299,457L299,457Z M299,459L299,459Z M300,456L300,456Z M303,468L303,468Z M293,452L293,452Z M305,483L305,483Z M305,484L305,484Z M296,456L296,456Z M299,458L299,458Z M303,466L303,466Z M306,481L306,481Z M304,472L304,472Z M299,457L299,457Z M295,456L295,456Z M300,453L300,453Z M292,450L292,450Z M300,456L300,456Z M304,473L304,473Z M294,453L294,453Z M302,462L302,462Z M294,450L294,450Z M322,502L322,502Z M310,496L310,496Z M304,471L304,471Z M294,452L294,452Z M293,454L293,454Z M294,450L294,450Z M310,496L310,496Z M299,459L299,459Z M302,463L302,463Z M301,454L301,454Z M300,456L300,456Z M299,460L299,460Z M305,485L305,485Z M292,450L292,450Z M280,759L280,759Z M299,456L299,456Z M299,456L299,456Z M294,450L294,450Z M302,464L302,464Z M292,448L292,448Z","MG":"M308,970L312,974L311,986L315,993L318,986L329,1007L332,1004L336,1020L337,1030L343,1027L344,1032L348,1032L351,1045L348,1063L347,1063L347,1076L345,1075L344,1082L344,1096L348,1109L348,1119L345,1116L343,1121L341,1119L342,1126L339,1127L338,1132L341,1153L338,1154L340,1159L341,1178L338,1187L336,1208L332,1208L332,1213L332,1226L330,1237L328,1239L329,1241L326,1265L327,1269L319,1284L312,1282L296,1306L293,1303L292,1314L287,1316L287,1310L285,1308L286,1302L283,1292L284,1285L283,1283L284,1280L283,1273L285,1259L283,1254L280,1257L278,1235L279,1226L277,1218L277,1207L275,1199L271,1200L271,1205L268,1201L268,1206L262,1206L261,1218L260,1207L258,1212L257,1199L254,1196L251,1198L245,1191L240,1203L240,1179L242,1179L242,1172L245,1164L247,1148L255,1140L256,1146L261,1132L267,1133L270,1140L277,1122L276,1113L277,1104L275,1096L279,1079L275,1060L277,1041L282,1035L281,1022L282,1013L281,1002L285,1002L284,991L285,988L287,997L290,996L289,1010L304,974L308,970Z","MS":"M211,1117L219,1122L219,1134L222,1134L220,1142L221,1146L225,1146L230,1159L239,1173L241,1182L240,1189L240,1204L234,1225L234,1237L231,1245L231,1254L229,1261L229,1269L226,1286L214,1318L213,1333L210,1338L209,1359L207,1363L203,1352L197,1360L195,1345L194,1306L192,1291L188,1291L186,1283L182,1292L170,1284L172,1238L171,1236L171,1230L170,1228L168,1207L171,1199L169,1190L173,1160L172,1156L174,1130L175,1129L172,1102L175,1116L180,1109L183,1092L186,1093L189,1087L199,1106L204,1099L207,1106L209,1105L213,1089L213,1106L211,1110L211,1117Z M211,1117L211,1117Z","MT":"M146,932L149,916L149,905L152,894L149,874L149,864L151,856L150,845L147,844L145,840L135,839L135,817L134,806L135,785L134,771L135,770L135,757L134,752L166,752L167,725L166,714L169,694L174,729L174,750L178,757L182,776L248,794L244,826L243,857L244,897L243,904L245,915L241,949L242,964L239,997L235,1003L231,1033L227,1036L223,1052L224,1062L220,1074L218,1092L218,1108L219,1122L211,1117L211,1108L213,1106L213,1089L209,1105L207,1106L204,1099L199,1106L189,1087L186,1093L183,1092L180,1109L175,1116L173,1101L170,1100L166,1087L165,1068L167,1051L148,1051L148,1019L144,1004L148,1004L147,985L145,968L146,959L145,952L143,947L146,938L146,932Z M146,932L146,932Z","PA":"M280,429L280,434L282,429L283,437L284,432L283,439L286,434L286,443L286,439L287,443L288,436L287,447L288,440L288,446L289,441L288,467L287,471L288,473L287,486L286,490L286,501L283,508L284,514L280,543L279,554L274,581L262,614L266,616L269,624L267,630L268,638L266,647L266,655L264,658L263,666L258,677L258,689L256,702L258,712L258,728L254,754L250,772L248,794L182,776L178,757L174,750L174,729L165,668L167,659L185,497L189,481L183,488L183,481L180,476L178,469L176,469L170,456L170,444L168,449L166,441L161,414L161,351L165,349L165,341L167,336L170,340L170,334L175,332L177,320L179,319L182,326L185,322L190,326L191,318L189,309L190,299L196,303L200,297L202,312L203,329L207,330L209,340L216,350L216,363L219,373L218,385L221,406L223,412L224,423L225,424L226,442L229,449L233,443L233,431L238,405L243,393L246,376L248,372L249,386L253,385L256,399L261,409L266,410L265,420L270,428L271,422L272,427L273,421L275,431L276,424L278,427L278,431L279,426L279,432L280,429Z M286,438L286,438Z M289,443L289,443Z M280,428L280,428Z M286,440L286,440Z M272,426L272,426Z M286,440L286,440Z M287,438L287,438Z M284,433L284,433Z M284,434L284,434Z M280,429L280,429Z M285,439L285,439Z M288,438L288,438Z M280,430L280,430Z M280,429L280,429Z M287,437L287,437Z","PB":"M378,641L378,646L376,654L375,668L377,668L378,673L382,669L383,679L385,673L385,664L386,665L385,658L386,652L390,660L400,659L402,686L402,702L399,696L395,698L395,706L386,713L384,724L380,732L378,718L376,719L378,711L378,703L380,699L378,691L369,713L367,713L366,707L364,710L363,704L365,692L362,680L364,671L365,656L364,656L365,653L369,661L373,648L378,641Z M401,679L401,679Z","PE":"M378,692L380,699L378,703L378,711L376,719L378,718L380,732L384,724L386,713L395,706L395,698L399,696L402,702L402,720L398,757L391,754L389,758L388,767L384,774L381,771L380,775L372,754L368,773L367,761L365,760L365,754L364,759L362,752L358,748L356,741L351,753L350,762L347,762L347,774L344,779L342,778L343,766L341,753L336,748L344,726L345,713L343,710L343,699L345,696L353,692L359,714L363,705L364,710L366,707L367,713L369,713L375,695L378,692Z M426,554L426,554Z M426,553L426,553Z","PI":"M333,512L337,520L336,535L338,548L337,561L339,562L339,567L338,595L341,607L341,642L343,666L346,672L345,696L343,699L343,710L345,713L344,726L336,748L332,770L328,772L322,785L320,776L317,777L315,771L312,782L313,800L309,825L307,822L304,825L301,837L298,833L296,825L296,818L294,805L292,811L290,809L292,779L290,757L292,744L295,710L297,703L303,696L309,671L313,668L316,674L321,667L322,653L319,642L319,625L322,607L321,592L321,579L320,569L325,538L328,537L332,521L332,511L333,512Z","PR":"M229,1301L237,1307L243,1318L250,1316L253,1324L254,1337L254,1354L258,1374L257,1387L264,1387L264,1403L267,1399L268,1408L270,1409L264,1439L258,1440L254,1449L251,1440L247,1445L244,1440L243,1450L238,1453L238,1465L236,1469L235,1463L231,1464L228,1458L214,1452L212,1439L211,1425L209,1425L209,1420L206,1428L204,1424L207,1374L207,1365L209,1358L210,1338L213,1333L214,1318L220,1303L228,1307L229,1301Z","RJ":"M305,1332L303,1335L301,1330L302,1320L307,1313L308,1307L304,1304L302,1295L312,1282L319,1284L327,1269L326,1265L329,1241L328,1239L331,1231L333,1235L333,1245L340,1252L339,1261L340,1280L330,1301L330,1309L331,1310L330,1320L319,1319L319,1307L317,1311L318,1318L317,1321L313,1322L314,1322L311,1316L308,1322L306,1321L307,1317L303,1322L303,1329L305,1332Z M316,1320L316,1320Z M308,1324L309,1327L307,1329L308,1324Z M312,1322L310,1323L312,1322Z M318,1311L317,1312L318,1311Z M311,1318L311,1318Z M318,1314L318,1314Z M311,1320L311,1320Z M304,1328L304,1328Z M310,1320L310,1320Z M303,1327L303,1327Z M333,1296L333,1296Z M305,1332L305,1332Z M319,1310L319,1310Z M319,1310L319,1310Z M318,1316L318,1316Z M304,1323L304,1323Z M311,1318L311,1318Z M333,1296L333,1296Z M304,1328L304,1328Z M304,1327L304,1327Z M311,1319L311,1319Z M304,1329L304,1329Z M331,1311L331,1311Z M309,1321L309,1321Z M311,1318L311,1318Z M315,1323L315,1323Z M319,1322L319,1322Z M304,1329L304,1329Z M311,1321L311,1321Z M303,1329L303,1329Z M310,1320L310,1320Z M318,1322L318,1322Z M303,1324L303,1324Z M310,1321L310,1321Z M311,1318L311,1318Z M303,1324L303,1324Z","RN":"M378,597L383,604L390,602L395,606L397,619L400,660L390,660L386,652L385,658L386,665L385,664L385,673L383,679L382,669L378,673L377,668L375,668L378,642L373,648L369,661L364,654L366,643L369,635L374,597L377,593L378,597Z","RO":"M85,795L82,793L85,785L86,776L90,777L92,783L94,777L96,779L96,773L98,770L99,777L102,760L109,758L109,750L111,743L111,733L112,733L114,719L121,719L125,735L126,736L127,744L128,744L129,752L131,755L133,747L135,757L135,770L134,771L135,785L134,806L135,817L135,839L145,840L147,844L150,845L151,856L149,864L149,874L152,894L149,905L149,915L147,923L146,938L143,948L140,939L132,942L128,925L122,920L118,905L117,907L112,897L107,900L103,883L102,886L102,880L100,880L99,868L97,868L98,861L96,850L97,839L96,819L97,809L96,788L94,794L92,789L85,795Z M85,795L85,795Z","RR":"M151,274L150,293L151,305L153,309L152,326L157,344L161,350L161,389L150,389L146,420L147,428L145,435L142,434L141,422L139,420L136,425L134,452L135,463L131,456L130,445L125,430L127,426L128,413L125,380L125,357L122,336L123,322L116,312L116,303L113,305L109,300L110,289L108,275L108,258L102,230L104,236L108,235L110,245L113,244L113,239L115,246L116,241L118,242L118,247L120,256L123,252L123,239L124,239L126,233L131,236L134,230L137,219L140,219L144,203L143,191L148,189L150,201L148,220L153,225L153,233L155,242L151,257L152,266L151,274Z","RS":"M230,1663L227,1674L229,1681L229,1686L227,1694L224,1725L216,1750L215,1745L216,1726L217,1724L219,1712L220,1709L221,1716L222,1714L224,1701L223,1693L224,1686L222,1691L223,1695L219,1706L216,1703L214,1695L213,1683L209,1677L204,1658L198,1650L194,1633L190,1643L190,1631L182,1604L179,1603L178,1612L174,1608L180,1586L184,1565L186,1563L191,1534L193,1537L192,1530L200,1514L199,1511L201,1511L202,1501L207,1498L208,1490L211,1485L214,1489L216,1484L217,1489L220,1483L220,1489L228,1491L231,1501L234,1500L239,1513L244,1536L252,1538L253,1545L251,1549L250,1563L248,1570L250,1574L249,1570L251,1568L253,1573L242,1644L229,1686L229,1673L231,1675L236,1665L236,1659L238,1658L238,1643L240,1642L240,1636L243,1630L243,1614L244,1619L244,1608L241,1617L238,1607L237,1600L237,1612L239,1615L237,1619L237,1630L236,1626L236,1643L234,1646L234,1651L231,1652L230,1668L230,1663Z M237,1630L237,1630Z M249,1569L249,1569Z M239,1619L239,1619Z M250,1563L250,1563Z M237,1602L237,1602Z M229,1672L229,1672Z M216,1725L216,1725Z M250,1565L250,1565Z M235,1662L235,1662Z M238,1611L238,1611Z M239,1610L239,1610Z M230,1663L230,1663Z M238,1609L238,1609Z","SC":"M213,1462L214,1450L217,1450L219,1456L223,1454L231,1464L235,1463L236,1469L238,1465L238,1453L243,1450L244,1440L247,1445L251,1440L254,1449L258,1440L264,1438L265,1449L263,1469L264,1471L264,1485L265,1486L264,1490L265,1493L264,1499L264,1516L263,1540L253,1573L250,1568L249,1570L249,1574L248,1568L250,1565L251,1549L253,1545L252,1538L244,1536L239,1513L234,1500L231,1501L228,1491L220,1489L220,1483L217,1489L216,1484L215,1488L212,1487L213,1478L213,1462Z M266,1496L264,1513L265,1498L266,1496Z M264,1499L264,1499Z","SE":"M370,781L380,799L386,820L381,830L375,862L370,856L370,848L368,835L368,828L372,828L371,817L373,813L372,800L370,797L370,781Z","SP":"M289,1354L288,1360L286,1359L281,1371L272,1399L269,1412L270,1409L268,1408L267,1399L264,1402L265,1390L264,1387L257,1387L258,1374L254,1354L254,1337L253,1327L250,1316L243,1318L237,1307L233,1307L229,1301L228,1307L219,1304L226,1286L229,1269L229,1261L231,1254L231,1245L234,1237L234,1225L244,1193L257,1198L258,1211L260,1207L261,1218L262,1206L268,1206L268,1201L271,1205L271,1200L275,1198L278,1209L277,1218L279,1226L278,1235L280,1257L283,1254L285,1259L283,1273L284,1280L283,1283L284,1285L283,1292L286,1302L285,1308L287,1310L286,1316L292,1314L293,1303L296,1306L302,1296L304,1304L308,1307L307,1313L302,1319L301,1329L303,1335L301,1333L296,1345L296,1353L292,1350L289,1354Z M297,1357L295,1356L297,1349L298,1358L297,1357Z M299,1341L299,1341Z M299,1352L299,1352Z M298,1343L298,1343Z M300,1350L300,1350Z M292,1355L292,1355Z M297,1344L297,1344Z M300,1350L300,1350Z M293,1352L293,1352Z M295,1354L295,1354Z M281,1376L281,1376Z M281,1375L281,1375Z M300,1342L300,1342Z M301,1336L301,1336Z M301,1335L301,1335Z M280,1375L280,1375Z M271,1407L271,1407Z M298,1353L298,1353Z M297,1357L297,1357Z M293,1352L293,1352Z M297,1354L297,1354Z M297,1357L297,1357Z M298,1353L298,1353Z M293,1352L293,1352Z","TO":"M280,759L282,776L284,779L284,789L286,807L292,811L293,807L292,817L288,826L284,852L285,861L289,865L287,865L286,875L288,876L286,882L286,893L288,899L287,903L287,918L289,917L286,920L286,913L285,919L282,919L276,932L274,924L273,939L272,932L268,932L268,926L266,932L265,925L264,933L264,922L261,912L260,918L259,912L258,915L256,931L247,914L249,896L246,902L245,914L244,913L243,858L244,826L250,772L257,735L258,712L256,702L258,689L258,677L263,666L265,654L266,655L266,647L268,638L267,630L269,625L266,616L263,615L265,608L271,610L275,621L276,651L275,679L273,688L275,692L274,698L280,722L284,716L285,720L285,731L282,736L280,759Z",};
var BC={"AC":[46,794],"AL":[385,776],"AM":[93,503],"AP":[225,319],"BA":[331,928],"CE":[354,607],"DF":[274,1033],"ES":[341,1193],"GO":[259,1032],"MA":[296,560],"MG":[302,1138],"MS":[196,1213],"MT":[185,979],"PA":[230,438],"PB":[380,685],"PE":[373,729],"PI":[319,685],"PR":[238,1404],"RJ":[316,1302],"RN":[383,639],"RO":[119,851],"RR":[136,284],"RS":[218,1608],"SC":[244,1492],"SE":[374,827],"SP":[276,1316],"TO":[270,817],};

function renderBrazilMap(){
  var gf=GF;
  // Acumular dados por UF
  var ufData={};
  gf.forEach(function(p){
    var u=(p.uf||'').toUpperCase().trim();
    if(!u)return;
    if(!ufData[u])ufData[u]={count:0,diamantes:0,ouro:0,prata:0,isp_sum:0,isp_cnt:0};
    ufData[u].count++;
    if(p.cat==='Diamante')ufData[u].diamantes++;
    else if(p.cat==='Ouro')ufData[u].ouro++;
    else if(p.cat==='Prata'||p.cat==='Bronze')ufData[u].prata++;
    if(p.isp>=0){ufData[u].isp_sum+=p.isp;ufData[u].isp_cnt++}
  });
  var hasData=Object.keys(ufData).length>0;
  var maxCount=hasData?Math.max.apply(null,Object.values(ufData).map(function(v){return v.count})):1;
  var totalParceiros=gf.length||1;
  var totalDiamantes=gf.filter(function(p){return p.cat==='Diamante'}).length||1;

  // ── INSIGHTS ESTRATÉGICOS ──────────────────────────────────────
  var insights=[];
  if(hasData){
    // 1: estado com mais Diamantes
    var ufArr=Object.entries(ufData);
    var topDia=ufArr.slice().sort(function(a,b){return b[1].diamantes-a[1].diamantes})[0];
    if(topDia&&topDia[1].diamantes>0){
      var pDia=Math.round(topDia[1].diamantes/totalDiamantes*100);
      insights.push({icon:'\uD83C\uDFC6',text:'<strong>'+topDia[0]+'</strong> lidera com <strong>'+topDia[1].diamantes+' parceiros Diamante</strong> \u2014 '+pDia+'% do total Diamante da carteira',bg:'#FFFBEB',border:'#F6AD55',color:'#7B341E'});
    }
    // 2: concentração top 3 estados
    var top3=ufArr.slice().sort(function(a,b){return b[1].count-a[1].count}).slice(0,3);
    var sum3=top3.reduce(function(s,e){return s+e[1].count},0);
    var pct3=Math.round(sum3/totalParceiros*100);
    if(top3.length>=2){
      insights.push({icon:'\uD83D\uDCCD',text:top3.map(function(e){return '<strong>'+e[0]+'</strong>'}).join(', ')+' concentram <strong>'+pct3+'%</strong> da carteira \u2014 '+sum3+' de '+totalParceiros+' parceiros',bg:'#EBF8FF',border:'#63B3ED',color:'#1A365D'});
    }
    // 3: estado com melhor ISP médio (min 3 parceiros)
    var topISP=ufArr.filter(function(e){return e[1].isp_cnt>=3}).sort(function(a,b){return(b[1].isp_sum/b[1].isp_cnt)-(a[1].isp_sum/a[1].isp_cnt)})[0];
    if(topISP){
      var ispM=Math.round(topISP[1].isp_sum/topISP[1].isp_cnt);
      insights.push({icon:'\u2B50',text:'<strong>'+topISP[0]+'</strong> tem o maior ISP m\u00e9dio da base: <strong>'+ispM+' pts</strong> ('+topISP[1].isp_cnt+' parceiros avaliados)',bg:'#F0FFF4',border:'#68D391',color:'#276749'});
    }
  }

  var el=document.getElementById('brazilMap');
  var html='';

  // ── PILLS DE INSIGHTS ─────────────────────────────────────────
  if(insights.length){
    html+='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin-bottom:18px">';
    insights.forEach(function(ins){
      html+='<div style="background:'+ins.bg+';border:1px solid '+ins.border+';border-radius:10px;padding:12px 14px;display:flex;gap:10px;align-items:flex-start">'
           +'<span style="font-size:20px;flex-shrink:0;line-height:1.2">'+ins.icon+'</span>'
           +'<span style="font-size:11px;color:'+ins.color+';line-height:1.6">'+ins.text+'</span>'
           +'</div>';
    });
    html+='</div>';
  }

  // ── LAYOUT PRINCIPAL: MAPA (largo) | LEGENDA (estreita) ─────
  html+='<div style="display:grid;grid-template-columns:3fr 1fr;gap:20px;align-items:start">';

  // ── MAPA SVG ─────────────────────────────────────────────────
  var ufs=['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO'];
  var svg='<svg viewBox="0 0 440 1700" width="100%" style="font-family:Inter,sans-serif;display:block" preserveAspectRatio="xMidYMid meet">';
  ufs.forEach(function(uf){
    if(!BP[uf])return;
    var d=ufData[uf]||{count:0,diamantes:0};
    var cnt=d.count;
    var fill;
    if(!hasData)fill='#D0D8E8';
    else if(cnt===0)fill='#EEF2F8';
    else{var t=Math.pow(cnt/maxCount,0.55);fill=lerpColor('#9EC8F0','#0E2F5D',t)}
    svg+='<path d="'+BP[uf]+'" fill="'+fill+'" stroke="#fff" stroke-width="1.5"><title>'+uf+': '+cnt+' parceiro(s)'+(d.diamantes?' | \u2605 '+d.diamantes+' Diamante(s)':'')+'</title></path>';
    // Label: sigla SEMPRE visível + contagem abaixo quando tem dados
    if(BC[uf]){
      var cx=BC[uf][0],cy=BC[uf][1];
      var darkFill=(cnt/maxCount)>0.38;
      var txtC=darkFill?'#ffffff':(cnt===0?'#9BA5C0':'#0E2F5D');
      // Sigla em destaque
      svg+='<text x="'+cx+'" y="'+(cy-(cnt>0?4:0))+'" text-anchor="middle" dominant-baseline="middle"'
          +' font-size="10" font-weight="700" fill="'+txtC+'" pointer-events="none" letter-spacing="0.5">'+uf+'</text>';
      // Contagem menor abaixo da sigla
      if(cnt>0)
        svg+='<text x="'+cx+'" y="'+(cy+8)+'" text-anchor="middle" dominant-baseline="middle"'
            +' font-size="8" font-weight="400" fill="'+txtC+'" opacity="0.9" pointer-events="none">'+cnt+'</text>';
      // Estrela Diamante no canto superior do estado
      if(d.diamantes>0)
        svg+='<text x="'+(cx+12)+'" y="'+(cy-10)+'" text-anchor="middle"'
            +' font-size="9" fill="#FFD700" pointer-events="none">\u2605</text>';
    }
  });
  svg+='</svg>';
  html+='<div>'+svg+'</div>';

  // ── LEGENDA LATERAL ───────────────────────────────────────────
  html+='<div style="position:sticky;top:80px">';
  html+='<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#7A8599;margin-bottom:14px">Legenda</div>';

  // Bloco gradiente com escala
  html+='<div style="display:flex;gap:10px;align-items:stretch;margin-bottom:16px">';
  // Barra gradiente vertical SVG
  html+='<svg width="20" height="180" style="flex-shrink:0">'
       +'<defs><linearGradient id="mapLgrd" x1="0" y1="0" x2="0" y2="1">'
       +'<stop offset="0%" stop-color="#0E2F5D"/>'
       +'<stop offset="100%" stop-color="#EEF2F8"/>'
       +'</linearGradient></defs>'
       +'<rect width="20" height="180" fill="url(#mapLgrd)" rx="4"/>'
       +'</svg>';
  // Labels de escala
  html+='<div style="display:flex;flex-direction:column;justify-content:space-between;height:180px;font-size:10px;color:#7A8599">';
  var scaleLabels=['M\u00e1x ('+maxCount+')','75%','50%','25%','1'];
  scaleLabels.forEach(function(l){html+='<span style="white-space:nowrap">'+l+'</span>'});
  html+='</div>';
  html+='</div>';

  // Item: sem dados
  html+='<div style="display:flex;align-items:center;gap:7px;margin-bottom:14px;font-size:10px;color:#9BA5C0">'
       +'<div style="width:20px;height:12px;border-radius:3px;background:#EEF2F8;border:1px solid #dde3ec;flex-shrink:0"></div>'
       +'<span>Sem parceiros</span>'
       +'</div>';

  // Item: Diamante
  html+='<div style="display:flex;align-items:center;gap:7px;margin-bottom:20px;font-size:10px;color:#7A8599">'
       +'<span style="font-size:14px;color:#FFD700;line-height:1">\u2605</span>'
       +'<span>Estado com parceiro(s) Diamante</span>'
       +'</div>';

  // Separador
  html+='<div style="border-top:1px solid #F0F2F5;margin-bottom:14px"></div>';

  // Top 5 estados
  html+='<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#7A8599;margin-bottom:10px">Top Estados</div>';
  var top5=Object.entries(ufData).sort(function(a,b){return b[1].count-a[1].count}).slice(0,7);
  if(top5.length){
    top5.forEach(function(entry,idx){
      var uf=entry[0],d=entry[1];
      var pct=Math.round(d.count/totalParceiros*100);
      var barPct=Math.round(d.count/top5[0][1].count*100);
      html+='<div style="margin-bottom:7px">';
      html+='<div style="display:flex;justify-content:space-between;align-items:baseline;font-size:11px;margin-bottom:3px">';
      html+='<span style="font-weight:700;color:var(--ae)">'+uf+'</span>';
      html+='<span style="color:#7A8599">'+d.count+' <span style="font-size:9px;color:#A0AEC0">('+pct+'%)</span></span>';
      html+='</div>';
      html+='<div style="height:5px;background:#F0F2F5;border-radius:3px;overflow:hidden">';
      html+='<div style="width:'+barPct+'%;height:100%;background:#0E2F5D;border-radius:3px;opacity:'+(0.4+0.6*barPct/100).toFixed(2)+'"></div>';
      html+='</div>';
      if(d.diamantes>0)html+='<div style="font-size:9px;color:#B7791F;margin-top:2px">\u2605 '+d.diamantes+' Diamante'+(d.diamantes>1?'s':'')+'</div>';
      html+='</div>';
    });
  }

  html+='</div>'; // end legenda
  html+='</div>'; // end grid
  el.innerHTML=html;
}

// ===== WOW REGIONAL SECTION =====
// semAtualKey, semAntKey e fator são repassados por renderWoW() para manter consistência
function renderWoWRegional(semAtualKey, semAntKey, fator){
  if(fator===undefined) fator=1;
  var adjLabel=fator<1?' (ajust. '+Math.round(fator*5)+'/5 du)':'';
  var html='<h3 style="font-size:13px;font-weight:700;color:var(--ae);margin-bottom:12px">Varia\u00e7\u00e3o Semanal por Regional</h3>';
  html+='<table class="prod-table"><thead><tr><th>Regional</th><th>Sem. Anterior'+adjLabel+'</th><th>Sem. Atual</th><th>Delta</th><th>Delta %</th><th>Parceiros Ativos</th></tr></thead><tbody>';
  REG_LIST.forEach(function(reg){
    var ps=D.filter(function(p){return p.regional===reg});
    var ant=0;var atu=0;var ativosAtu=0;
    ps.forEach(function(p){
      var sem=p.semanas||{};
      var a=sem[semAntKey]||0;
      var c=sem[semAtualKey]||0;
      ant+=Math.round(a*fator);atu+=c;
      if(c>0)ativosAtu++;
    });
    var delta=atu-ant;
    var deltaPct=ant>0?Math.round(delta/ant*100):atu>0?100:0;
    var cls=delta>0?'tend-up':delta<0?'tend-down':'tend-flat';
    var arrow=delta>0?'\u25B2':delta<0?'\u25BC':'';
    html+='<tr><td><span class="prod-badge" style="background:'+(REG_COLORS[reg]||'#B0B0B0')+';color:'+(reg==='SP (C/D)'||reg==='N/I'?'#333':'#fff')+'">'+reg+'</span></td>';
    html+='<td style="text-align:center">'+ant+'</td>';
    html+='<td style="text-align:center;font-weight:700">'+atu+'</td>';
    html+='<td style="text-align:center" class="'+cls+'">'+arrow+' '+(delta>0?'+':'')+delta+'</td>';
    html+='<td style="text-align:center" class="'+cls+'">'+(deltaPct>0?'+':'')+deltaPct+'%</td>';
    html+='<td style="text-align:center">'+ativosAtu+'</td></tr>';
  });
  html+='</tbody></table>';
  document.getElementById('wowRegionalSection').innerHTML=html;
}

// ===== FIX STICKY TABS =====
(function(){
  var hd=document.querySelector('.hd');
  var tabs=document.querySelector('.tabs');
  if(hd&&tabs){
    var hdH=hd.offsetHeight;
    tabs.style.top=hdH+'px';
  }
  window.addEventListener('resize',function(){
    if(hd&&tabs){tabs.style.top=hd.offsetHeight+'px'}
  });
})();

// ===== INITIAL RENDER =====
renderKPIs();
renderPanorama();
renderSaude();
renderProd();
renderEvo();
renderGG();
renderConclusão();
renderRegional();
renderBrazilMap();
renderRisco();
renderWoW();
renderPlanner();

// Kanban removido

// ===== MULTI-SELECT TOGGLE =====
function toggleMS(id){
  var wrap=document.getElementById(id);
  var dd=wrap.querySelector('.ms-dd');
  var isOpen=dd.style.display!=='none';
  // Fechar todos os outros
  document.querySelectorAll('.ms-dd').forEach(function(d){d.style.display='none'});
  if(!isOpen)dd.style.display='block';
}
// Fechar dropdowns ao clicar fora
document.addEventListener('click',function(e){
  if(!e.target.closest('.ms-wrap')){
    document.querySelectorAll('.ms-dd').forEach(function(d){d.style.display='none'});
  }
});
function getCheckedValues(wrapId){
  var checks=document.querySelectorAll('#'+wrapId+' input[type=checkbox]:checked');
  var vals=[];
  checks.forEach(function(c){vals.push(c.value)});
  return vals;
}
function updateMSLabel(wrapId,defaultLabel){
  var vals=getCheckedValues(wrapId);
  var btn=document.querySelector('#'+wrapId+' .ms-btn');
  if(vals.length===0){btn.innerHTML=defaultLabel+' <span class="ms-arrow">&#9662;</span>'}
  else if(vals.length===1){btn.innerHTML=vals[0]+' <span class="ms-arrow">&#9662;</span>'}
  else{btn.innerHTML=vals.length+' selecionados <span class="ms-arrow">&#9662;</span>'}
}

// ===== FILTROS GLOBAIS =====
function applyGlobalFilters(){
  var cats=getCheckedValues('msCat');
  var saudes=getCheckedValues('msSaude');
  var envios=getCheckedValues('msEnvio');
  var regs=getCheckedValues('msRegional');
  var nome=document.getElementById('gfNome').value.toLowerCase();
  var dateFrom=document.getElementById('gfDateFrom').value;
  var dateTo=document.getElementById('gfDateTo').value;

  updateMSLabel('msCat','Categorias');
  updateMSLabel('msSaude','Saúde');
  updateMSLabel('msEnvio','Envio');
  updateMSLabel('msRegional','Regional');

  GF=D.filter(function(p){
    if(cats.length>0&&cats.indexOf(p.cat)===-1)return false;
    if(saudes.length>0&&saudes.indexOf(p.saude)===-1)return false;
    if(envios.length>0&&envios.indexOf(p.envio_class)===-1)return false;
    if(regs.length>0&&regs.indexOf(p.regional)===-1)return false;
    if(nome&&p.nome.toLowerCase().indexOf(nome)===-1)return false;
    // Filtro de data: parceiro deve ter atividade no periodo
    if(dateFrom||dateTo){
      var pUltEnvio=p.data_ultimo_envio||'';
      var pPrimEnvio=p.data_primeiro_envio||'';
      var pUltPago=p.data_ultimo_pago||'';
      var pPrimPago=p.data_primeiro_pago||'';
      var latest=pUltEnvio||pUltPago||'';
      var earliest=pPrimEnvio||pPrimPago||'';
      if(!latest&&!earliest)return true;
      if(dateFrom&&latest&&latest<dateFrom)return false;
      if(dateTo&&earliest&&earliest>dateTo)return false;
    }
    return true;
  });
  document.getElementById('gfCount').textContent=GF.length+' de '+D.length+' parceiros';
  renderKPIs();
  renderPanorama();
  renderSaude();
  renderProd();
  renderEvo();
  renderGG();
  renderConclusão();
  renderRegional();
  renderBrazilMap();
  renderRisco();
}
function resetGlobalFilters(){
  document.querySelectorAll('.ms-dd input[type=checkbox]').forEach(function(c){c.checked=false});
  document.getElementById('gfNome').value='';
  document.getElementById('gfDateFrom').value='';
  document.getElementById('gfDateTo').value='';
  updateMSLabel('msCat','Categorias');
  updateMSLabel('msSaude','Saúde');
  updateMSLabel('msEnvio','Envio');
  updateMSLabel('msRegional','Regional');
  applyGlobalFilters();
}

// ===== PLANNER (KANBAN) =====
// Persistência: localStorage. Futura integração: API REST → PostgreSQL
// TASKS já declarado no topo (linha de inicialização global)
function saveTasks(){localStorage.setItem('eaimeu_tasks',JSON.stringify(TASKS))}
function genTaskId(){return 't_'+Date.now()+'_'+Math.random().toString(36).slice(2,7)}
function abrirNovaTask(){
  document.getElementById('taskTitulo').value='';
  document.getElementById('taskDesc').value='';
  document.getElementById('taskResp').value='';
  document.getElementById('taskParceiro').value='';
  document.getElementById('taskPrio').value='Média';
  document.getElementById('taskData').value='';
  document.getElementById('plannerModal').style.display='flex';
  setTimeout(function(){document.getElementById('taskTitulo').focus()},50);
}
function fecharModalTask(e){if(e.target.id==='plannerModal')document.getElementById('plannerModal').style.display='none'}
function salvarTask(){
  var titulo=document.getElementById('taskTitulo').value.trim();
  if(!titulo){alert('Digite um título para a tarefa.');return}
  var task={id:genTaskId(),titulo:titulo,desc:document.getElementById('taskDesc').value.trim(),resp:document.getElementById('taskResp').value.trim(),parceiro:document.getElementById('taskParceiro').value.trim(),prio:document.getElementById('taskPrio').value,data:document.getElementById('taskData').value,status:'todo',criado:new Date().toISOString()};
  TASKS.push(task);saveTasks();renderPlanner();
  document.getElementById('plannerModal').style.display='none';
}
function moverTask(id,novoStatus){
  var t=TASKS.find(function(x){return x.id===id});
  if(t){t.status=novoStatus;saveTasks();renderPlanner()}
}
function deletarTask(id){
  if(!confirm('Excluir esta tarefa?'))return;
  TASKS=TASKS.filter(function(x){return x.id!==id});saveTasks();renderPlanner();
}
var _dragTaskId=null;
function onKanbanDragStart(id){_dragTaskId=id}
function onKanbanDragOver(e){e.preventDefault();e.currentTarget.classList.add('drag-over')}
function onKanbanDrop(e,status){
  e.preventDefault();
  document.querySelectorAll('.kanban-dropzone').forEach(function(el){el.classList.remove('drag-over')});
  if(_dragTaskId)moverTask(_dragTaskId,status);
  _dragTaskId=null;
}
function renderPlanner(){
  var search=(document.getElementById('plannerSearch')||{value:''}).value.toLowerCase();
  var statuses=['todo','doing','done'];
  var total=0;
  statuses.forEach(function(st){
    var filtered=TASKS.filter(function(t){
      if(t.status!==st)return false;
      if(search&&t.titulo.toLowerCase().indexOf(search)===-1&&(!t.parceiro||t.parceiro.toLowerCase().indexOf(search)===-1))return false;
      return true;
    });
    total+=filtered.length;
    var cnt=document.getElementById('cnt-'+st);
    var cards=document.getElementById('cards-'+st);
    if(cnt)cnt.textContent=filtered.length;
    if(!cards)return;
    if(!filtered.length){cards.innerHTML='<div style="text-align:center;color:#CBD5E0;font-size:11px;padding:20px 0">'+(st==='done'?'Nenhuma conclu\u00edda':'Nenhuma tarefa aqui')+'</div>';return}
    cards.innerHTML=filtered.map(function(t){
      var dataStr=t.data?'<span>\uD83D\uDCC5 '+t.data+'</span>':'';
      var respStr=t.resp?'<span>\uD83D\uDC64 '+t.resp+'</span>':'';
      var parcStr=t.parceiro?'<span style="color:var(--az)">\uD83E\uDD1D '+t.parceiro+'</span>':'';
      var nextStatus=st==='todo'?'doing':st==='doing'?'done':'todo';
      var nextLabel=st==='todo'?'Iniciar':st==='doing'?'Concluir':'Reabrir';
      return '<div class="task-card" data-prio="'+t.prio+'" draggable="true" ondragstart="onKanbanDragStart(\''+t.id+'\')">'
        +'<div class="task-card-title">'+t.titulo+'</div>'
        +(t.desc?'<div class="task-card-desc">'+t.desc+'</div>':'')
        +'<div class="task-card-meta">'
        +'<span class="task-prio-badge '+t.prio+'">'+t.prio+'</span>'
        +dataStr+respStr+parcStr
        +'<button class="task-del-btn" onclick="deletarTask(\''+t.id+'\')" title="Excluir">\u2715</button>'
        +'</div>'
        +'<div style="margin-top:8px;text-align:right"><button class="btn btn-p" style="font-size:10px;padding:3px 10px" onclick="moverTask(\''+t.id+'\',\''+nextStatus+'\')">'+nextLabel+'</button></div>'
        +'</div>';
    }).join('');
  });
  var pc=document.getElementById('plannerCount');
  if(pc)pc.textContent=total+' tarefa(s)';
}

// ===== GLOSSARIO =====
(function(){
  var gs=document.getElementById('glossCats');
  var cats=[
    ['Diamante','<strong>Critérios:</strong> Ticket médio ≥ R$ 1M (direto) <strong>OU</strong> (3+ pagos OU ticket ≥ R$ 500K) <strong>E</strong> média ≥ 3 leads/semana (8 sem) <strong>E</strong> 4+ meses ativos.<br><strong>Perfil:</strong> Topo da carteira. Alto valor de compra e fluxo consistente. Parceiro estratégico.','var(--ae)','#fff'],
    ['Ouro','<strong>Critérios:</strong> 1+ processo pago <strong>E</strong> ticket < R$ 1M <strong>E</strong> enviou nas últimas 8 semanas <strong>E</strong> 2+ meses ativos.<br><strong>Perfil:</strong> Parceiro que compra e mantém envio ativo. Candidato a evoluir para Diamante.','#FFD400','#333'],
    ['Prata','<strong>Critérios:</strong> Enviou nas últimas 8 semanas <strong>E</strong> 3+ leads totais <strong>E</strong> não qualifica para Diamante nem Ouro.<br><strong>Perfil:</strong> Parceiro ativo com volume razoável. Pode ter ou não compras.','#B0B0B0','#333'],
    ['Bronze','<strong>Critérios:</strong> Enviou nas últimas 8 semanas <strong>E</strong> menos de 3 leads totais ou parceiro novo (primeiro envio há ≤ 4 semanas).<br><strong>Perfil:</strong> Parceiro em fase inicial ou com baixo volume. A flag "Novo" identifica estreantes.','#CD7F32','#fff'],
    ['Em Recuperação','<strong>Critérios:</strong> Ficou 8+ semanas sem enviar nenhum lead <strong>E</strong> voltou a enviar nas últimas 4 semanas.<br><strong>Perfil:</strong> Parceiro que retomou atividade após período longo de inatividade. Precisa de acompanhamento próximo.','#17A2B8','#fff'],
    ['Inativo','<strong>Critérios:</strong> Zero envio de leads nas últimas 8+ semanas. Nenhuma atividade recente na esteira.<br><strong>Perfil:</strong> Parceiro que parou de enviar. Pode ter histórico de compra (candidato a reativação) ou não. A saúde (ISP) e o histórico de pagos ajudam a priorizar quem reativar.','var(--ce)','#fff'],
    ['Fantasma','<strong>Critérios:</strong> 1+ processo pago (compra realizada) <strong>E</strong> zero leads enviados na esteira em todo o histórico.<br><strong>Perfil:</strong> Parceiro que gera compras por outros canais mas não usa a esteira para enviar leads. Invisível no funil.','#804080','#fff']
  ];
  gs.innerHTML=cats.map(function(c){return '<div style="display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #F0F2F5"><span class="bd" style="background:'+c[2]+';color:'+c[3]+';min-width:120px;text-align:center;flex-shrink:0">'+c[0]+'</span><span style="font-size:12px;color:var(--ce);line-height:1.6">'+c[1]+'</span></div>'}).join('');

  document.getElementById('glossISP').innerHTML='<div style="font-size:12px;color:var(--ce);line-height:1.6"><p style="margin-bottom:12px">O <strong>ISP (Índice de Saúde do Parceiro)</strong> mede de 0 a 100 a saúde de cada parceiro. Cada componente tem faixas de pontuação específicas:</p>'
    +'<table class="prod-table" style="max-width:800px"><thead><tr><th>Componente</th><th>Peso</th><th>O que mede</th><th>Faixas de pontuação</th></tr></thead><tbody>'
    +'<tr><td><strong>Recência</strong></td><td>25%</td><td>Quando foi o último envio de lead</td><td>Enviou nas últimas 4 sem = 25 pts<br>Enviou entre 5-8 sem atrás = 18 pts<br>Tem histórico mas parado 9+ sem = 5 pts<br>Nunca enviou = 0 pts</td></tr>'
    +'<tr><td><strong>Produção</strong></td><td>25%</td><td>Processos pagos + taxa de conversão</td><td>6+ pagos = 25 pts<br>3-5 pagos = 20 pts<br>2 pagos = 15 pts<br>1 pago = 10 pts<br>0 pagos = 0 pts<br>Bônus: +5 pts se taxa de conversão > 15%</td></tr>'
    +'<tr><td><strong>Volume Ajustado</strong></td><td>20%</td><td>Média semanal de leads nas semanas em que enviou (não penaliza semanas zeradas de parceiros sazonais)</td><td>Média ≥ 5 leads/sem = 20 pts<br>Média 3-4.9 = 15 pts<br>Média 1.5-2.9 = 10 pts<br>Média 0.5-1.4 = 5 pts<br>Média < 0.5 = 2 pts</td></tr>'
    +'<tr><td><strong>Consistência</strong></td><td>15%</td><td>Quantos meses distintos o parceiro enviou leads</td><td>7+ meses = 15 pts<br>4-6 meses = 12 pts<br>2-3 meses = 8 pts<br>1 mês = 3 pts<br>0 meses = 0 pts</td></tr>'
    +'<tr><td><strong>Tendência</strong></td><td>10%</td><td>Variação do envio recente (últimas 4 sem) vs anterior (4 sem antes)</td><td>Crescimento > 20% = 10 pts<br>Estável (-20% a +20%) = 7 pts<br>Queda entre -20% e -50% = 3 pts<br>Queda > 50% = 0 pts</td></tr>'
    +'<tr><td><strong>Valor</strong></td><td>5%</td><td>Valor acumulado em compras de precatórios</td><td>R$ 2M+ = 5 pts<br>R$ 500K-2M = 4 pts<br>R$ 100K-500K = 3 pts<br>Qualquer valor < 100K = 1 pt<br>R$ 0 = 0 pts</td></tr>'
    +'</tbody></table>'
    +'<p style="margin-top:12px;font-style:italic;color:#7A8599">Exemplo: Parceiro com envio nas ult. 4 sem (25) + 3 pagos (20) + média 3 leads/sem (15) + 5 meses ativos (12) + tendência estável (7) + R$ 800K (4) = ISP 83 → Excelente</p></div>';

  var sfaixas=[
    ['Excelente','80-100','Ativo, consistente, com producao e tendência positiva','#38A169'],
    ['Bom','60-79','Ativo com histórico, producao ou volume relevante','#4299E1'],
    ['Regular','40-59','Ativo mas com sinais de queda ou histórico curto','#ECC94B'],
    ['Ruim','20-39','Parado 5-12 sem ou queda severa com pagos','#ED8936'],
    ['Péssimo','0-19','Parado 8+ sem ou sem histórico relevante','#E53E3E'],
    ['Em Recuperação','variavel','Retomou apos gap de 8+ semanas','#17A2B8'],
    ['N/A','--','Fantasma. Sem dados de envio','#A0AEC0']
  ];
  document.getElementById('glossSaude').innerHTML=sfaixas.map(function(s){return '<div style="display:flex;gap:10px;align-items:center;padding:6px 0;border-bottom:1px solid #F0F2F5"><span class="bd" style="background:'+s[3]+';color:#fff;min-width:90px;text-align:center">'+s[0]+'</span><span style="font-size:11px;color:#7A8599;width:50px">'+s[1]+'</span><span style="font-size:12px;color:var(--ce)">'+s[2]+'</span></div>'}).join('');

  var envios=[
    ['Consistente','6+ leads em 4 semanas E atividade em 3+ meses. Media semanal >= 1.5'],
    ['Regular','3-5 leads em 4 sem OU (1-2 mas media por semana ativa >= 2) E 2+ meses'],
    ['Esporadico','1-2 leads em 4 sem E media por semana ativa menor que 2 E apenas 1 mes'],
    ['Novo (flag)','Primeiro envio de todo o historico ha 4 semanas ou menos. Aparece dentro da categoria Bronze.'],
    ['Sem envio','Zero leads nas ultimas 4 semanas']
  ];
  document.getElementById('glossEnvio').innerHTML=envios.map(function(e){return '<div style="display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #F0F2F5"><span style="font-weight:600;min-width:100px;font-size:12px">'+e[0]+'</span><span style="font-size:12px;color:var(--ce)">'+e[1]+'</span></div>'}).join('');

  var termos=[
    ['Parceiro Ativo','Enviou pelo menos 1 lead nas ultimas 4 semanas'],
    ['Parceiro Inativo','Estado atual (retrospectivo): nenhum lead nas ultimas 8+ semanas. O parceiro JA parou de enviar. Diferente do Score de Risco — ver Indicadores Preditivos.'],
    ['Parceiro Sazonal','Envia em rajadas (6 ou menos semanas ativas em 12, mas media alta quando envia). Nao penalizado no ISP'],
    ['Atividade Recente','Qualquer envio de lead nas ultimas 4 semanas'],
    ['Historico Relevante','3 ou mais leads históricos OU pelo menos 1 compra realizada'],
    ['Recorrencia','Envio em 3+ meses distintos'],
    ['Deterioração','Queda progressiva: tendência menor que -30% por 2+ periodos'],
    ['Reativação','Ação para reconectar parceiro Inativo que tem pagos. Gatilho: 8+ semanas parado com compras'],
    ['MID (Mega Investidor)','CPF com ValorBruto ≥ R$ 10M ou CNPJ com ValorBruto ≥ R$ 5M. Excluídos do VLR a Distribuir por terem tratamento diferenciado.']
  ];
  document.getElementById('glossTermos').innerHTML=termos.map(function(t){return '<div style="display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #F0F2F5"><span style="font-weight:600;min-width:140px;font-size:12px;flex-shrink:0">'+t[0]+'</span><span style="font-size:12px;color:var(--ce)">'+t[1]+'</span></div>'}).join('');

  // ─── INDICADORES PREDITIVOS ────────────────────────────────────────────────
  var preditivos=[
    ['Score de Risco de Churn',
     '<span style="font-weight:700;color:#E05353">Predição prospectiva (0–100)</span> — diferente de "Inativo": mede a probabilidade de um parceiro <em>ainda ativo</em> se tornar inativo em breve, baseada em 5 fatores: (1) Tendência de queda (até 30 pts), (2) Semanas sem envio (até 30 pts), (3) ISP baixo (até 20 pts), (4) Classificação de envio ruim (até 10 pts), (5) Desconto para parceiros sazonais (–10 pts). Score ≥ 60 = intervenção urgente; 30–59 = monitoramento ativo; < 30 = risco baixo.<br><strong>Inativo ≠ Risco de Churn:</strong> Inativos já consolidaram a perda. O score serve para agir <em>antes</em> disso acontecer.'],
    ['Benchmark por UF',
     'Compara as métricas de um parceiro (ISP, Leads 4 semanas) com a mediana de todos os parceiros ativos na mesma Unidade Federativa (UF). Exibido no detalhe individual de cada parceiro. Percentil 50%+ = acima da mediana. Útil para contextualizar desempenho relativo dentro da praça.'],
    ['Sazonalidade Projetada',
     'Para cada parceiro, busca o volume de envios da mesma semana no ano anterior (ex: semana 15/2025 como base para semana 15/2026). Exibido como projeção das próximas 4 semanas. Útil para distinguir quedas reais de quedas esperadas pelo padrão histórico anual.'],
  ];
  document.getElementById('glossPreditivos').innerHTML=preditivos.map(function(t){
    return '<div style="padding:10px 0;border-bottom:1px solid #F0F2F5">'
      +'<div style="font-weight:700;font-size:12px;color:var(--ae);margin-bottom:4px">'+t[0]+'</div>'
      +'<div style="font-size:12px;color:var(--ce);line-height:1.6">'+t[1]+'</div>'
      +'</div>';
  }).join('');

  // ─── MÉTRICAS FINANCEIRAS ──────────────────────────────────────────────────
  var financeiro=[
    ['VLR a Distribuir','Soma do ValorBruto de todos os processos <strong>Em andamento</strong> vinculados ao parceiro, excluindo MIDs. Representa o potencial distribuível atual na esteira. Atualizado a cada geração do dashboard via BD_EnvioParceiros.'],
    ['VLR a Distribuir / Sem','Versão semanal do VLR a Distribuir: soma do ValorBruto de processos Em andamento enviados em uma semana específica. Usado no comparativo WoW (semana atual vs semana anterior).'],
    ['R$ Compra','Valor total de precatórios efetivamente comprados (pagos) vinculados ao parceiro. Base: BD_Pagos.'],
    ['Ticket Médio','R$ Compra ÷ Quantidade de processos pagos. Indica o valor médio por precatório adquirido.'],
    ['Taxa de Conversão','Pagos ÷ Leads × 100. Percentual de leads que se tornaram compra efetiva.'],
  ];
  document.getElementById('glossFinanceiro').innerHTML=financeiro.map(function(t){return '<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #F0F2F5"><span style="font-weight:600;min-width:160px;font-size:12px;flex-shrink:0">'+t[0]+'</span><span style="font-size:12px;color:var(--ce);line-height:1.5">'+t[1]+'</span></div>'}).join('');
})();

// ===== LISTA DE DADOS (ex-EXPLORADOR) =====
// ===== NAVEGACAO ENTRE ABAS COM FILTRO =====
function setMSCheck(wrapId,value){
  var wrap=document.getElementById(wrapId);
  if(!wrap)return;
  var cbs=wrap.querySelectorAll('input[type="checkbox"]');
  cbs.forEach(function(cb){cb.checked=false});
  if(value){
    cbs.forEach(function(cb){if(cb.value===value)cb.checked=true});
  }
}
function clearMSAll(wrapId){
  var wrap=document.getElementById(wrapId);
  if(!wrap)return;
  wrap.querySelectorAll('input[type="checkbox"]').forEach(function(cb){cb.checked=false});
  var labelMap={msCatDados:'Categorias',msSaudeDados:'Saúde',msRegionalDados:'Regional'};
  updateMSLabel(wrapId,labelMap[wrapId]||wrapId);
}
function goToList(cat,saude){
  document.getElementById('searchName').value='';
  clearMSAll('msCatDados');
  clearMSAll('msSaudeDados');
  clearMSAll('msRegionalDados');
  document.getElementById('dadosDateFrom').value='';
  document.getElementById('dadosDateTo').value='';
  if(cat)setMSCheck('msCatDados',cat);
  if(saude)setMSCheck('msSaudeDados',saude);
  updateMSLabel('msCatDados','Categorias');
  updateMSLabel('msSaudeDados','Saúde');
  document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active')});
  document.querySelectorAll('.pnl').forEach(function(p){p.classList.remove('active')});
  var listaTab=document.querySelector('.tab[data-tab="dados"]');
  var listaPnl=document.getElementById('p-dados');
  if(listaTab)listaTab.classList.add('active');
  if(listaPnl)listaPnl.classList.add('active');
  renderExp();
  window.scrollTo(0,0);
}

function goToPartner(nome){
  document.getElementById('searchName').value=nome;
  clearMSAll('msCatDados');
  clearMSAll('msSaudeDados');
  clearMSAll('msRegionalDados');
  document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active')});
  document.querySelectorAll('.pnl').forEach(function(p){p.classList.remove('active')});
  var listaTab=document.querySelector('.tab[data-tab="dados"]');
  var listaPnl=document.getElementById('p-dados');
  if(listaTab)listaTab.classList.add('active');
  if(listaPnl)listaPnl.classList.add('active');
  renderExp();
  window.scrollTo(0,0);
}

var eSort={col:'isp',asc:false};
var PO=['CRITICA','ALTA','MEDIA','BAIXA','OBSERVACAO'];
var COrd=['Diamante','Ouro','Prata','Bronze','Em Recuperação','Inativo','Fantasma'];
var SOrd=['Excelente','Bom','Regular','Ruim','Péssimo','Em Recuperação','N/A'];

function filterExplorer(){renderExp()}
function getFiltered(){
  var nm=document.getElementById('searchName').value.toLowerCase();
  var cats=getCheckedValues('msCatDados');
  var sds=getCheckedValues('msSaudeDados');
  var regs=getCheckedValues('msRegionalDados');
  var df=document.getElementById('dadosDateFrom').value;
  var dt=document.getElementById('dadosDateTo').value;
  return D.filter(function(p){
    if(nm&&p.nome.toLowerCase().indexOf(nm)===-1)return false;
    if(cats.length>0&&cats.indexOf(p.cat)===-1)return false;
    if(sds.length>0&&sds.indexOf(p.saude)===-1)return false;
    if(regs.length>0&&regs.indexOf(p.regional)===-1)return false;
    if(df&&p.data_primeiro_envio&&p.data_primeiro_envio<df)return false;
    if(dt&&p.data_ultimo_envio&&p.data_ultimo_envio>dt)return false;
    return true;
  });
}

function buildAnalise(p){
  var sit='';var mud='';var dir='';
  var parado=p.semanas_parado||0;
  var temPagos=p.pagos>0;
  var ticket=temPagos?Math.round(p.compra/p.pagos):0;
  var ativo=p.sem4>0;
  var catStr=p.cat;
  var nomeShort=p.nome.substring(0,25);

  // ---- SITUACAO ATUAL ----
  if(p.cat==='Fantasma'){
    sit='Parceiro com '+p.pagos+' processos pagos ('+fB(p.compra)+'), ticket '+fB(ticket)+', mas sem nenhum lead registrado na esteira. Opera fora do canal oficial.';
  } else if(!ativo&&parado>0&&temPagos){
    sit='Parceiro '+catStr+' parado h\u00e1 '+parado+' semanas. Possui '+p.pagos+' pagos hist\u00f3ricos ('+fB(p.compra)+'). \u00daltimo envio foi na semana '+(semAtual-parado)+'. ISP atual: '+p.isp+'/100 ('+p.saude+').';
  } else if(ativo&&temPagos){
    sit='Parceiro '+catStr+' ativo com '+p.sem4+' leads nas \u00faltimas 4 semanas. Acumula '+p.pagos+' processos pagos ('+fB(p.compra)+', ticket '+fB(ticket)+'). Convers\u00e3o de '+fP(p.taxa_conv)+'. ISP: '+p.isp+'/100.';
  } else if(ativo&&!temPagos){
    sit='Parceiro enviando leads ativamente ('+p.sem4+' nas \u00falt. 4 sem), por\u00e9m sem nenhuma compra at\u00e9 o momento. Total de '+p.leads+' leads em '+p.meses+' meses. Classificado como '+catStr+'.';
  } else {
    sit='Parceiro com '+p.leads+' leads hist\u00f3ricos em '+p.meses+' meses. '+(temPagos?p.pagos+' pagos ('+fB(p.compra)+').':'Sem compras.')+ ' Parado h\u00e1 '+(parado>0?parado+' semanas.':'tempo indeterminado.');
  }

  // ---- O QUE MUDOU ----
  if(p.tend<-50&&ativo){
    mud='Queda severa de '+Math.abs(Math.round(p.tend))+'% no volume de envio comparando as \u00faltimas 4 semanas com as 4 anteriores. Passou de um patamar mais alto para apenas '+p.sem4+' leads recentes. Sinal claro de desacelera\u00e7\u00e3o, poss\u00edvel perda de engajamento ou redirecionamento para concorr\u00eancia.';
  } else if(p.tend<-30&&ativo){
    mud='Redu\u00e7\u00e3o de '+Math.abs(Math.round(p.tend))+'% no volume de leads. Ainda ativo, mas com tend\u00eancia de queda que merece aten\u00e7\u00e3o. Se mantiver esse ritmo por mais 2-4 semanas, pode migrar para categoria de risco.';
  } else if(parado>0&&parado<=8&&temPagos){
    mud='Parou de enviar h\u00e1 '+parado+' semanas. Para um parceiro com hist\u00f3rico de '+p.pagos+' pagos e '+fB(p.compra)+' em compras, essa parada \u00e9 um alerta relevante. Quanto mais tempo sem contato, maior o risco de perda definitiva.';
  } else if(parado>8&&temPagos){
    mud='Inativo h\u00e1 '+parado+' semanas (+'+(Math.round(parado/4))+' meses). J\u00e1 ultrapassou o per\u00edodo razo\u00e1vel de pausa. Com '+p.pagos+' pagos hist\u00f3ricos ('+fB(p.compra)+'), representa valor em risco de perda permanente.';
  } else if(p.tend>50){
    mud='Crescimento expressivo de +'+Math.round(p.tend)+'% no volume de leads. Parceiro acelerando, o que indica potencial para subir de categoria ou converter mais se acompanhado de perto.';
  } else if(p.tend>20){
    mud='Tend\u00eancia positiva de +'+Math.round(p.tend)+'% nos envios recentes. Mant\u00e9m consist\u00eancia e pode estar ampliando capta\u00e7\u00e3o. Momento favor\u00e1vel para fortalecer relacionamento.';
  } else if(p.is_em_recuperacao){
    mud='Retomou envio de leads ap\u00f3s per\u00edodo de inatividade superior a 8 semanas. Parceiro em fase de readapta\u00e7\u00e3o \u2014 o comportamento das pr\u00f3ximas semanas vai definir se a retomada \u00e9 sustent\u00e1vel ou pontual.';
  } else if(!ativo&&!temPagos&&p.leads>=3){
    mud='Parceiro que j\u00e1 enviou '+p.leads+' leads mas parou completamente. Sem compras registradas. Pode ter desistido do canal ou redirecionado para outra empresa.';
  } else {
    mud='Sem mudan\u00e7a significativa no per\u00edodo. Comportamento est\u00e1vel dentro do padr\u00e3o esperado para a categoria.';
  }

  // ---- DIRECIONAMENTO ----
  if(p.cat==='Fantasma'){
    dir='Investigar por que o parceiro n\u00e3o usa a esteira. Se os leads passarem pelo canal oficial, a PJUS ganha visibilidade e controle sobre o funil. Sugest\u00e3o: reuni\u00e3o consultiva para apresentar benef\u00edcios da esteira.';
  } else if(p.cat==='Diamante'&&p.tend<-30){
    dir='A\u00e7\u00e3o imediata. Parceiro estrat\u00e9gico com hist\u00f3rico relevante apresentando queda. Recomenda-se contato direto em at\u00e9 48h para entender gargalos. Investigar: mudan\u00e7a de equipe, insatisfa\u00e7\u00e3o, concorr\u00eancia ou altera\u00e7\u00e3o no mix de produtos.';
  } else if(p.cat==='Diamante'&&parado>0){
    dir='Alerta m\u00e1ximo. Parceiro Diamante parado \u00e9 perda cr\u00edtica. Acionar gest\u00e3o de conta para contato urgente. Cada semana sem a\u00e7\u00e3o aumenta o risco de migra\u00e7\u00e3o para concorrente.';
  } else if(p.cat==='Prata'&&p.tend<-30){
    dir='Contato proativo recomendado. Parceiro com hist\u00f3rico de compra em desacelera\u00e7\u00e3o. Antes que a queda se consolide, buscar entendimento: o que mudou na opera\u00e7\u00e3o dele? H\u00e1 algum gargalo que a PJUS pode resolver?';
  } else if(p.cat==='Inativo'&&temPagos){
    dir='Reativa\u00e7\u00e3o necess\u00e1ria. Parceiro com '+fB(p.compra)+' em compras hist\u00f3ricas. A cada semana parado, a probabilidade de retorno diminui. Abordagem sugerida: contato consultivo, n\u00e3o comercial.';
  } else if(p.cat==='Bronze'&&p.leads>=20){
    dir='Parceiro com alto volume de envio ('+p.leads+' leads) e zero convers\u00e3o. Auditar qualidade dos leads enviados. Se o perfil for compat\u00edvel, investir em acompanhamento para destravar primeira compra. Primeira convers\u00e3o \u00e9 o ponto de virada.';
  } else if(p.cat==='Em Recuperação'){
    dir='Monitorar de perto nas pr\u00f3ximas 4 semanas. Se mantiver envio consistente, reclassificar. Se parar novamente, retirar do foco ativo.';
  } else if(p.tend>20&&temPagos){
    dir='Momento favor\u00e1vel para aprofundar parceria. Parceiro em crescimento e com hist\u00f3rico de convers\u00e3o. Avaliar se h\u00e1 espa\u00e7o para ampliar escopo ou volume.';
  } else if(p.tend>20&&!temPagos){
    dir='Parceiro em alta mas sem convers\u00e3o. Priorizar acompanhamento da qualidade dos leads para converter a primeira compra.';
  } else {
    dir='Manter monitoramento peri\u00f3dico. Sem a\u00e7\u00e3o urgente, mas acompanhar nas pr\u00f3ximas semanas para detectar mudan\u00e7as de padr\u00e3o.';
  }

  return {situacao:sit,mudanca:mud,direcao:dir};
}

function renderExp(){
  var fd=getFiltered();
  var sorted=fd.slice().sort(function(a,b){
    var va=a[eSort.col],vb=b[eSort.col];
    if(eSort.col==='cat'){va=COrd.indexOf(va);vb=COrd.indexOf(vb)}
    if(eSort.col==='regional'){va=REG_LIST.indexOf(va);vb=REG_LIST.indexOf(vb)}
    if(eSort.col==='saude'){va=SOrd.indexOf(va);vb=SOrd.indexOf(vb)}
    if(typeof va==='string')va=va.toLowerCase();
    if(typeof vb==='string')vb=vb.toLowerCase();
    if(va<vb)return eSort.asc?-1:1;if(va>vb)return eSort.asc?1:-1;return 0;
  });
  document.getElementById('expInfo').textContent=sorted.length+' de '+D.length+' parceiros';
  document.getElementById('expBody').innerHTML=sorted.map(function(p,i){
    var rc='';
    var rid='x_'+i;
    var flags=[];
    if(p.is_novo)flags.push('Novo');
    if(p.is_em_recuperacao)flags.push('Em Recuperação');
    if(p.is_sazonal)flags.push('Sazonal');
    if(p.is_fantasma)flags.push('Fantasma');
    var flagStr=flags.length>0?flags.join(', '):'--';
    var tk=p.pagos>0?fB(Math.round(p.compra/p.pagos)):'--';
    var conv=p.leads>0&&p.pagos>0?(p.taxa_conv.toFixed(1)+'%'):'--';
    var regBd='<span class="bd" style="background:'+(REG_COLORS[p.regional]||'#B0B0B0')+';color:'+(p.regional==='SP (C/D)'||p.regional==='N/I'?'#333':'#fff')+'">'+p.regional+'</span>';
    var vdStr=p.vlr_dist>0?'<span style="font-size:11px;font-weight:700;color:#805ad5">'+fB(p.vlr_dist)+'</span>':'<span style="color:#ccc">--</span>';
    var _cs=calcChurnScore(p);
    var _csCls=_cs>=60?'alto':_cs>=30?'medio':'baixo';
    var _csIcon=_cs>=60?'\u{1F534}':_cs>=30?'\u{1F7E1}':'\u{1F7E2}';
    var churnCell='<span class="churn-badge '+_csCls+'">'+_csIcon+' '+_cs+'</span>';
    var r='<tr class="'+rc+'" style="cursor:pointer" onclick="toggleX(\''+rid+'\')"><td><strong>'+p.nome+'</strong></td><td>'+catBd(p.cat)+'</td><td>'+regBd+'</td><td>'+(p.isp===-1?'--':p.isp)+'</td><td>'+sauBd(p.saude)+'</td><td>'+fN(p.leads)+'</td><td>'+fN(p.sem4)+'</td><td>'+fN(p.pagos)+'</td><td>'+tk+'</td><td>'+conv+'</td><td>'+tA(p.tend)+'</td><td>'+vdStr+'</td><td>'+churnCell+'</td><td>'+buildSparkVis(p)+'</td></tr>';
    // Gerar analise conclusiva
    var analise=buildAnalise(p);
    r+='<tr class="exr" id="'+rid+'"><td colspan="14"><div class="exc" style="display:grid;grid-template-columns:1fr 1fr;gap:16px">';
    // Coluna 1: Situacao e Contexto
    r+='<div style="display:flex;flex-direction:column;gap:10px">';
    r+='<div style="background:#F7FAFC;padding:10px 14px;border-radius:8px;border-left:3px solid var(--az)"><div class="fl" style="color:var(--az);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">\u{1F4CA} Situação Atual</div><div class="fv" style="font-size:12px;line-height:1.5">'+analise.situacao+'</div></div>';
    r+='<div style="background:#F7FAFC;padding:10px 14px;border-radius:8px;border-left:3px solid #ECC94B"><div class="fl" style="color:#B7791F;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">\u{1F50D} O que mudou</div><div class="fv" style="font-size:12px;line-height:1.5">'+analise.mudanca+'</div></div>';
    r+='<div style="background:#F0FFF4;padding:10px 14px;border-radius:8px;border-left:3px solid var(--vd)"><div class="fl" style="color:var(--vd);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">\u{1F3AF} Direcionamento</div><div class="fv" style="font-size:12px;line-height:1.5;font-weight:500">'+analise.direcao+'</div></div>';
    // BENCHMARK UF
    var _bench=calcBenchmarkUF(p);
    if(_bench){
      r+='<div class="bench-box"><h5>&#x1F4CA; Benchmark na UF '+p.uf+' ('+_bench.peers_n+' pares)</h5>';
      r+='<div class="bench-grid">';
      var _ispPct=Math.round(_bench.isp_pct);
      var _ispDir=_ispPct>=50?'bk-up \u2191':'bk-down \u2193';
      r+='<div class="bench-kpi"><div class="bk-label">ISP</div><div class="bk-value">'+(p.isp>=0?p.isp:'--')+'</div><div class="bk-sub"><span class="'+_ispDir+'">'+_ispPct+'% da UF</span> (med: '+Math.round(_bench.isp_med)+')</div></div>';
      var _l4Pct=Math.round(_bench.l4_pct);
      var _l4Dir=_l4Pct>=50?'bk-up \u2191':'bk-down \u2193';
      r+='<div class="bench-kpi"><div class="bk-label">Leads 4sem</div><div class="bk-value">'+p.sem4+'</div><div class="bk-sub"><span class="'+_l4Dir+'">'+_l4Pct+'% da UF</span> (med: '+Math.round(_bench.l4_med)+')</div></div>';
      r+='</div></div>';
    }
    // SAZONALIDADE PROJETADA
    var _sproj=calcSazonProjecao(p);
    var _hasProj=_sproj.some(function(s){return s.base!==null});
    if(_hasProj){
      r+='<div class="sazon-box"><h5>&#x1F4C5; Sazonalidade Projetada (pr\u00f3ximas 4 semanas)</h5>';
      r+='<table class="sazon-table"><thead><tr><th>Semana</th><th>Base ano ant.</th><th>Projetado</th></tr></thead><tbody>';
      _sproj.forEach(function(s){
        var baseStr=s.base!==null?fN(s.base):'sem hist\u00f3rico';
        var projStr=s.base!==null?('~'+fN(s.base)+' leads'):'--';
        r+='<tr><td>'+s.sem+'</td><td>'+baseStr+'</td><td style="font-weight:700;color:var(--ae)">'+projStr+'</td></tr>';
      });
      r+='</tbody></table></div>';
    }
    // MOTIVOS DE REPROVACAO
    if(p.top_motivos&&p.top_motivos.length){
      r+='<div class="motivos-box"><h5>&#x274C; Top Motivos de Reprova\u00e7\u00e3o</h5>';
      p.top_motivos.forEach(function(m){
        r+='<div class="motivo-item"><span class="motivo-label">'+m[0]+'</span><span class="motivo-cnt">'+m[1]+'x</span></div>';
      });
      r+='</div>';
    }
    r+='</div>';
    // Coluna 2: Indicadores e ISP
    r+='<div style="display:flex;flex-direction:column;gap:10px">';
    r+='<div style="background:#F7FAFC;padding:10px 14px;border-radius:8px"><div class="fl" style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">\u{1F4C8} Indicadores-chave</div>';
    r+='<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:11px">';
    r+='<div><span style="color:#7A8599">Leads total:</span> <strong>'+fN(p.leads)+'</strong></div>';
    r+='<div><span style="color:#7A8599">Leads 4 sem:</span> <strong>'+fN(p.sem4)+'</strong></div>';
    r+='<div><span style="color:#7A8599">Pagos:</span> <strong>'+fN(p.pagos)+'</strong></div>';
    r+='<div><span style="color:#7A8599">R$ Compra:</span> <strong>'+fB(p.compra)+'</strong></div>';
    r+='<div><span style="color:#7A8599">Ticket:</span> <strong>'+(p.pagos>0?fB(Math.round(p.compra/p.pagos)):'--')+'</strong></div>';
    r+='<div><span style="color:#7A8599">Conversão:</span> <strong>'+fP(p.taxa_conv)+'</strong></div>';
    r+='<div><span style="color:#7A8599">Meses ativos:</span> <strong>'+p.meses+'</strong></div>';
    r+='<div><span style="color:#7A8599">Envio:</span> <strong>'+(p.envio_class||'--')+'</strong></div>';
    r+='<div style="grid-column:span 2"><span style="color:#805ad5;font-weight:700">VLR a Distribuir:</span> <strong style="color:#805ad5">'+(p.vlr_dist>0?fB(p.vlr_dist):'--')+'</strong> <span style="color:#7A8599;font-size:10px">(em andamento, ex-MID)</span></div>';
    r+='</div></div>';
    // ISP Breakdown
    r+='<div style="background:#F7FAFC;padding:10px 14px;border-radius:8px"><div class="fl" style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">\u{1F9E9} ISP '+p.isp+'/100</div>';
    r+='<div style="display:flex;gap:4px;flex-wrap:wrap">';
    var ispParts=[['Rec\u00eancia',p.isp_rec,25],['Produção',p.isp_prod,25],['Volume',p.isp_vol,20],['Consist\u00eancia',p.isp_cons,15],['Tend\u00eancia',p.isp_tend,10],['Valor',p.isp_val,5]];
    ispParts.forEach(function(ip){
      var v=ip[1]!=null?ip[1]:0;
      var mx=ip[2];
      var pct=mx>0?Math.round(v/mx*100):0;
      var cor=pct>=75?'var(--vd)':pct>=50?'var(--az)':pct>=25?'#ECC94B':'var(--danger)';
      r+='<div style="flex:1;min-width:80px;background:#fff;padding:6px 8px;border-radius:6px;text-align:center;border:1px solid #E8EDF2"><div style="font-size:9px;color:#7A8599">'+ip[0]+'</div><div style="font-size:13px;font-weight:700;color:'+cor+'">'+v+'/'+mx+'</div></div>';
    });
    r+='</div></div>';
    if(flagStr!=='--'){r+='<div style="font-size:10px;color:#7A8599;padding:4px 8px"><strong>Flags:</strong> '+flagStr+'</div>'}
    // CHURN SCORE
    r+='<div class="bench-box" style="background:#FFF5F5;border-color:#FED7D7"><h5 style="color:#9B2C2C">&#x26A0; Score de Risco de Churn</h5>';
    r+='<div style="display:flex;align-items:center;gap:12px;padding:4px 0">';
    r+='<div style="font-size:36px;font-weight:900;color:'+(_cs>=60?'#E05353':_cs>=30?'#F5A623':'#38a169')+'">'+_cs+'</div>';
    r+='<div style="font-size:11px;color:#7A8599;line-height:1.6">';
    r+='<div>Tend\u00eancia: <strong>'+(p.tend<-20?'Queda acentuada':p.tend<0?'Queda leve':p.tend>10?'Alta':'\u2014')+'</strong></div>';
    r+='<div>Semanas parado: <strong>'+(p.semanas_parado||0)+'</strong></div>';
    r+='<div>Sazon\u00e1l: <strong>'+(p.is_sazonal?'Sim (desconto aplicado)':'N\u00e3o')+'</strong></div>';
    r+='</div></div></div>';
    r+='</div>';
    // CRM MOCKUP
    r+='<div class="crm-mock-box">';
    r+='<div class="crm-mock-header">\uD83D\uDCCB Hist\u00f3rico CRM <span class="crm-badge-tag">Em breve</span></div>';
    r+='<div class="crm-mock-grid">';
    r+='<div class="crm-field"><label>\u00daltimo Contato</label><span>\u2014</span></div>';
    r+='<div class="crm-field"><label>Respons\u00e1vel</label><span>\u2014</span></div>';
    r+='<div class="crm-field"><label>Canal</label><span>\u2014</span></div>';
    r+='<div class="crm-field"><label>Resultado</label><span>\u2014</span></div>';
    r+='</div>';
    r+='<div class="crm-note">\u26a1 Integra\u00e7\u00e3o CRM em andamento. Dados ser\u00e3o populados automaticamente.</div>';
    r+='</div>';
    r+='</div>';
    r+='</div></td></tr>';
    return r;
  }).join('');
}

function toggleX(rid){var r=document.getElementById(rid);if(!r)return;if(r.classList.contains('open')){r.classList.remove('open')}else{document.querySelectorAll('.exr.open').forEach(function(x){x.classList.remove('open')});r.classList.add('open')}}

document.getElementById('searchName').addEventListener('input',renderExp);
document.querySelectorAll('#expTable thead th[data-col]').forEach(function(th){
  th.addEventListener('click',function(){
    var c=th.dataset.col;
    if(eSort.col===c)eSort.asc=!eSort.asc;else{eSort.col=c;eSort.asc=true}
    renderExp();
  });
});
function resetFilters(){
  document.getElementById('searchName').value='';
  clearMSAll('msCatDados');
  clearMSAll('msSaudeDados');
  clearMSAll('msRegionalDados');
  document.getElementById('dadosDateFrom').value='';
  document.getElementById('dadosDateTo').value='';
  renderExp();
}
function exportCSV(){
  var f=getFiltered();
  var h=['Nome','Categoria','UF','Regional','ISP','ISP_Rec','ISP_Prod','ISP_Vol','ISP_Cons','ISP_Tend','ISP_Val','Saude','Leads','Sem4','Pagos','Compra','Ticket','Tendência','Taxa Conv','Envio','Diagnostico','Acao'];
  var rows=f.map(function(p){return ['"'+p.nome+'"',p.cat,p.uf||'',p.regional||'',p.isp,p.isp_rec,p.isp_prod,p.isp_vol,p.isp_cons,p.isp_tend,p.isp_val,p.saude,p.leads,p.sem4,p.pagos,p.compra,p.ticket,p.tend,p.taxa_conv,p.envio_class||'','"'+(p.diagnostico||'').replace(/"/g,'""')+'"','"'+(p.acao||'').replace(/"/g,'""')+'"'].join(';')});
  var csv=h.join(';')+'\n'+rows.join('\n');
  var blob=new Blob([csv],{type:'text/csv;charset=utf-8;'});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a');a.href=url;a.download='parceiros_export.csv';a.click();
  URL.revokeObjectURL(url);showToast('CSV exportado!');
}
renderExp();

// ===== NAME AUTOCOMPLETE =====
function setupNameAutocomplete(inputId, suggestId, onSelectFn) {
  var inp = document.getElementById(inputId);
  var sug = document.getElementById(suggestId);
  if(!inp || !sug) return;

  function showSuggestions() {
    var q = inp.value.toLowerCase().trim();
    sug.innerHTML = '';
    if(q.length < 1) { sug.style.display='none'; return; }
    var matches = D.filter(function(p){ return p.nome.toLowerCase().indexOf(q) >= 0; })
      .sort(function(a,b){
        var as = a.nome.toLowerCase().startsWith(q) ? 0 : 1;
        var bs = b.nome.toLowerCase().startsWith(q) ? 0 : 1;
        return as - bs || a.nome.localeCompare(b.nome);
      }).slice(0, 10);
    if(matches.length === 0) { sug.style.display='none'; return; }
    matches.forEach(function(p) {
      var item = document.createElement('div');
      item.className = 'name-suggest-item';
      // highlight matching part
      var nm = p.nome;
      var idx = nm.toLowerCase().indexOf(q);
      var hl = idx >= 0
        ? nm.slice(0,idx)+'<mark style="background:#d6eaff;padding:0">'+nm.slice(idx,idx+q.length)+'</mark>'+nm.slice(idx+q.length)
        : nm;
      item.innerHTML = '<span class="ns-name">'+hl+'</span><span class="ns-cat">'+p.cat+'</span>';
      item.addEventListener('mousedown', function(e) {
        e.preventDefault();
        inp.value = p.nome;
        sug.style.display = 'none';
        onSelectFn();
      });
      sug.appendChild(item);
    });
    sug.style.display = 'block';
  }

  inp.addEventListener('input', showSuggestions);
  inp.addEventListener('focus', showSuggestions);
  inp.addEventListener('blur', function() {
    setTimeout(function(){ sug.style.display='none'; }, 180);
  });
  inp.addEventListener('keydown', function(e) {
    if(e.key === 'Escape') { sug.style.display='none'; }
    if(e.key === 'Enter') { sug.style.display='none'; onSelectFn(); }
  });
}
setupNameAutocomplete('gfNome', 'gfNomeSuggest', applyGlobalFilters);
setupNameAutocomplete('searchName', 'searchNameSuggest', renderExp);

// ===== CHATBOT =====
document.getElementById('chatToggle').addEventListener('click',function(){
  document.getElementById('chatPanel').classList.toggle('open');
});
document.getElementById('chatClose').addEventListener('click',function(){
  document.getElementById('chatPanel').classList.remove('open');
});
document.getElementById('chatInput').addEventListener('keydown',function(e){
  if(e.key==='Enter')sendChat();
});
function sendChat(){
  var input=document.getElementById('chatInput');
  var msg=input.value.trim();
  if(!msg)return;
  var body=document.getElementById('chatBody');
  var now=new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'});
  body.innerHTML+='<div class="chat-msg user"><div class="bubble">'+msg+'</div><div class="time" style="text-align:right">'+now+'</div></div>';
  input.value='';
  setTimeout(function(){
    var resp='Ainda estou em treinamento! Em breve vou poder te ajudar com consultas sobre parceiros, histórico e análises. Fica ligado!';
    var ml=msg.toLowerCase();
    if(ml.indexOf('critico')>-1||ml.indexOf('alerta')>-1){
      resp='Temos '+CR.length+' parceiros em prioridade critica ou alta. Os principais sao: '+CR.slice(0,3).map(function(p){return p.nome}).join(', ')+'. Quer saber mais sobre algum deles?';
    } else if(ml.indexOf('diamante')>-1){
      var dias=NF.filter(function(p){return p.cat==='Diamante'});
      if(dias.length>0){dias.sort(function(a,b){return b.compra-a.compra});resp='Temos '+dias.length+' parceiros Diamante. O maior eh '+dias[0].nome+' com '+fB(dias[0].compra)+' em compras.';}
      else{resp='Nenhum parceiro Diamante encontrado na base atual.';}
    } else if(ml.indexOf('fantasma')>-1){
      resp='Temos '+FN.length+' parceiros Fantasma (compram mas nao usam a esteira). Valor total: '+fB(FN.reduce(function(s,p){return s+p.compra},0))+'.';
    } else if(ml.indexOf('top')>-1||ml.indexOf('melhor')>-1){
      if(topCompra.length>=3)resp='Top 3 parceiros por compra: 1) '+topCompra[0].nome+' '+fB(topCompra[0].compra)+', 2) '+topCompra[1].nome+' '+fB(topCompra[1].compra)+', 3) '+topCompra[2].nome+' '+fB(topCompra[2].compra);
      else resp='Poucos parceiros com compras registradas.';
    } else if(ml.indexOf('isp')>-1){
      resp='O ISP medio da base (excluindo Fantasmas) eh '+ispMédio+'. Os componentes sao: Recência, Produção, Volume, Consistência, Tendência e Valor.';
    }
    body.innerHTML+='<div class="chat-msg bot"><div class="bubble">'+resp+'</div><div class="time">'+now+'</div></div>';
    body.scrollTop=body.scrollHeight;
  },600);
  body.scrollTop=body.scrollHeight;
}
"""

# ====================================================================
# ASSEMBLE
# ====================================================================
js_final = JS.replace("__DATA__", json_str).replace("__HOJE__", hoje)

# Replace placeholders in HTML body
html_body_final = HTML_BODY.replace("__LOGO__", logo_b64).replace("__AVATAR__", AVATAR_IMG).replace("__AVATAR_BTN__", AVATAR_BTN_IMG)

output = '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n'
output += '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
output += '<title>E aí, meu parça - PJUS</title>\n'
output += '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">\n'
output += '<style>' + CSS + '</style>\n'
output += '</head>\n<body>\n'
output += html_body_final
output += '\n<script>\n' + js_final + '\n</script>\n'
output += '</body>\n</html>'

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(output)

print(f"HTML v2 gerado: {OUT_PATH}")
print(f"Tamanho: {len(output):,} chars")

# ====================================================================
# ABRIR HTML NO BROWSER AUTOMATICAMENTE
# ====================================================================
import webbrowser as _wb
_wb.open(OUT_PATH)

# ====================================================================
# AUTO-SAVE NO GITHUB
# ====================================================================
import subprocess, sys, os

def _git_push_github():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    semana_label = hoje  # já definido como string "YYYY-MM-DD"
    msg = f"auto: dashboard atualizado em {semana_label}"
    try:
        # Adiciona apenas os arquivos principais (evita subir dados sensíveis acidentalmente)
        files = ["e_ai_meu_parca.html", "_build_v2.py", "_reclassificar_v3.py", "parceiros_data.json"]
        existing = [f for f in files if os.path.exists(os.path.join(repo_dir, f))]
        subprocess.run(["git", "add"] + existing, cwd=repo_dir, check=True)
        # Verifica se há algo para commitar
        status = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir,
                                capture_output=True, text=True)
        if not status.stdout.strip():
            print("GitHub: nenhuma alteração nova para commitar.")
            return
        subprocess.run(["git", "commit", "-m", msg], cwd=repo_dir, check=True)
        subprocess.run(["git", "push", "origin", "master:main"], cwd=repo_dir, check=True)
        print(f"[OK] GitHub atualizado: {msg}")
    except subprocess.CalledProcessError as e:
        print(f"[AVISO] Erro ao salvar no GitHub: {e}")
    except FileNotFoundError:
        print("[AVISO] Git nao encontrado no PATH. Instale o Git para habilitar auto-save.")

_git_push_github()
