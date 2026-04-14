import pandas as pd
import matplotlib.pyplot as plt
import os

# ─── Carregar o CSV ───────────────────────────────────────────────────────────
base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, "cybersecurity_attacks.csv"))

# ─── Exploração inicial ───────────────────────────────────────────────────────
print("=" * 50)
print("5 PRIMEIRAS LINHAS")
print("=" * 50)
print(df.head())

print("\n" + "=" * 50)
print("DIMENSOES (linhas, colunas)")
print("=" * 50)
print(df.shape)

print("\n" + "=" * 50)
print("TIPOS DE DADOS")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("ESTATISTICAS GERAIS")
print("=" * 50)
print(df.describe())

print("\n" + "=" * 50)
print("NOMES DAS COLUNAS")
print("=" * 50)
print(df.columns.tolist())

print("\n" + "=" * 50)
print("VALORES NULOS POR COLUNA")
print("=" * 50)
print(df.isnull().sum())

# ─── Análises de segurança ────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("ATAQUES POR TIPO")
print("=" * 50)
print(df["attack_type"].value_counts())

print("\n" + "=" * 50)
print("ATAQUES POR SEVERIDADE")
print("=" * 50)
print(df["severity"].value_counts())

print("\n" + "=" * 50)
print("TOP 5 PAISES DE ORIGEM")
print("=" * 50)
print(df["country"].value_counts().head(5))

# ─── Gráfico: Tipos de ataque ─────────────────────────────────────────────────
traducoes = {
    "DDoS": "DDoS",
    "SQL Injection": "Injeção SQL",
    "Phishing": "Phishing",
    "Port Scan": "Varredura de Porta",
    "Brute Force": "Força Bruta",
    "XSS": "XSS",
    "Ransomware": "Ransomware",
}

contagem = df["attack_type"].value_counts()
contagem.index = [traducoes.get(i, i) for i in contagem.index]

contagem.plot(kind="bar", color="crimson", edgecolor="black")
plt.title("Quantidade de Ataques por Tipo", fontsize=14, fontweight="bold")
plt.xlabel("Tipo de Ataque", fontsize=12)
plt.ylabel("Quantidade", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "grafico_ataques.png"))
plt.show()
print("\nGrafico salvo como 'grafico_ataques.png'")
