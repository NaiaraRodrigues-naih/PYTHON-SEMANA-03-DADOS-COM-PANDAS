# Projeto 1 — Carregando e Explorando Dados de Ataques Cibernéticos

## Descrição

Projeto introdutório de análise de dados com foco em segurança cibernética.
Utiliza **Pandas** para carregar e explorar um dataset de ataques e **Matplotlib** para gerar gráficos.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| `projeto1_exploracao.py` | Script principal de análise e visualização |
| `cybersecurity_attacks.csv` | Dataset com 30 registros de ataques simulados |
| `grafico_ataques.png` | Gráfico gerado automaticamente ao rodar o script |

---

## Dataset — cybersecurity_attacks.csv

O arquivo contém registros de ataques com as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `timestamp` | Data e hora do ataque |
| `src_ip` | IP de origem do ataque |
| `dst_ip` | IP de destino |
| `attack_type` | Tipo de ataque (DDoS, Ransomware, Phishing, etc.) |
| `severity` | Severidade (Low, Medium, High, Critical) |
| `country` | País de origem |
| `protocol` | Protocolo utilizado (TCP, UDP, HTTP, SSH) |
| `bytes_sent` | Bytes enviados |
| `bytes_received` | Bytes recebidos |
| `duration_sec` | Duração do ataque em segundos |
| `status` | Resultado (Blocked / Detected) |

---

## O que o script faz

### Exploração inicial
- `df.head()` — exibe as 5 primeiras linhas
- `df.shape` — mostra o total de linhas e colunas
- `df.info()` — lista os tipos de dados de cada coluna
- `df.describe()` — calcula estatísticas (média, mínimo, máximo, desvio padrão)
- `df.columns` — lista os nomes das colunas
- `df.isnull().sum()` — conta valores vazios por coluna

### Análises de segurança
- Contagem de ataques por **tipo**
- Contagem de ataques por **severidade**
- **Top 5 países** de origem dos ataques

### Visualização
- Gráfico de barras com a quantidade de ataques por tipo (em português)
- Gráfico salvo automaticamente como `grafico_ataques.png`

---

## Como executar

```bash
& "C:\Users\User\AppData\Local\Python\bin\python.exe" projeto1_exploracao.py
```

> O script detecta automaticamente o diretório onde está salvo,
> então pode ser executado de qualquer pasta.

---

## Bibliotecas utilizadas

```bash
pip install pandas matplotlib
```

| Biblioteca | Versão utilizada | Finalidade |
|---|---|---|
| pandas | 3.0+ | Carregar e analisar o CSV |
| matplotlib | 3.10+ | Gerar o gráfico de barras |

---

## Conceitos aprendidos

| Comando | O que faz |
|---|---|
| `import pandas as pd` | Importar Pandas |
| `import matplotlib.pyplot as plt` | Importar Matplotlib |
| `pd.read_csv()` | Carregar arquivo CSV |
| `df.head()` | Ver primeiras linhas |
| `df.shape` | Ver dimensões da tabela |
| `df.info()` | Ver tipos de dados |
| `df.describe()` | Ver estatísticas gerais |
| `df.isnull().sum()` | Contar valores nulos |
| `df["coluna"].value_counts()` | Contar ocorrências por valor |
| `.plot(kind="bar")` | Gerar gráfico de barras |

---

*Semana 3 — Python com Dados e Pandas | Kensei Cybersecurity*
