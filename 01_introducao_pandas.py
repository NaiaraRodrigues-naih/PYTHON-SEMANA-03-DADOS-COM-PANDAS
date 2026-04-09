# Semana 03 — Projeto 1: Introdução ao Pandas
# Primeiros passos: Series, DataFrames e operações básicas

import pandas as pd

print("=== INTRODUÇÃO AO PANDAS ===")
print()

# --- Series ---
print("--- Series ---")
idades = pd.Series([22, 35, 28, 41, 19], name="Idades")
print(idades)
print(f"\nMédia de idades: {idades.mean():.1f}")
print(f"Maior idade: {idades.max()}")
print(f"Menor idade: {idades.min()}")

# --- DataFrame ---
print("\n--- DataFrame ---")
dados = {
    "Nome":       ["Ana", "Bruno", "Carla", "Diego", "Eva"],
    "Idade":      [22, 35, 28, 41, 19],
    "Cidade":     ["SP", "RJ", "MG", "BA", "RS"],
    "Salario":    [3500, 7200, 5100, 8900, 2800]
}

df = pd.DataFrame(dados)
print(df)

print("\n--- Informações do DataFrame ---")
print(f"Linhas x Colunas: {df.shape}")
print(f"\nTipos de dados:\n{df.dtypes}")

print("\n--- Estatísticas ---")
print(df.describe())

print("\n--- Filtro: salário acima de 5000 ---")
print(df[df["Salario"] > 5000])

print("\n--- Ordenado por salário ---")
print(df.sort_values("Salario", ascending=False))
