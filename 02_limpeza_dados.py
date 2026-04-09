# Semana 03 — Projeto 2: Limpeza de Dados
# Tratar valores nulos, duplicatas, tipos incorretos e padronização

import pandas as pd
import numpy as np

print("=== LIMPEZA DE DADOS ===")
print()

# Dataset sujo simulado
dados_sujos = {
    "Nome":    ["Ana", "Bruno", "bruno", "Carla", None, "Diego", "Ana"],
    "Idade":   [22, 35, 35, None, 19, -5, 22],
    "Email":   ["ana@email.com", "bruno@email.com", "bruno@email.com",
                "carla@email.com", "eva@email.com", "diego@email.com", "ana@email.com"],
    "Salario": ["3500", "7200", "7200", "5100", "2800", "8900", "3500"]
}

df = pd.DataFrame(dados_sujos)

print("--- Dados originais (sujos) ---")
print(df)
print(f"\nTotal de linhas: {len(df)}")

# 1. Valores nulos
print("\n--- 1. Valores nulos ---")
print(df.isnull().sum())
df["Nome"].fillna("Desconhecido", inplace=True)
df["Idade"].fillna(df["Idade"].median(), inplace=True)
print("Nulos preenchidos!")

# 2. Duplicatas
print("\n--- 2. Duplicatas ---")
print(f"Duplicatas encontradas: {df.duplicated().sum()}")
df.drop_duplicates(inplace=True)
print(f"Linhas após remover duplicatas: {len(df)}")

# 3. Tipos incorretos
print("\n--- 3. Corrigindo tipos ---")
df["Salario"] = df["Salario"].astype(float)
df["Idade"] = df["Idade"].astype(int)
print(df.dtypes)

# 4. Valores inválidos
print("\n--- 4. Valores inválidos (idade negativa) ---")
df = df[df["Idade"] > 0]
print(f"Linhas válidas: {len(df)}")

# 5. Padronização de texto
print("\n--- 5. Padronizando nomes ---")
df["Nome"] = df["Nome"].str.strip().str.title()

print("\n--- Dados limpos ---")
print(df.reset_index(drop=True))
