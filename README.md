# Dados com Pandas — Semana 03
### Kensei AI Foundations 2026

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-interativo-3F4F75?style=flat&logo=plotly)
![NASA](https://img.shields.io/badge/Dados-NASA-0B3D91?style=flat)
![Status](https://img.shields.io/badge/Status-Concluido-00d4ff?style=flat)

**Dashboard ao vivo:** https://naiararodrigues-naih.github.io/PYTHON-SEMANA-03-DADOS-COM-PANDAS/

---

## Sobre

5 projetos de analise de dados com Python e Pandas, do basico ao pipeline completo com dados reais da NASA.
Tudo construido via Vibe Coding com IA — eu direciono, a IA ajuda a executar.

---

## Projetos

### Projeto 1 — Explorando Dados
Primeiros passos com Pandas em um dataset real de ataques ciberneticos.
Tecnicas: `read_csv`, `head`, `shape`, `info`, `describe`, `value_counts`

### Projeto 2 — Limpando Dados Sujos
Transformacao de dados inconsistentes em dados confiaveis.
Tecnicas: `fillna`, `dropna`, `drop_duplicates`, `astype`, `str.strip`

### Projeto 3 — Filtrando e Agrupando
Analise de logs de seguranca (SOC) com SQLite.
Tecnicas: `groupby`, `filter`, `sort_values`, `query`, banco de dados SQLite

### Projeto 4 — Graficos com Matplotlib
Visualizacoes de ataques ciberneticos por mes, tipo e ranking DDoS.
Tecnicas: `bar`, `pie`, `plot`, `savefig`, `subplots`

### Projeto 5 — Pipeline Completo com NASA
Pipeline de ponta a ponta com 41.281 asteroides e 27.430 aproximacoes (2015-2035).

```
Carregar → Explorar → Limpar → Analisar → Visualizar → Dashboard Online
```

**Destaques:**
- 6,2% dos asteroides classificados como PHA (Potencialmente Perigosos)
- 1.221 aproximacoes a menos de 1 distancia lunar da Terra
- Asteroide mais proximo: apenas 6.599 km da Terra
- Velocidade maxima: 40,2 km/s (~144.000 km/h)

---

## Estrutura

```
PYTHON-SEMANA-03-DADOS-COM-PANDAS/
├── Projeto 1 Carregando e Explorando Dados/
├── Projeto 2 Limpando Dados Sujos/
├── Projeto 3 Filtrando e Agrupando/
├── Projeto 4 Graficos com Matplotlib/
└── Projeto 5 Analise Completa/
    ├── analise_asteroides.py
    ├── index.html              # Dashboard interativo
    └── grafico1..5.png
```

---

## Como rodar

```bash
git clone https://github.com/NaiaraRodrigues-naih/PYTHON-SEMANA-03-DADOS-COM-PANDAS.git
pip install pandas matplotlib seaborn
cd "Projeto 5 Analise Completa"
python analise_asteroides.py
```

Ou acesse o dashboard online direto no link acima — sem instalacao.

---

## Tecnologias

- **Python 3** + **Pandas** — analise de dados
- **Matplotlib / Seaborn** — visualizacoes
- **SQLite** — banco de dados local
- **Chart.js** — graficos interativos no dashboard
- **GitHub Pages** — hospedagem gratuita do dashboard
- **Dados:** NASA Near-Earth Asteroids (Kaggle)

---

Feito por **Naiara Rodrigues** | Kensei AI Foundations 2026