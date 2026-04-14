import pandas as pd
import numpy as np
import subprocess, sys
from pathlib import Path

# ============================================================
# PROJETO 2 - Limpando Dados Sujos
# Dados reais SEMPRE vem sujos. Limpar é 80% do trabalho!
# ============================================================

# Pasta onde este script está salvo
PASTA = Path(__file__).parent

# --- 1. CARREGAR O DATASET ---
# Gera o CSV sujo na hora (sem precisar rodar outro script)
subprocess.run([sys.executable, PASTA / "gerar_dataset_sujo.py"], check=True, cwd=PASTA)

df = pd.read_csv(PASTA / "logs_sujos.csv")

print("=" * 50)
print("DATASET ORIGINAL (SUJO)")
print("=" * 50)
print(df.to_string())

# --- 2. DIAGNÓSTICO: entender a sujeira ---
print("\n" + "=" * 50)
print("DIAGNÓSTICO")
print("=" * 50)

print("\n[+] Valores nulos por coluna:")
print(df.isnull().sum())

print(f"\n[+] Linhas duplicadas: {df.duplicated().sum()}")

print(f"\n[+] Shape original: {df.shape}")

# --- 3. REMOVER DUPLICADOS ---
print("\n" + "=" * 50)
print("PASSO 1: Remover duplicados")
print("=" * 50)

antes = len(df)
df = df.drop_duplicates()
depois = len(df)
print(f"Removidas {antes - depois} linha(s) duplicada(s).")

# --- 4. PREENCHER NULOS ---
print("\n" + "=" * 50)
print("PASSO 2: Preencher valores nulos")
print("=" * 50)

# Coluna 'tipo': preenche com 'desconhecido'
df["tipo"] = df["tipo"].fillna("desconhecido")
print("[+] 'tipo' nulo preenchido com 'desconhecido'")

# Coluna 'tentativas': preenche com a mediana (mais robusta que média para outliers)
mediana = df["tentativas"].median()
df["tentativas"] = df["tentativas"].fillna(mediana)
print(f"[+] 'tentativas' nula preenchida com mediana ({mediana})")

# --- 5. CONVERTER DATAS ---
print("\n" + "=" * 50)
print("PASSO 3: Converter coluna de datas")
print("=" * 50)

df["data"] = pd.to_datetime(df["data"], errors="coerce")  # invalidos viram NaT
nulos_data = df["data"].isnull().sum()
print(f"[+] Datas inválidas convertidas para NaT: {nulos_data}")
df = df.dropna(subset=["data"])
print(f"[+] Linhas com data inválida removidas. Restam: {len(df)}")

# --- 6. REMOVER LINHAS COM DADOS CRÍTICOS AUSENTES ---
print("\n" + "=" * 50)
print("PASSO 4: Remover linhas sem ip_origem")
print("=" * 50)

antes = len(df)
df = df.dropna(subset=["ip_origem"])
print(f"Removidas {antes - len(df)} linha(s) sem ip_origem.")

# --- 7. REMOVER DADOS INVÁLIDOS DE DOMÍNIO ---
print("\n" + "=" * 50)
print("PASSO 5: Remover dados inválidos de domínio")
print("=" * 50)

# Portas válidas: 0 a 65535
antes = len(df)
df = df[(df["porta"] >= 0) & (df["porta"] <= 65535)]
print(f"Removidas {antes - len(df)} linha(s) com porta fora do range válido (0-65535).")

# IPs obviamente inválidos (octetos > 255) — validação simples
def ip_valido(ip):
    partes = str(ip).split(".")
    if len(partes) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in partes)
    except ValueError:
        return False

antes = len(df)
df = df[df["ip_origem"].apply(ip_valido)]
print(f"Removidas {antes - len(df)} linha(s) com IP inválido.")

# --- 8. RESULTADO FINAL ---
print("\n" + "=" * 50)
print("DATASET LIMPO - RESULTADO FINAL")
print("=" * 50)
print(df.to_string())

print("\n" + "=" * 50)
print("RESUMO DA LIMPEZA")
print("=" * 50)
print(f"Shape original : (13, 6)")
print(f"Shape final    : {df.shape}")
print(f"\nValores nulos restantes:")
print(df.isnull().sum())

# Salvar dataset limpo
df.to_csv(PASTA / "logs_limpos.csv", index=False)
print("\n[+] Dataset limpo salvo em: logs_limpos.csv")
