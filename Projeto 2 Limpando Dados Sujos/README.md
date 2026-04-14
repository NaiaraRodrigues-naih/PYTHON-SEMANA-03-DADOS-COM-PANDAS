# Projeto 2 — Limpando Dados Sujos

> "Dados reais SEMPRE vem sujos. Limpar é 80% do trabalho!"

## Objetivo

Praticar limpeza de dados com **pandas** usando um dataset simulado de logs de acesso de rede com problemas propositais: duplicatas, nulos, datas inválidas, IPs e portas fora do padrão.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| `gerar_dataset_sujo.py` | Gera o arquivo `logs_sujos.csv` com erros propositais |
| `limpar_dados.py` | Script principal — executa toda a limpeza passo a passo |
| `logs_sujos.csv` | Dataset bruto com 13 linhas e vários problemas (gerado automaticamente) |
| `logs_limpos.csv` | Dataset final limpo (gerado ao rodar o script) |

---

## Como executar

```bash
python limpar_dados.py
```

O script já chama o `gerar_dataset_sujo.py` automaticamente. Basta rodar o arquivo principal.

---

## Problemas no dataset original

| Problema | Coluna | Exemplo |
|---|---|---|
| Linha duplicada | todas | id=10 aparecia 2 vezes |
| IP nulo | `ip_origem` | `None` |
| IP inválido | `ip_origem` | `999.999.999.999` |
| Tipo nulo | `tipo` | `None` |
| Data em formato variado | `data` | `16-01-2024`, `2024/01/17` |
| Data completamente inválida | `data` | `"nao_e_data"` |
| Porta negativa | `porta` | `-1` |
| Porta fora do range TCP/UDP | `porta` | `65536` |
| Tentativas nulas | `tentativas` | `None` |

---

## Passos da limpeza

### Diagnóstico
```python
print(df.isnull().sum())    # contar nulos por coluna
print(df.duplicated().sum()) # contar linhas duplicadas
```

### Passo 1 — Remover duplicados
```python
df = df.drop_duplicates()
```

### Passo 2 — Preencher nulos
```python
df["tipo"] = df["tipo"].fillna("desconhecido")      # valor fixo
df["tentativas"] = df["tentativas"].fillna(mediana)  # mediana (robusta a outliers)
```

### Passo 3 — Converter datas
```python
df["data"] = pd.to_datetime(df["data"], errors="coerce")  # inválidos viram NaT
df = df.dropna(subset=["data"])                           # remove linhas com NaT
```

### Passo 4 — Remover linhas sem dado crítico
```python
df = df.dropna(subset=["ip_origem"])
```

### Passo 5 — Remover dados inválidos de domínio
```python
df = df[(df["porta"] >= 0) & (df["porta"] <= 65535)]  # portas válidas
df = df[df["ip_origem"].apply(ip_valido)]              # IPs com octetos 0-255
```

---

## Resultado

| | Linhas | Nulos |
|---|---|---|
| Antes da limpeza | 13 | 7 |
| Depois da limpeza | 6 | 0 |

---

## Conceitos praticados

| Método | O que faz |
|---|---|
| `.isnull().sum()` | Conta valores nulos por coluna |
| `.duplicated().sum()` | Conta linhas duplicadas |
| `.drop_duplicates()` | Remove linhas duplicadas |
| `.fillna()` | Preenche valores nulos |
| `pd.to_datetime()` | Converte strings para formato de data |
| `.dropna()` | Remove linhas com nulos em colunas específicas |
| `.apply()` | Aplica uma função customizada em cada valor da coluna |
