# =============================================================================
# PIPELINE COMPLETO — NASA Near-Earth Asteroids & Close Approaches
# Dataset: https://www.kaggle.com/datasets/darkmatternet/nasa-near-earth-asteroids-and-close-approaches
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

BASE = "./"   # pasta onde estão os CSVs

# Paleta consistente
CORES = {
    "azul":     "#1f77b4",
    "laranja":  "#ff7f0e",
    "verde":    "#2ca02c",
    "vermelho": "#d62728",
    "roxo":     "#9467bd",
    "cinza":    "#7f7f7f",
}

# =============================================================================
# ETAPA 1 — CARREGAR E EXPLORAR
# =============================================================================
print("=" * 60)
print("ETAPA 1 — CARREGANDO OS DADOS")
print("=" * 60)

df_neo = pd.read_csv(BASE + "near_earth_asteroids_2025 (1).csv",
                     encoding="utf-8", low_memory=False)
df_ca  = pd.read_csv(BASE + "asteroid_close_approaches_2015_2035 (1).csv",
                     encoding="utf-8")

print(f"\n[NEO]  {df_neo.shape[0]:,} asteroides  |  {df_neo.shape[1]} colunas")
print(f"[CA]   {df_ca.shape[0]:,} aproximações  |  {df_ca.shape[1]} colunas")

print("\n--- Primeiras linhas (NEO) ---")
print(df_neo[["full_name", "pha", "H", "diameter_km", "size_category", "class"]].head(5).to_string(index=False))

print("\n--- Primeiras linhas (Close Approaches) ---")
print(df_ca[["full_name", "close_approach_date", "dist_km", "velocity_km_s", "is_future"]].head(5).to_string(index=False))

print("\n--- Info geral (NEO) ---")
df_neo.info(verbose=False)

print("\n--- Estatísticas (Close Approaches) ---")
print(df_ca[["dist_km", "dist_lunar", "velocity_km_s"]].describe().round(2))

# =============================================================================
# ETAPA 2 — LIMPEZA DE DADOS
# =============================================================================
print("\n" + "=" * 60)
print("ETAPA 2 — LIMPEZA DOS DADOS")
print("=" * 60)

# --- NEO ---
nulos_antes_neo = df_neo.isnull().sum().sum()
dup_antes_neo   = df_neo.duplicated().sum()

# Converter datas
df_neo["first_obs"] = pd.to_datetime(df_neo["first_obs"], errors="coerce")
df_neo["last_obs"]  = pd.to_datetime(df_neo["last_obs"],  errors="coerce")

# Preencher colunas com poucos nulos por mediana
for col in ["H", "moid_au", "moid_km", "moid_lunar_distances"]:
    df_neo[col].fillna(df_neo[col].median(), inplace=True)

# 'name' quase todo nulo — substituir por pdes (designação)
df_neo["name"] = df_neo["name"].fillna(df_neo["pdes"])

# Remover duplicados
df_neo.drop_duplicates(inplace=True)

nulos_depois_neo = df_neo.isnull().sum().sum()
print(f"[NEO]  Nulos antes: {nulos_antes_neo:,}  →  depois: {nulos_depois_neo:,}")
print(f"[NEO]  Duplicados removidos: {dup_antes_neo}")

# --- Close Approaches ---
nulos_antes_ca = df_ca.isnull().sum().sum()
dup_antes_ca   = df_ca.duplicated().sum()

# Converter data
df_ca["close_approach_date"] = pd.to_datetime(df_ca["close_approach_date"], errors="coerce")
df_ca["year"]  = df_ca["close_approach_date"].dt.year
df_ca["month"] = df_ca["close_approach_date"].dt.month

# Preencher nulos com mediana
for col in ["velocity_infinity_km_s", "absolute_magnitude"]:
    df_ca[col].fillna(df_ca[col].median(), inplace=True)

df_ca.drop_duplicates(inplace=True)

nulos_depois_ca = df_ca.isnull().sum().sum()
print(f"[CA]   Nulos antes: {nulos_antes_ca:,}  →  depois: {nulos_depois_ca:,}")
print(f"[CA]   Duplicados removidos: {dup_antes_ca}")
print("\nDados limpos! ✔")

# =============================================================================
# ETAPA 3 — ANÁLISE
# =============================================================================
print("\n" + "=" * 60)
print("ETAPA 3 — ANÁLISE")
print("=" * 60)

