"""
SOC Dashboard — FastAPI + WebSocket
Projeto 3: Filtrando e Agrupando
"""

import os
import asyncio
import json
import bcrypt
import pandas as pd
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import JWTError, jwt
from dotenv import load_dotenv

from banco import iniciar_banco, AtaquesRepo, AlertasRepo, engine
from alertas import verificar_e_persistir
from dados import gerar_dados
from sqlalchemy import text

load_dotenv()

SECRET   = os.environ["SOC_SECRET_KEY"]
HASH     = os.environ["SOC_SENHA_HASH"].encode("utf-8")
USERNAME = os.environ["SOC_USERNAME"]
PORT     = int(os.environ.get("PORT", 8000))

app = FastAPI(title="SOC Dashboard")

# ── Banco + dados iniciais ──────────────────────────────────
iniciar_banco()
with engine.connect() as c:
    total = c.execute(text("SELECT COUNT(*) FROM ataques")).scalar()

if total == 0:
    print("Carregando dados simulados...")
    AtaquesRepo().inserir(gerar_dados(1000))
    print("1000 eventos carregados.")

# ── WebSocket manager ───────────────────────────────────────
class WSManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, data: dict):
        for ws in list(self.active):
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                self.disconnect(ws)

manager = WSManager()

# ── Auth ────────────────────────────────────────────────────
def criar_token(username: str) -> str:
    exp = datetime.utcnow() + timedelta(hours=8)
    return jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm="HS256")

def token_valido(token: str) -> bool:
    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
        return True
    except JWTError:
        return False

def autenticado(request: Request) -> bool:
    token = request.cookies.get("soc_token")
    return bool(token and token_valido(token))

