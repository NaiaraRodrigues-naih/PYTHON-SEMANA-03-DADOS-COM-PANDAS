# Semana 03 — Projeto 3: Análise Exploratória
# Estatísticas descritivas, agrupamentos, filtros e insights

import pandas as pd

print("=== ANÁLISE EXPLORATÓRIA DE DADOS ===")
print()

dados = {
    "Nome":        ["Ana", "Bruno", "Carla", "Diego", "Eva", "Felipe", "Gia", "Hugo"],
    "Departamento":["TI", "RH", "TI", "Financeiro", "RH", "TI", "Financeiro", "RH"],
    "Salario":     [7200, 4500, 8100, 6300, 4200, 9500, 7800, 3900],
    "Idade":       [28, 35, 31, 42, 26, 38, 29, 45],
    "Anos_empresa":[3, 8, 5, 12, 2, 10, 4, 15]
}

df = pd.DataFrame(dados)

print("--- Dataset ---")
print(df)

print("\n--- Estatísticas gerais ---")
print(df[["Salario", "Idade", "Anos_empresa"]].describe().round(2))

print("\n--- Média de salário por departamento ---")
print(df.groupby("Departamento")["Salario"].mean().round(2).sort_values(ascending=False))

print("\n--- Total de funcionários por departamento ---")
print(df.groupby("Departamento")["Nome"].count())

print("\n--- Maior salário de cada departamento ---")
print(df.groupby("Departamento")["Salario"].max())

print("\n--- Funcionários com salário acima da média ---")
media = df["Salario"].mean()
print(f"Média geral: R$ {media:.2f}")
acima = df[df["Salario"] > media][["Nome", "Departamento", "Salario"]]
print(acima)

print("\n--- Correlação entre anos na empresa e salário ---")
correlacao = df["Anos_empresa"].corr(df["Salario"])
print(f"Correlação: {correlacao:.2f}")
if correlacao > 0.5:
    print("Forte correlação positiva: mais tempo = maior salário")
elif correlacao > 0:
    print("Correlação positiva fraca")
else:
    print("Sem correlação clara")