# Q1: Quantos asteroides são Potencialmente Perigosos (PHA)?
pha_count = df_neo["pha"].value_counts()
print(f"\n[Q1] Asteroides PHA (Potencialmente Perigosos):")
print(f"     Sim: {pha_count[True]:,}  ({pha_count[True]/len(df_neo)*100:.1f}%)")
print(f"     Não: {pha_count[False]:,}  ({pha_count[False]/len(df_neo)*100:.1f}%)")

# Q2: Distribuição por classe orbital
print(f"\n[Q2] Distribuição por classe orbital:")
classes = df_neo["class"].value_counts()
for cls, n in classes.items():
    desc = {"APO": "Apolo (cruzam a Terra)", "AMO": "Amor (próximos à Terra)",
            "ATE": "Aten (dentro da órbita)", "IEO": "Atira (interior à Terra)"}.get(cls, cls)
    print(f"     {cls} — {desc}: {n:,}")

# Q3: Tamanho — categorias
print(f"\n[Q3] Categorias de tamanho:")
for cat, n in df_neo["size_category"].value_counts().items():
    print(f"     {cat}: {n:,}")

# Q4: Aproximações por ano
print(f"\n[Q4] Aproximações registradas/previstas por ano (top 5):")
por_ano = df_ca.groupby("year").size().sort_values(ascending=False).head(5)
for ano, n in por_ano.items():
    print(f"     {int(ano)}: {n:,} aproximações")

# Q5: Aproximações perigosas (< 1 distância lunar ≈ 384.400 km)
perigo = df_ca[df_ca["dist_lunar"] < 1]
print(f"\n[Q5] Aproximações a menos de 1 distância lunar: {len(perigo)}")
print(f"     Mais próxima: {perigo['dist_km'].min():,.0f} km")
print(f"     Objeto mais próximo: {perigo.loc[perigo['dist_km'].idxmin(), 'full_name']}")

# Q6: Velocidades
print(f"\n[Q6] Velocidade das aproximações:")
print(f"     Média:  {df_ca['velocity_km_s'].mean():.1f} km/s")
print(f"     Máxima: {df_ca['velocity_km_s'].max():.1f} km/s")
print(f"     Mínima: {df_ca['velocity_km_s'].min():.2f} km/s")

# =============================================================================
# ETAPA 4 — VISUALIZAÇÕES
# =============================================================================
print("\n" + "=" * 60)
print("ETAPA 4 — GERANDO GRÁFICOS")
print("=" * 60)

plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor":   "#161b22",
    "axes.edgecolor":   "#30363d",
    "axes.labelcolor":  "#e6edf3",
    "xtick.color":      "#8b949e",
    "ytick.color":      "#8b949e",
    "text.color":       "#e6edf3",
    "grid.color":       "#21262d",
    "grid.linestyle":   "--",
    "grid.alpha":       0.5,
    "font.family":      "monospace",
})

# ------------------------------------------------------------------
# GRÁFICO 1 — Aproximações por ano + projeção futura
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 6))

por_ano_all = df_ca.groupby("year").size().reset_index(name="n")
passado = por_ano_all[por_ano_all["year"] <= 2025]
futuro  = por_ano_all[por_ano_all["year"] > 2025]

ax.bar(passado["year"], passado["n"], color=CORES["azul"],   label="Registrado (2015–2025)", zorder=3)
ax.bar(futuro["year"],  futuro["n"],  color=CORES["laranja"], label="Previsto (2026–2035)",   zorder=3)

ax.axvline(2025.5, color=CORES["vermelho"], linestyle="--", linewidth=1.5, label="Hoje (2025)")
ax.set_title("Aproximações de Asteroides à Terra por Ano", fontsize=15, pad=12)
ax.set_xlabel("Ano")
ax.set_ylabel("Número de Aproximações")
ax.legend(framealpha=0.2)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.grid(axis="y", zorder=0)

for bar in ax.patches:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2, h + 20, f"{int(h):,}",
                ha="center", va="bottom", fontsize=7, color="#8b949e")

fig.tight_layout()
fig.savefig(BASE + "grafico1_aproximacoes_por_ano.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✔ grafico1_aproximacoes_por_ano.png")

