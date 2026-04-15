# Projeto 3 — Filtrando e Agrupando

> **Semana 3 — Python com Dados usando Pandas**  
> Curso: kensei Cybersecurity  
> Tema: Análise de ataques cibernéticos com filtragem, agrupamento e visualização em tempo real

---

## Sobre o Projeto

Este projeto aplica os conceitos de **filtragem e agrupamento de dados com Pandas** em um cenário real de segurança cibernética: um **SOC Dashboard** (Security Operations Center) para monitoramento de ataques DDoS.

A partir de um conjunto de dados de ataques simulados, o sistema filtra, agrupa, analisa e exibe os resultados em um dashboard web interativo com alertas em tempo real.

---

## O que foi construído

### Etapa 1 — Filtragem e Agrupamento com Pandas

Aplicação direta dos conceitos da semana:

```python
# Filtrar ataques DDoS do último mês
ddos = df[df["tipo"] == "DDoS"]
recentes = ddos[ddos["data"] > um_mes_atras]

# Agrupar por país e contar — Top 10
top10 = (
    recentes
    .groupby("pais_origem")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

# Média de duração por país
media_duracao = (
    recentes
    .groupby("pais_origem")["duracao_segundos"]
    .mean()
    .sort_values(ascending=False)
)

# Múltiplas métricas com .agg()
resumo = (
    recentes
    .groupby("pais_origem")["duracao_segundos"]
    .agg(
        total_ataques="count",
        media_duracao="mean",
        maior_ataque="max"
    )
    .round(2)
    .sort_values("total_ataques", ascending=False)
    .head(10)
)
```

**Conceitos aplicados:**

| Operação | Método |
|---|---|
| Filtrar linhas por condição | `df[condição]` |
| Filtrar por data relativa | `pd.Timestamp.now() - pd.DateOffset()` |
| Agrupar por coluna | `.groupby()` |
| Contar por grupo | `.size()` / `.count()` |
| Média por grupo | `.mean()` |
| Múltiplas métricas | `.agg()` |
| Ordenar | `.sort_values()` |
| Top N | `.head(N)` |
| Resetar índice | `.reset_index()` |

---

### Etapa 2 — Visualização com Plotly

Dashboard com 4 gráficos interativos gerados a partir dos dados agrupados:

- **Top 10 Países por Volume de Ataques** — gráfico de barras horizontal
- **Distribuição por Tipo de Ataque** — gráfico de rosca (pie com hole)
- **Volume de Ataques por Hora do Dia** — barras coloridas por período
- **Evolução Diária por Tipo — 30 dias** — linhas com área

---

### Etapa 3 — Banco de Dados (SQLite)

Persistência dos dados com **SQLAlchemy** usando o padrão Repository:

```
soc.db
 ├── ataques              — eventos brutos de ataques
 ├── alertas              — alertas gerados com status (aberto/resolvido)
 └── paises_conhecidos    — histórico de países detectados
```

Classes implementadas:
- `AtaquesRepo` — inserir, consultar por período, histórico diário
- `AlertasRepo` — inserir, listar abertos, resolver, histórico
- `PaisesRepo` — detectar países novos

---

### Etapa 4 — Sistema de Alertas Automáticos

Motor de detecção com 4 regras aplicadas sobre os dados agrupados:

| Regra | Limiar | Nível |
|---|---|---|
| Ataques por país na última hora | ≥ 50 | CRÍTICO |
| Duração média de ataque | ≥ 300s | AVISO |
| País nunca visto antes | — | INFO |
| Volume total na última hora | ≥ 500 | CRÍTICO |

---

### Etapa 5 — Dashboard Web com FastAPI

Interface web completa com autenticação e dados em tempo real:

**Tecnologias:**
- `FastAPI` — servidor web e API REST
- `WebSocket` — push de alertas em tempo real (sem refresh)
- `Plotly.js` — gráficos interativos no navegador
- `SQLite + SQLAlchemy` — banco de dados local
- `JWT + bcrypt` — autenticação segura

**Rotas da API:**

| Rota | Descrição |
|---|---|
| `GET /` | Dashboard principal |
| `GET /login` | Página de login |
| `POST /login` | Autenticar usuário |
| `GET /logout` | Encerrar sessão |
| `GET /api/stats` | KPIs em tempo real |
| `GET /api/ataques/por-pais` | Top países agrupados |
| `GET /api/ataques/por-tipo` | Contagem por tipo |
| `GET /api/ataques/por-hora` | Volume por hora |
| `GET /api/ataques/historico` | Evolução 30 dias |
| `GET /api/alertas` | Alertas em aberto |
| `POST /api/alertas/{id}/resolver` | Resolver alerta |
| `WS /ws` | Stream de alertas ao vivo |

---

### Etapa 6 — Autenticação Segura

| Proteção | Implementação |
|---|---|
| Senha hasheada | `bcrypt` com salt automático |
| Token de sessão | `JWT` assinado com chave secreta |
| Cookie seguro | `httponly=True` — JS não acessa |
| Credenciais | Variáveis de ambiente (`.env`) |
| Expiração | Token válido por 8 horas |

---

## Estrutura de Arquivos

```
Projeto 3 Filtrando e Agrupando/
 ├── main.py        — servidor FastAPI, dashboard HTML, rotas da API
 ├── banco.py       — SQLite, criação de tabelas, repositórios
 ├── alertas.py     — motor de detecção de alertas
 ├── dados.py       — gerador de dados simulados de ataques
 ├── .env           — credenciais (não versionado)
 ├── .gitignore     — arquivos ignorados pelo git
 └── README.md      — este arquivo
```

---

## Como Executar

### 1. Instalar dependências

```bash
pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography] python-multipart python-dotenv pandas sqlalchemy bcrypt
```

### 2. Configurar credenciais

Crie o arquivo `.env` na pasta do projeto:

```bash
# Gerar hash da senha
python -c "import bcrypt; print(bcrypt.hashpw(b'SuaSenha', bcrypt.gensalt()).decode())"

# Gerar chave secreta
python -c "import secrets; print(secrets.token_hex(32))"
```

```env
SOC_USERNAME=seu_usuario
SOC_SENHA_HASH=$2b$12$hash_gerado_aqui
SOC_SECRET_KEY=chave_gerada_aqui
```

### 3. Iniciar o servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Acessar no navegador

```
http://localhost:8000
```

---

## Dados Simulados

O arquivo `dados.py` gera 1000 eventos aleatórios com países reais:

**Países incluídos:** China, Rússia, Estados Unidos, Brasil, Irã, Coreia do Norte, Índia, Alemanha, Ucrânia, Nigéria, Romênia, Vietnã, Paquistão, Turquia, Indonésia

**Tipos de ataque:** DDoS (50%), Phishing (20%), Ransomware (10%), BruteForce (10%), SQLInjection (10%)

---

## Conceitos da Semana Aplicados

```python
df[condicao]              # Filtrar linhas
.groupby("coluna")        # Agrupar por coluna
.size()                   # Contar por grupo
.mean()                   # Média por grupo
.agg(total="count", ...)  # Múltiplas métricas
.sort_values()            # Ordenar resultados
.head(10)                 # Top N
pd.DateOffset(months=1)   # Janela de tempo dinâmica
pd.to_datetime()          # Converter datas
```

---

## Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat&logo=fastapi)
![Plotly](https://img.shields.io/badge/Plotly-JS-3F4F75?style=flat&logo=plotly)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite)

---

*Projeto desenvolvido durante o curso kensei Cybersecurity — Semana 3*
