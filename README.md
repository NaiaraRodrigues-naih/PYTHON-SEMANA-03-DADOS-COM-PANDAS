# Semana 03 — Dados com Pandas

Projetos desenvolvidos durante o curso **Python do Zero com Copiloto IA** pela **KENSEI CYBERSECURITY ACADEMY**.

Dados reais, limpeza, analise e graficos — tudo via Vibe Coding com IA!

---

## Site ao Vivo

O Projeto 5 tem um **dashboard interativo publicado online:**

**https://naiararodrigues-naih.github.io/PYTHON-SEMANA-03-DADOS-COM-PANDAS/**

Graficos interativos, contador regressivo em tempo real para a proxima aproximacao de asteroide, animacoes e tabela dos 20 objetos mais proximos da Terra.

---

## Projetos

### Projeto 1 — Carregando e Explorando Dados

Primeiros passos com Pandas aplicados a um dataset real de ataques ciberneticos.

Tecnicas: `read_csv`, `head`, `shape`, `info`, `describe`, `value_counts`

Arquivos: `projeto1_exploracao.py` · `cybersecurity_attacks.csv`

---

### Projeto 2 — Limpando Dados Sujos

Como transformar dados inconsistentes em dados confiaveis: nulos, duplicatas, formatos errados e padronizacao.

Tecnicas: `fillna`, `dropna`, `drop_duplicates`, `astype`, `str.strip`

Arquivos: `limpar_dados.py` · `logs_sujos.csv` · `logs_limpos.csv`

---

### Projeto 3 — Filtrando e Agrupando

Analise de logs de segurança (SOC) com banco de dados SQLite: filtros, agrupamentos e alertas automaticos.

Tecnicas: `groupby`, `filter`, `sort_values`, `query`, SQLite com `sqlite3`

Arquivos: `main.py` · `banco.py` · `dados.py` · `alertas.py` · `soc.db`

---

### Projeto 4 — Graficos com Matplotlib

Visualizacoes de ataques ciberneticos por mes, por tipo e ranking dos maiores ataques DDoS.

Tecnicas: `bar`, `pie`, `plot`, `savefig`, `subplots`

Graficos gerados: `ataques_por_mes.png` · `tipos_ataque.png` · `top10_ddos.png`

---

### Projeto 5 — Analise Completa (Pipeline com NASA)

Pipeline completo de ciencia de dados usando dois datasets oficiais da NASA sobre asteroides Near-Earth.

**Dataset:** [NASA Near-Earth Asteroids — Kaggle](https://www.kaggle.com/datasets/darkmatternet/nasa-near-earth-asteroids-and-close-approaches)

**41.281 asteroides** e **27.430 aproximacoes** registradas/previstas entre 2015 e 2035.

#### Etapas do pipeline

```
1. Carregar     read_csv, head, shape, info, describe
2. Explorar     tipos, nulos, duplicados, range de datas
3. Limpar       fillna (mediana), to_datetime, drop_duplicates
4. Analisar     filtros, groupby, contagens, estatisticas
5. Visualizar   5 graficos salvos como PNG
```

#### Descobertas

- 6,2% dos asteroides sao classificados como PHA (Potencialmente Perigosos)
- 1.221 aproximacoes ocorreram a menos de 1 distancia lunar da Terra
- O asteroide **(2025 UC11)** chegou a apenas **6.599 km** da Terra
- Velocidade maxima registrada: **40,2 km/s** (~144.000 km/h)
- Classe Apolo domina com 23.484 objetos — todos cruzam a orbita da Terra

#### Graficos gerados

| Arquivo | Conteudo |
|---|---|
| `grafico1_aproximacoes_por_ano.png` | Aproximacoes por ano — registrado vs. previsto |
| `grafico2_distancias_e_velocidades.png` | Distribuicao de distancias + scatter velocidade |
| `grafico3_classificacao_neo.png` | Pizza PHA vs nao-PHA + categorias de tamanho |
| `grafico4_top15_mais_proximos.png` | Top 15 aproximacoes mais proximas |
| `grafico5_classe_e_magnitude.png` | Classe orbital + magnitude absoluta |

#### Dashboard online

Alem do script Python, o projeto conta com um site interativo:

- Contadores animados com os indicadores principais
- Countdown em tempo real para a proxima aproximacao
- 5 graficos interativos com Chart.js
- Tabela top 20 com barra de perigo colorida

**Acesse:** https://naiararodrigues-naih.github.io/PYTHON-SEMANA-03-DADOS-COM-PANDAS/

Arquivos: `analise_asteroides.py` · `index.html` · 5 PNGs

---

## Estrutura do Repositorio

```
PYTHON-SEMANA-03-DADOS-COM-PANDAS/
├── index.html                          # Redireciona para o dashboard
├── README.md
├── 01_introducao_pandas.py
├── 02_limpeza_dados.py
├── 03_analise_exploratoria.py
├── 04_visualizacao_graficos.py
├── 05_projeto_final.py
├── Projeto 1 Carregando e Explorando Dados/
│   ├── projeto1_exploracao.py
│   ├── cybersecurity_attacks.csv
│   └── README.md
├── Projeto 2 Limpando Dados Sujos/
│   ├── limpar_dados.py
│   ├── logs_sujos.csv
│   ├── logs_limpos.csv
│   └── README.md
├── Projeto 3 Filtrando e Agrupando/
│   ├── main.py · banco.py · dados.py · alertas.py
│   ├── soc.db
│   └── README.md
├── Projeto 4 Graficos com Matplotlib/
│   ├── graficos.py
│   ├── ataques_por_mes.png
│   ├── tipos_ataque.png
│   ├── top10_ddos.png
│   └── README.md
└── Projeto 5 Analise Completa/
    ├── analise_asteroides.py
    ├── index.html
    ├── grafico1_aproximacoes_por_ano.png
    ├── grafico2_distancias_e_velocidades.png
    ├── grafico3_classificacao_neo.png
    ├── grafico4_top15_mais_proximos.png
    ├── grafico5_classe_e_magnitude.png
    └── README.md
```

---

## Pre-requisitos

```bash
pip install pandas matplotlib seaborn
```

---

## Como executar

```bash
# Qualquer projeto individualmente
python 01_introducao_pandas.py

# Pipeline completo do Projeto 5
cd "Projeto 5 Analise Completa"
python analise_asteroides.py
```

---

Feito com dedicacao por **Naiara Rodrigues**

Estudante de Engenharia de Software — KENSEI CYBERSECURITY ACADEMY