# ------------------------------------------------------------------
# GRÁFICO 2 — Distribuição de distâncias (em distâncias lunares)
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Histograma de distâncias
ax = axes[0]
ax.hist(df_ca["dist_lunar"], bins=60, color=CORES["azul"], edgecolor="#0d1117", linewidth=0.3, zorder=3)
ax.axvline(1, color=CORES["vermelho"], linestyle="--", linewidth=1.5, label="1 distância lunar (perigoso)")
ax.set_title("Distribuição de Distâncias (Distâncias Lunares)")
ax.set_xlabel("Distâncias Lunares (1 LD = 384.400 km)")
ax.set_ylabel("Nº de Aproximações")
ax.legend(framealpha=0.2, fontsize=9)
ax.grid(axis="y", zorder=0)

# Scatter distância × velocidade
ax = axes[1]
scatter_data = df_ca[df_ca["dist_lunar"] <= 40].copy()
sc = ax.scatter(
    scatter_data["dist_lunar"],
    scatter_data["velocity_km_s"],
    c=scatter_data["dist_lunar"],
    cmap="plasma",
    alpha=0.4, s=8, zorder=3
)
ax.axvline(1, color=CORES["vermelho"], linestyle="--", linewidth=1.2, label="1 LD")
plt.colorbar(sc, ax=ax, label="Distância (LD)")
ax.set_title("Distância vs Velocidade das Aproximações")
ax.set_xlabel("Distância (Distâncias Lunares)")
ax.set_ylabel("Velocidade (km/s)")
ax.legend(framealpha=0.2, fontsize=9)

fig.suptitle("Perfil de Risco das Aproximações", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(BASE + "grafico2_distancias_e_velocidades.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✔ grafico2_distancias_e_velocidades.png")

# ------------------------------------------------------------------
# GRÁFICO 3 — Classificação dos Asteroides NEO
# ------------------------------------------------------------------
fig = plt.figure(figsize=(14, 7))
gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

# Pizza — PHA vs não-PHA
ax1 = fig.add_subplot(gs[0])
labels_pha  = ["Não Perigoso\n(não-PHA)", "Potencialmente\nPerigoso (PHA)"]
valores_pha = [pha_count[False], pha_count[True]]
cores_pha   = [CORES["azul"], CORES["vermelho"]]
wedges, texts, autotexts = ax1.pie(
    valores_pha, labels=labels_pha, colors=cores_pha,
    autopct="%1.1f%%", startangle=90,
    wedgeprops=dict(edgecolor="#0d1117", linewidth=1.5),
    textprops=dict(color="#e6edf3")
)
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight("bold")
ax1.set_title("Asteroides PHA vs Não-PHA\n(41.281 objetos)", fontsize=12, pad=10)

# Barras horizontais — categorias de tamanho
ax2 = fig.add_subplot(gs[1])
size_data = df_neo["size_category"].value_counts().sort_values()
# Rótulos curtos
short_labels = [s.split(" — ")[0] for s in size_data.index]
cores_size = [CORES["verde"], CORES["azul"], CORES["laranja"], CORES["vermelho"]]
bars = ax2.barh(short_labels, size_data.values, color=cores_size[::-1], edgecolor="#0d1117", zorder=3)

for bar, val in zip(bars, size_data.values):
    ax2.text(val + 150, bar.get_y() + bar.get_height()/2,
             f"{val:,}", va="center", fontsize=10)

ax2.set_title("Distribuição por Tamanho", fontsize=12, pad=10)
ax2.set_xlabel("Número de Asteroides")
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax2.grid(axis="x", zorder=0)
ax2.set_xlim(0, size_data.max() * 1.18)

fig.suptitle("Perfil dos Asteroides Near-Earth (NASA — 2025)", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(BASE + "grafico3_classificacao_neo.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✔ grafico3_classificacao_neo.png")

# ------------------------------------------------------------------
# GRÁFICO 4 — Top 15 Aproximações Mais Perigosas (passado + futuro)
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))

top15 = (df_ca.sort_values("dist_lunar").head(15)
              .sort_values("dist_lunar", ascending=False))

cores_bars = [CORES["laranja"] if f else CORES["azul"] for f in top15["is_future"]]
bars = ax.barh(
    top15["full_name"].str.strip("()"),
    top15["dist_lunar"],
    color=cores_bars, edgecolor="#0d1117", zorder=3
)

