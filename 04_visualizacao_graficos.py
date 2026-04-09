# Semana 03 — Projeto 4: Visualização e Gráficos
# Gráficos com Matplotlib e Seaborn: barras, linhas, pizza e histograma

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=== VISUALIZAÇÃO E GRÁFICOS ===")

dados = {
    "Mes":        ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
    "Vendas":     [1200, 1850, 1400, 2100, 1750, 2400],
    "Despesas":   [900, 1100, 1000, 1300, 1200, 1500],
    "Categoria":  ["Eletrônicos", "Roupas", "Eletrônicos", "Alimentos", "Roupas", "Alimentos"]
}

df = pd.DataFrame(dados)
df["Lucro"] = df["Vendas"] - df["Despesas"]

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Semana 03 — Análise de Vendas", fontsize=14, fontweight="bold")

# 1. Gráfico de barras — vendas por mês
axes[0, 0].bar(df["Mes"], df["Vendas"], color="steelblue")
axes[0, 0].set_title("Vendas por Mês")
axes[0, 0].set_ylabel("R$")

# 2. Gráfico de linhas — vendas vs despesas
axes[0, 1].plot(df["Mes"], df["Vendas"], marker="o", label="Vendas", color="green")
axes[0, 1].plot(df["Mes"], df["Despesas"], marker="o", label="Despesas", color="red")
axes[0, 1].set_title("Vendas vs Despesas")
axes[0, 1].legend()

# 3. Gráfico de pizza — distribuição por categoria
cat_count = df["Categoria"].value_counts()
axes[1, 0].pie(cat_count, labels=cat_count.index, autopct="%1.1f%%", startangle=90)
axes[1, 0].set_title("Distribuição por Categoria")

# 4. Histograma — distribuição do lucro
axes[1, 1].hist(df["Lucro"], bins=5, color="purple", edgecolor="white")
axes[1, 1].set_title("Distribuição do Lucro")
axes[1, 1].set_xlabel("R$")

plt.tight_layout()
plt.savefig("graficos_semana03.png", dpi=150)
print("Gráficos salvos em 'graficos_semana03.png'!")
plt.show()