# ── Login HTML ──────────────────────────────────────────────
LOGIN_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SOC — Acesso Seguro</title>
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      background: #080812;
      color: #e0e0e0;
      font-family: 'Segoe UI', 'Courier New', monospace;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-image: radial-gradient(ellipse at 20% 50%, #1a0010 0%, transparent 50%),
                        radial-gradient(ellipse at 80% 20%, #000d1a 0%, transparent 50%);
    }}
    .container {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 32px;
    }}
    .marca {{
      text-align: center;
    }}
    .marca .sigla {{
      font-size: 3rem;
      font-weight: 900;
      letter-spacing: 8px;
      color: #ff003c;
      text-shadow: 0 0 30px #ff003c88;
    }}
    .marca .subtitulo {{
      font-size: 0.7rem;
      letter-spacing: 4px;
      color: #555;
      margin-top: 4px;
    }}
    .box {{
      background: #10101e;
      border: 1px solid #ff003c44;
      border-radius: 12px;
      padding: 40px 44px;
      width: 380px;
      box-shadow: 0 0 60px #ff003c18, inset 0 1px 0 #ffffff08;
    }}
    .box h2 {{
      font-size: 0.8rem;
      letter-spacing: 3px;
      color: #555;
      margin-bottom: 28px;
      text-transform: uppercase;
    }}
    .campo {{
      margin-bottom: 16px;
    }}
    .campo label {{
      display: block;
      font-size: 0.7rem;
      letter-spacing: 2px;
      color: #666;
      margin-bottom: 6px;
      text-transform: uppercase;
    }}
    .campo input {{
      width: 100%;
      background: #080812;
      border: 1px solid #1e1e30;
      border-radius: 6px;
      color: #e0e0e0;
      padding: 12px 16px;
      font-family: inherit;
      font-size: 0.9rem;
      outline: none;
      transition: border-color .2s;
    }}
    .campo input:focus {{
      border-color: #ff003c;
      box-shadow: 0 0 0 3px #ff003c18;
    }}
    button {{
      width: 100%;
      background: #ff003c;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 13px;
      font-family: inherit;
      font-size: 0.85rem;
      font-weight: 600;
      letter-spacing: 3px;
      cursor: pointer;
      margin-top: 8px;
      transition: background .2s, box-shadow .2s;
      text-transform: uppercase;
    }}
    button:hover {{
      background: #cc0030;
      box-shadow: 0 4px 20px #ff003c44;
    }}
    .erro {{
      background: #ff003c15;
      border: 1px solid #ff003c44;
      border-radius: 6px;
      color: #ff003c;
      font-size: 0.78rem;
      padding: 10px 14px;
      margin-bottom: 16px;
      letter-spacing: 0.5px;
    }}
    .rodape {{
      font-size: 0.65rem;
      color: #333;
      letter-spacing: 2px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="marca">
      <div class="sigla">SOC</div>
      <div class="subtitulo">Centro de Operações de Segurança</div>
    </div>
    <div class="box">
      <h2>Autenticação Requerida</h2>
      {erro}
      <form method="POST" action="/login">
        <div class="campo">
          <label>Usuário</label>
          <input type="text" name="username" placeholder="Digite seu usuário" required autofocus>
        </div>
        <div class="campo">
          <label>Senha</label>
          <input type="password" name="password" placeholder="••••••••••••">
        </div>
        <button type="submit">Entrar no Sistema</button>
      </form>
    </div>
    <div class="rodape">Acesso restrito — somente pessoal autorizado</div>
  </div>
</body>
</html>"""

# ── Dashboard HTML ──────────────────────────────────────────
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SOC Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      background: #080812;
      color: #c8c8d4;
      font-family: 'Segoe UI', 'Courier New', monospace;
      min-height: 100vh;
    }

    /* ── Header ─────────────────────────────────────────── */
    header {
      background: #10101e;
      border-bottom: 1px solid #ff003c66;
      padding: 0 28px;
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 20px #ff003c18;
    }

    .header-esq {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .logo {
      font-size: 1.4rem;
      font-weight: 900;
      letter-spacing: 4px;
      color: #ff003c;
      text-shadow: 0 0 20px #ff003c66;
    }

    .header-titulo {
      font-size: 0.75rem;
      letter-spacing: 2px;
      color: #444;
      text-transform: uppercase;
      border-left: 1px solid #222;
      padding-left: 20px;
    }

    .header-dir {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .relogio {
      font-size: 0.8rem;
      color: #555;
      letter-spacing: 1px;
    }

    .status-ws {
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 0.72rem;
      letter-spacing: 1px;
    }

    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }
    .dot.verde    { background: #00ff88; box-shadow: 0 0 8px #00ff88; }
    .dot.vermelho { background: #ff003c; box-shadow: 0 0 8px #ff003c; }

    .btn-sair {
      background: none;
      border: 1px solid #ff003c44;
      border-radius: 6px;
      color: #ff003c;
      font-family: inherit;
      font-size: 0.72rem;
      letter-spacing: 2px;
      padding: 6px 14px;
      cursor: pointer;
      text-decoration: none;
      transition: all .2s;
    }
    .btn-sair:hover { background: #ff003c18; border-color: #ff003c; }

    /* ── Seções ──────────────────────────────────────────── */
    .secao {
      padding: 24px 28px 0;
    }

    .secao-titulo {
      font-size: 0.65rem;
      letter-spacing: 3px;
      color: #444;
      text-transform: uppercase;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .secao-titulo::after {
      content: '';
      flex: 1;
      height: 1px;
      background: linear-gradient(to right, #2a2a4a, transparent);
    }

    /* ── Cards KPI ───────────────────────────────────────── */
    .cards {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }

    .card {
      background: #10101e;
      border: 1px solid #1e1e30;
      border-radius: 10px;
      padding: 22px 20px;
      position: relative;
      overflow: hidden;
      transition: border-color .2s;
    }

    .card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
      background: #1e1e30;
    }

    .card.verde::before  { background: #00ff88; }
    .card.azul::before   { background: #0099ff; }
    .card.amarelo::before{ background: #ff9900; }
    .card.vermelho::before{ background: #ff003c; }

    .card-icone {
      font-size: 1.5rem;
      margin-bottom: 12px;
      opacity: 0.7;
    }

    .card-valor {
      font-size: 2.6rem;
      font-weight: 700;
      line-height: 1;
      margin-bottom: 6px;
    }

    .card.verde   .card-valor { color: #00ff88; }
    .card.azul    .card-valor { color: #0099ff; }
    .card.amarelo .card-valor { color: #ff9900; }
    .card.vermelho .card-valor{ color: #ff003c; }

    .card-label {
      font-size: 0.65rem;
      letter-spacing: 2px;
      color: #555;
      text-transform: uppercase;
    }

    .card-sub {
      font-size: 0.7rem;
      color: #333;
      margin-top: 8px;
    }

    /* ── Gráficos ────────────────────────────────────────── */
    .graficos {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      padding: 24px 28px 0;
    }

    .grafico-box {
      background: #10101e;
      border: 1px solid #1e1e30;
      border-radius: 10px;
      padding: 4px;
    }

    /* ── Tabela de Alertas ───────────────────────────────── */
    .alertas-box {
      margin: 24px 28px;
      background: #10101e;
      border: 1px solid #1e1e30;
      border-radius: 10px;
      overflow: hidden;
    }

    .alertas-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      border-bottom: 1px solid #1e1e30;
    }

    .alertas-header h2 {
      font-size: 0.7rem;
      letter-spacing: 3px;
      color: #555;
      text-transform: uppercase;
    }

    .alertas-header .contador {
      font-size: 0.7rem;
      color: #ff003c;
      background: #ff003c18;
      border: 1px solid #ff003c44;
      border-radius: 20px;
      padding: 2px 10px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    thead th {
      font-size: 0.65rem;
      letter-spacing: 2px;
      color: #444;
      text-transform: uppercase;
      padding: 10px 20px;
      text-align: left;
      background: #0c0c18;
      border-bottom: 1px solid #1e1e30;
    }

    tbody td {
      padding: 12px 20px;
      font-size: 0.82rem;
      border-bottom: 1px solid #0c0c18;
      vertical-align: middle;
    }

    tbody tr:last-child td { border-bottom: none; }
    tbody tr:hover td { background: #13132a; }

    .badge {
      display: inline-block;
      padding: 3px 10px;
      border-radius: 4px;
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 1px;
    }
    .badge.CRITICO { background: #ff003c22; color: #ff003c; border: 1px solid #ff003c44; }
    .badge.AVISO   { background: #ff990022; color: #ff9900; border: 1px solid #ff990044; }
    .badge.INFO    { background: #0099ff22; color: #0099ff; border: 1px solid #0099ff44; }

    .td-mensagem { color: #aaa; }
    .td-regra    { color: #555; font-size: 0.75rem; }

    .btn-resolver {
      background: none;
      border: 1px solid #00ff8844;
      border-radius: 5px;
      color: #00ff88;
      padding: 4px 12px;
      cursor: pointer;
      font-family: inherit;
      font-size: 0.72rem;
      letter-spacing: 1px;
      transition: all .2s;
    }
    .btn-resolver:hover {
      background: #00ff8818;
      border-color: #00ff88;
    }

    .sem-alertas {
      text-align: center;
      padding: 32px;
      color: #333;
      font-size: 0.8rem;
      letter-spacing: 2px;
    }

    /* ── Toast ───────────────────────────────────────────── */
    .toast {
      position: fixed;
      bottom: 28px;
      right: 28px;
      background: #10101e;
      border: 1px solid #ff003c;
      border-radius: 8px;
      padding: 14px 20px;
      font-size: 0.82rem;
      display: none;
      z-index: 999;
      max-width: 360px;
      box-shadow: 0 4px 30px #ff003c44;
      animation: slidein .3s ease;
    }

    .toast-nivel {
      font-size: 0.65rem;
      letter-spacing: 2px;
      color: #ff003c;
      margin-bottom: 4px;
    }

    @keyframes slidein {
      from { opacity: 0; transform: translateY(10px); }
      to   { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>

<!-- Header -->
<header>
  <div class="header-esq">
    <div class="logo">SOC</div>
    <div class="header-titulo">Monitor de Ataques Cibernéticos — DDoS</div>
  </div>
  <div class="header-dir">
    <div class="relogio" id="relogio"></div>
    <div class="status-ws">
      <span class="dot vermelho" id="dot"></span>
      <span id="ws-label">Conectando...</span>
    </div>
    <a href="/logout" class="btn-sair">Sair</a>
  </div>
</header>

<!-- KPIs -->
<div class="secao" style="padding-top:24px;">
  <div class="secao-titulo">Indicadores em Tempo Real</div>
  <div class="cards">
    <div class="card verde">
      <div class="card-icone">⚡</div>
      <div class="card-valor" id="c-ataques">—</div>
      <div class="card-label">Ataques na Última Hora</div>
      <div class="card-sub">Todos os tipos combinados</div>
    </div>
    <div class="card vermelho">
      <div class="card-icone">🚨</div>
      <div class="card-valor" id="c-criticos">—</div>
      <div class="card-label">Alertas Críticos</div>
      <div class="card-sub">Requerem ação imediata</div>
    </div>
    <div class="card amarelo">
      <div class="card-icone">⚠</div>
      <div class="card-valor" id="c-abertos">—</div>
      <div class="card-label">Alertas em Aberto</div>
      <div class="card-sub">Aguardando resolução</div>
    </div>
    <div class="card azul">
      <div class="card-icone">🌐</div>
      <div class="card-valor" id="c-paises">—</div>
      <div class="card-label">Países Ativos</div>
      <div class="card-sub">Origens detectadas</div>
    </div>
  </div>
</div>

<!-- Gráficos -->
<div class="secao" style="padding-top:20px;">
  <div class="secao-titulo">Análise Visual</div>
</div>
<div class="graficos">
  <div class="grafico-box" id="g-pais"></div>
  <div class="grafico-box" id="g-tipo"></div>
  <div class="grafico-box" id="g-hora"></div>
  <div class="grafico-box" id="g-hist"></div>
</div>

<!-- Alertas -->
<div class="secao" style="padding-top:20px;">
  <div class="secao-titulo">Alertas</div>
</div>
<div class="alertas-box">
  <div class="alertas-header">
    <h2>Alertas em Aberto</h2>
    <span class="contador" id="cont-alertas">0 alertas</span>
  </div>
  <table>
    <thead>
      <tr>
        <th>Data / Hora</th>
        <th>Nível</th>
        <th>Regra</th>
        <th>Mensagem</th>
        <th>Ação</th>
      </tr>
    </thead>
    <tbody id="tb-alertas"></tbody>
  </table>
</div>

<div class="toast" id="toast">
  <div class="toast-nivel" id="toast-nivel"></div>
  <div id="toast-msg"></div>
</div>

<script>
  const BG = "#10101e", FG = "#c8c8d4", GRID = "#1a1a2e"

  const layout = (title) => ({
    title: { text: title, font: { size: 13, color: "#888" }, x: 0.02 },
    paper_bgcolor: BG, plot_bgcolor: BG,
    font: { color: FG, family: "Segoe UI, monospace" },
    margin: { l: 130, r: 20, t: 44, b: 40 },
    xaxis: { gridcolor: GRID, zerolinecolor: GRID },
    yaxis: { gridcolor: GRID, zerolinecolor: GRID }
  })

  // Relógio
  function atualizarRelogio() {
    const agora = new Date()
    document.getElementById("relogio").textContent =
      agora.toLocaleDateString("pt-BR") + "  " +
      agora.toLocaleTimeString("pt-BR")
  }
  setInterval(atualizarRelogio, 1000)
  atualizarRelogio()

  // WebSocket
  const ws = new WebSocket(`ws://${location.host}/ws`)
  ws.onopen = () => {
    document.getElementById("dot").className = "dot verde"
    document.getElementById("ws-label").textContent = "Ao Vivo"
  }
  ws.onclose = () => {
    document.getElementById("dot").className = "dot vermelho"
    document.getElementById("ws-label").textContent = "Desconectado"
  }
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data)
    if (m.tipo === "novo_alerta") {
      mostrarToast(m.dados.nivel, m.dados.mensagem)
      carregarAlertas()
      carregarStats()
    }
  }

  function mostrarToast(nivel, msg) {
    document.getElementById("toast-nivel").textContent = `[ ${nivel} ]`
    document.getElementById("toast-msg").textContent = msg
    const t = document.getElementById("toast")
    t.style.display = "block"
    setTimeout(() => t.style.display = "none", 6000)
  }

  // Stats
  async function carregarStats() {
    const d = await fetch("/api/stats").then(r => r.json())
    document.getElementById("c-ataques").textContent  = d.ataques_ultima_hora
    document.getElementById("c-criticos").textContent = d.alertas_criticos
    document.getElementById("c-abertos").textContent  = d.alertas_abertos
    document.getElementById("c-paises").textContent   = d.paises_ativos
  }

  // Gráfico: Top Países
  async function graficoPaises() {
    const d = await fetch("/api/ataques/por-pais").then(r => r.json())
    const top = d.slice(0, 10)
    Plotly.newPlot("g-pais", [{
      type: "bar", orientation: "h",
      x: top.map(i => i.total_ataques),
      y: top.map(i => i.pais_origem),
      text: top.map(i => i.total_ataques),
      textposition: "outside",
      textfont: { color: "#ff003c", size: 11 },
      marker: {
        color: top.map((_, idx) => `rgba(255,0,60,${1 - idx * 0.07})`),
        line: { color: "#ff003c44", width: 1 }
      },
      hovertemplate: "<b>%{y}</b><br>Ataques: %{x}<extra></extra>"
    }], {
      ...layout("Top 10 Países por Volume de Ataques (24h)"),
      yaxis: { ...layout().yaxis, autorange: "reversed" }
    })
  }

  // Gráfico: Por Tipo (rosca)
  async function graficoTipo() {
    const d = await fetch("/api/ataques/por-tipo").then(r => r.json())
    Plotly.newPlot("g-tipo", [{
      type: "pie", hole: 0.5,
      labels: d.map(i => i.tipo),
      values: d.map(i => i.total),
      marker: { colors: ["#ff003c", "#ff9900", "#0099ff", "#00ff88", "#cc44ff"] },
      textinfo: "label+percent",
      textfont: { color: "#ccc", size: 11 },
      hovertemplate: "<b>%{label}</b><br>%{value} ataques (%{percent})<extra></extra>"
    }], {
      title: { text: "Distribuição por Tipo de Ataque", font: { size: 13, color: "#888" }, x: 0.02 },
      paper_bgcolor: BG,
      font: { color: FG },
      margin: { t: 44, b: 20, l: 20, r: 20 },
      legend: { font: { color: "#888", size: 11 } },
      annotations: [{
        text: "Tipos", x: 0.5, y: 0.5, showarrow: false,
        font: { size: 13, color: "#555" }
      }]
    })
  }

  // Gráfico: Por Hora
  async function graficoHora() {
    const d = await fetch("/api/ataques/por-hora").then(r => r.json())
    Plotly.newPlot("g-hora", [{
      type: "bar",
      x: d.map(i => `${String(i.hora).padStart(2,"0")}h`),
      y: d.map(i => i.total),
      marker: {
        color: d.map(i =>
          i.hora >= 0 && i.hora < 6   ? "#ff003c" :
          i.hora >= 6 && i.hora < 12  ? "#ff6600" :
          i.hora >= 12 && i.hora < 18 ? "#4682b4" : "#0066aa"
        ),
        line: { color: "#0f0f1a", width: 1 }
      },
      hovertemplate: "<b>%{x}</b><br>Ataques: %{y}<extra></extra>"
    }], {
      ...layout("Volume de Ataques por Hora do Dia"),
      margin: { l: 50, r: 20, t: 44, b: 40 },
      xaxis: { ...layout().xaxis, tickfont: { size: 10 } }
    })
  }

  // Gráfico: Histórico 30 dias
  async function graficoHistorico() {
    const d = await fetch("/api/ataques/historico").then(r => r.json())
    const tipos = [...new Set(d.map(i => i.tipo))]
    const cores = ["#ff003c", "#ff9900", "#0099ff", "#00ff88", "#cc44ff"]
    const traces = tipos.map((tipo, idx) => ({
      type: "scatter", mode: "lines+markers", name: tipo,
      x: d.filter(i => i.tipo === tipo).map(i => i.dia),
      y: d.filter(i => i.tipo === tipo).map(i => i.total),
      line: { color: cores[idx % cores.length], width: 2 },
      marker: { size: 4 },
      fill: tipo === "DDoS" ? "tozeroy" : "none",
      fillcolor: "rgba(255,0,60,0.05)"
    }))
    Plotly.newPlot("g-hist", traces, {
      ...layout("Evolução Diária por Tipo — Últimos 30 Dias"),
      margin: { l: 50, r: 20, t: 44, b: 40 },
      legend: { font: { color: "#888", size: 10 }, bgcolor: BG, bordercolor: GRID }
    })
  }

  // Tabela de alertas
  async function carregarAlertas() {
    const d = await fetch("/api/alertas").then(r => r.json())
    const cont = document.getElementById("cont-alertas")
    cont.textContent = `${d.length} alerta${d.length !== 1 ? "s" : ""}`

    const tbody = document.getElementById("tb-alertas")
    if (d.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="sem-alertas">✓ Nenhum alerta em aberto</td></tr>`
      return
    }
    tbody.innerHTML = d.map(a => `
      <tr>
        <td style="color:#555;font-size:.78rem">${a.timestamp}</td>
        <td><span class="badge ${a.nivel}">${a.nivel}</span></td>
        <td class="td-regra">${a.regra}</td>
        <td class="td-mensagem">${a.mensagem}</td>
        <td><button class="btn-resolver" onclick="resolver(${a.id})">Resolver</button></td>
      </tr>`).join("")
  }

  async function resolver(id) {
    await fetch(`/api/alertas/${id}/resolver`, { method: "POST" })
    carregarAlertas()
    carregarStats()
  }

  async function init() {
    await Promise.all([
      carregarStats(),
      carregarAlertas(),
      graficoPaises(),
      graficoTipo(),
      graficoHora(),
      graficoHistorico()
    ])
  }

  init()
  setInterval(init, 30000)
</script>
</body>
</html>"""

# ── Rotas de auth ───────────────────────────────────────────
@app.get("/login", response_class=HTMLResponse)
def pagina_login():
    return LOGIN_HTML.format(erro="")

@app.post("/login")
async def fazer_login(request: Request, username: str = Form(...), password: str = Form(...)):
    senha_ok = (
        username == USERNAME and
        bcrypt.checkpw(password.encode("utf-8"), HASH)
    )
    if not senha_ok:
        return HTMLResponse(
            LOGIN_HTML.format(erro='<div class="erro">Usuário ou senha incorretos.</div>'),
            status_code=401
        )
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie("soc_token", criar_token(username),
                        httponly=True, samesite="lax", max_age=8*3600)
    return response

@app.get("/logout")
def logout():
    r = RedirectResponse(url="/login", status_code=302)
    r.delete_cookie("soc_token")
    return r

# ── Rotas do dashboard ──────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    return DASHBOARD_HTML

# ── API ─────────────────────────────────────────────────────
@app.get("/api/stats")
def api_stats(request: Request):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    with engine.connect() as c:
        return {
            "ataques_ultima_hora": c.execute(text("SELECT COUNT(*) FROM ataques WHERE data >= datetime('now','-1 hour')")).scalar(),
            "alertas_abertos":     c.execute(text("SELECT COUNT(*) FROM alertas WHERE resolvido=0")).scalar(),
            "alertas_criticos":    c.execute(text("SELECT COUNT(*) FROM alertas WHERE resolvido=0 AND nivel='CRITICO'")).scalar(),
            "paises_ativos":       c.execute(text("SELECT COUNT(DISTINCT pais_origem) FROM ataques WHERE data >= datetime('now','-1 hour')")).scalar(),
        }

@app.get("/api/ataques/por-pais")
def api_por_pais(request: Request, horas: int = 24):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    return AtaquesRepo().por_pais_periodo(horas).to_dict(orient="records")

@app.get("/api/ataques/por-tipo")
def api_por_tipo(request: Request):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    df = pd.read_sql("SELECT tipo, COUNT(*) AS total FROM ataques GROUP BY tipo ORDER BY total DESC", engine)
    return df.to_dict(orient="records")

@app.get("/api/ataques/por-hora")
def api_por_hora(request: Request):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    df = pd.read_sql(
        "SELECT CAST(strftime('%H', data) AS INTEGER) AS hora, COUNT(*) AS total "
        "FROM ataques GROUP BY hora ORDER BY hora",
        engine
    )
    return df.to_dict(orient="records")

@app.get("/api/ataques/historico")
def api_historico(request: Request, dias: int = 30):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    return AtaquesRepo().historico_diario(dias).to_dict(orient="records")

@app.get("/api/alertas")
def api_alertas(request: Request):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    df = AlertasRepo().abertos()
    df["timestamp"] = df["timestamp"].astype(str)
    return df.to_dict(orient="records")

@app.post("/api/alertas/{alerta_id}/resolver")
def api_resolver(alerta_id: int, request: Request):
    if not autenticado(request):
        return RedirectResponse(url="/login", status_code=302)
    AlertasRepo().resolver(alerta_id)
    return {"status": "ok"}

# ── WebSocket ───────────────────────────────────────────────
@app.websocket("/ws")
async def websocket(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)

# ── Background: monitoramento ───────────────────────────────
@app.on_event("startup")
async def startup():
    asyncio.create_task(loop_monitoramento())

async def loop_monitoramento():
    while True:
        novos = verificar_e_persistir()
        for a in novos:
            await manager.broadcast({"tipo": "novo_alerta", "dados": a})
            print(f"[{a['nivel']}] {a['mensagem']}")
        await asyncio.sleep(60)
