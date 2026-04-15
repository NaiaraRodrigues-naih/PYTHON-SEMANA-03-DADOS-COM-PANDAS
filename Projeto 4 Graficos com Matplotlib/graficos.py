"""
Projeto 4 — Gráficos com Matplotlib
Semana 3 | Kensei Cybersecurity

Gera 3 gráficos de ataques DDoS e salva como PNG:
  1. Barras   — Top 10 países de origem
  2. Linha    — Ataques por mês
  3. Pizza    — Distribuição por tipo de ataque
"""

import sys
import os

# Permite importar dados.py do Projeto 3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Projeto 3 Filtrando e Agrupando"))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dados import gerar_dados

# ── Dados ────────────────────────────────────────────────────
df = gerar_dados(n=1000, seed=42)

# Extrai mês/ano para o gráfico de linha
df["mes"] = df["data"].dt.to_period("M").astype(str)

PASTA = os.path.dirname(__file__)

# ── Estilo global ────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0d0d1a",
    "axes.facecolor":   "#0d0d1a",
    "axes.edgecolor":   "#2a2a4a",
    "axes.labelcolor":  "#aaaacc",
    "xtick.color":      "#888",
    "ytick.color":      "#888",
    "text.color":       "#ccccdd",
    "grid.color":       "#1e1e30",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.6,
})

# ════════════════════════════════════════════════════════════
# 1. BARRAS — Top 10 Países
# ════════════════════════════════════════════════════════════
top10 = (
    df["pais_origem"]
    .value_counts()
    .head(10)
    .sort_values()           # menor → maior (barras horizontais ficam mais legíveis)
)

fig, ax = plt.subplots(figsize=(10, 6))

cores = [
    f"rgba({int(22 + i * 20)},{int(199 - i * 14)},{int(154 - i * 12)},1)"
    for i in range(len(top10))
]
# matplotlib usa hex, não rgba string — calculamos a cor verde degradê
import matplotlib.colors as mcolors
verde_base = "#16C79A"
vermelho_base = "#ff003c"
cmap = mcolors.LinearSegmentedColormap.from_list("ddos", [verde_base, vermelho_base])
cores_mpl = [cmap(i / (len(top10) - 1)) for i in range(len(top10))]

bars = ax.barh(top10.index, top10.values, color=cores_mpl, edgecolor="#0d0d1a", height=0.7)

# Rótulos de valor ao lado das barras
for bar, val in zip(bars, top10.values):
    ax.text(val + 2, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=9, color="#ccccdd")

ax.set_title("Top 10 Países — Ataques DDoS (últimos 30 dias)",
             fontsize=13, fontweight="bold", pad=14, color="#e0e0f0")
ax.set_xlabel("Número de Ataques", fontsize=10)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.grid(axis="x")
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
caminho1 = os.path.join(PASTA, "top10_ddos.png")
plt.savefig(caminho1, dpi=150)
plt.show()
print(f"[OK] Salvo: {caminho1}")


# ════════════════════════════════════════════════════════════
# 2. LINHA — Ataques por Mês
# ════════════════════════════════════════════════════════════
por_mes = df.groupby("mes").size().reset_index(name="ataques").sort_values("mes")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(por_mes["mes"], por_mes["ataques"],
        color="#16C79A", linewidth=2.5, marker="o", markersize=7,
        markerfacecolor="#ff003c", markeredgecolor="#ff003c")

# Sombra sob a linha
ax.fill_between(por_mes["mes"], por_mes["ataques"],
                alpha=0.12, color="#16C79A")

# Rótulos nos pontos
for _, row in por_mes.iterrows():
    ax.annotate(str(int(row["ataques"])),
                xy=(row["mes"], row["ataques"]),
                xytext=(0, 10), textcoords="offset points",
                ha="center", fontsize=9, color="#aaaacc")

ax.set_title("Ataques por Mês — Série Histórica",
             fontsize=13, fontweight="bold", pad=14, color="#e0e0f0")
ax.set_xlabel("Mês", fontsize=10)
ax.set_ylabel("Número de Ataques", fontsize=10)
ax.grid(axis="y")
ax.spines[["top", "right"]].set_visible(False)
plt.xticks(rotation=30, ha="right")

plt.tight_layout()
caminho2 = os.path.join(PASTA, "ataques_por_mes.png")
plt.savefig(caminho2, dpi=150)
plt.show()
print(f"[OK] Salvo: {caminho2}")


# ════════════════════════════════════════════════════════════
# 3. PIZZA — Tipos de Ataque
# ════════════════════════════════════════════════════════════
por_tipo = df["tipo"].value_counts()

cores_pizza = ["#ff003c", "#ff9900", "#0099ff", "#00ff88", "#cc44ff"]
explode = [0.04] * len(por_tipo)   # separa levemente todas as fatias

fig, ax = plt.subplots(figsize=(8, 7))

wedges, texts, autotexts = ax.pie(
    por_tipo,
    labels=por_tipo.index,
    autopct="%1.1f%%",
    colors=cores_pizza[:len(por_tipo)],
    explode=explode,
    startangle=140,
    wedgeprops={"edgecolor": "#0d0d1a", "linewidth": 1.5},
    textprops={"color": "#ccccdd", "fontsize": 10},
)

for at in autotexts:
    at.set_fontsize(9)
    at.set_color("#ffffff")

ax.set_title("Distribuição por Tipo de Ataque",
             fontsize=13, fontweight="bold", pad=20, color="#e0e0f0")

plt.tight_layout()
caminho3 = os.path.join(PASTA, "tipos_ataque.png")
plt.savefig(caminho3, dpi=150)
plt.show()
print(f"[OK] Salvo: {caminho3}")

print("\nTodos os gráficos foram gerados com sucesso!")
