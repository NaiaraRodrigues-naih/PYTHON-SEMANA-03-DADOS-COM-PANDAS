# Semana 03 — Projeto 5: Projeto Final
# Análise completa: limpeza, análise exploratória e visualização

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=== PROJETO FINAL — ANÁLISE COMPLETA ===")
print()

# Dataset: notas de alunos por disciplina
dados = {
    "Aluno":      ["Ana", "Bruno", "Carla", "Diego", "Eva", "Felipe", "Gia", "Hugo", "Iris", "João"],
    "Python":     [9.5, 7.0, None, 8.5, 6.0, 10.0, 7.5, None, 8.0, 9.0],
    "Redes":      [8.0, 6.5, 9.0, 7.0, None, 8.5, 6.0, 7.5, 9.5, 7.0],
    "Seguranca":  [9.0, 8.0, 8.5, None, 7.0, 9.5, 8.0, 6.5, 10.0, 8.5],
    "Turma":      ["A", "B", "A", "B", "A", "A", "B", "B", "A", "B"]
}

df = pd.DataFrame(dados)

# --- 1. Limpeza ---
print("--- 1. Limpeza ---")
print(f"Nulos antes: {df.isnull().sum().sum()}")
for col in ["Python", "Redes", "Seguranca"]:
    df[col].fillna(df[col].mean(), inplace=True)
print(f"Nulos depois: {df.isnull().sum().sum()}")
df = df.round(1)

# --- 2. Análise ---
print("\n--- 2. Análise ---")
df["Media"] = df[["Python", "Redes", "Seguranca"]].mean(axis=1).round(1)
df["Situacao"] = df["Media"].apply(lambda m: "Aprovado" if m >= 7.0 else "Reprovado")

print(df[["Aluno", "Media", "Situacao"]])

print(f"\nAprovados: {(df['Situacao'] == 'Aprovado').sum()}")
print(f"Reprovados: {(df['Situacao'] == 'Reprovado').sum()}")

print("\n--- Média por turma ---")
print(df.groupby("Turma")["Media"].mean().round(2))

print("\n--- Melhor aluno por disciplina ---")
for col in ["Python", "Redes", "Seguranca"]:
    melhor = df.loc[df[col].idxmax(), "Aluno"]
    print(f"  {col}: {melhor} ({df[col].max()})")

# --- 3. Visualização ---
print("\n--- 3. Gerando gráficos ---")
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle("Projeto Final — Análise de Notas", fontsize=13, fontweight="bold")

# Médias por aluno
cores = ["green" if s == "Aprovado" else "red" for s in df["Situacao"]]
axes[0].barh(df["Aluno"], df["Media"], color=cores)
axes[0].axvline(7.0, color="black", linestyle="--", label="Mínimo (7.0)")
axes[0].set_title("Média por Aluno")
axes[0].legend()

# Boxplot por disciplina
df_notas = df[["Python", "Redes", "Seguranca"]]
axes[1].boxplot([df_notas[c] for c in df_notas.columns], labels=df_notas.columns)
axes[1].set_title("Distribuição de Notas")
axes[1].set_ylabel("Nota")

# Pizza situação
sit = df["Situacao"].value_counts()
axes[2].pie(sit, labels=sit.index, autopct="%1.0f%%",
            colors=["#2ecc71", "#e74c3c"], startangle=90)
axes[2].set_title("Aprovados vs Reprovados")

plt.tight_layout()
plt.savefig("projeto_final_semana03.png", dpi=150)
print("Gráfico salvo em 'projeto_final_semana03.png'!")
plt.show()