for bar, (_, row) in zip(bars, top15.iterrows()):
    ax.text(bar.get_width() + 0.005,
            bar.get_y() + bar.get_height()/2,
            f"{row['dist_km']:,.0f} km  |  {row['velocity_km_s']:.1f} km/s",
            va="center", fontsize=8, color="#8b949e")

ax.axvline(1, color=CORES["vermelho"], linestyle="--", linewidth=1.5,
           label="Limite PHA (1 LD)")
ax.set_title("Top 15 Aproximações Mais Próximas à Terra (2015–2035)", fontsize=13, pad=12)
ax.set_xlabel("Distância em Distâncias Lunares (1 LD = 384.400 km)")
ax.set_xlim(0, top15["dist_lunar"].max() * 1.35)
ax.grid(axis="x", zorder=0)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=CORES["azul"],   label="Evento passado"),
    Patch(facecolor=CORES["laranja"], label="Evento futuro"),
    Patch(facecolor=CORES["vermelho"], linestyle="--", label="Limite PHA (1 LD)"),
]
ax.legend(handles=legend_elements, framealpha=0.2)

fig.tight_layout()
fig.savefig(BASE + "grafico4_top15_mais_proximos.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✔ grafico4_top15_mais_proximos.png")

# ------------------------------------------------------------------
# GRÁFICO 5 — Classe orbital × PHA (heatmap de contagem)
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Barras empilhadas por classe orbital
ax = axes[0]
pivot = df_neo.groupby(["class", "pha"]).size().unstack(fill_value=0)
pivot.columns = ["Não-PHA", "PHA"]
pivot = pivot.sort_values("PHA", ascending=False)
x = range(len(pivot))
ax.bar(x, pivot["Não-PHA"], color=CORES["azul"],    label="Não-PHA", zorder=3)
ax.bar(x, pivot["PHA"],     color=CORES["vermelho"], label="PHA",
       bottom=pivot["Não-PHA"], zorder=3)
ax.set_xticks(list(x))
ax.set_xticklabels(
    ["Apolo (APO)", "Amor (AMO)", "Aten (ATE)", "Atira (IEO)"],
    fontsize=10
)
ax.set_title("Asteroides por Classe Orbital e Periculosidade")
ax.set_ylabel("Quantidade")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
ax.legend(framealpha=0.2)
ax.grid(axis="y", zorder=0)

for i, (_, row) in enumerate(pivot.iterrows()):
    total = row["Não-PHA"] + row["PHA"]
    ax.text(i, total + 100, f"{total:,}", ha="center", fontsize=9, color="#8b949e")

# Histograma de magnitude absoluta (H) — brilho/tamanho proxy
ax = axes[1]
ax.hist(df_neo["H"].dropna(), bins=50, color=CORES["roxo"],
        edgecolor="#0d1117", linewidth=0.3, zorder=3)
ax.set_title("Distribuição de Magnitude Absoluta (H)")
ax.set_xlabel("Magnitude Absoluta H  (menor H = maior/mais brilhante)")
ax.set_ylabel("Número de Asteroides")
ax.axvline(df_neo["H"].median(), color=CORES["laranja"], linestyle="--",
           linewidth=1.5, label=f"Mediana: {df_neo['H'].median():.1f}")
ax.legend(framealpha=0.2)
ax.grid(axis="y", zorder=0)

fig.suptitle("Análise Orbital e Física dos NEOs", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(BASE + "grafico5_classe_e_magnitude.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✔ grafico5_classe_e_magnitude.png")

# =============================================================================
# RESUMO FINAL
# =============================================================================
print("\n" + "=" * 60)
print("RESUMO DO PIPELINE")
print("=" * 60)
print(f"  Dataset 1 (NEO):             {len(df_neo):,} asteroides")
print(f"  Dataset 2 (Close Approaches):{len(df_ca):,} aproximações")
print(f"  Perigosos (PHA):             {pha_count[True]:,} ({pha_count[True]/len(df_neo)*100:.1f}%)")
print(f"  Aprox. < 1 LD:               {len(perigo)}")
print(f"  Objeto mais próximo já:      {perigo.loc[perigo['dist_km'].idxmin(), 'full_name'].strip()}")
print(f"  Distância mínima:            {perigo['dist_km'].min():,.0f} km")
print(f"  Gráficos salvos:             5 PNGs")
print("=" * 60)
print("Pipeline concluído com sucesso!")
