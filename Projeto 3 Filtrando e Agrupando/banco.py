"""
Camada de acesso ao banco de dados (SQLite).
"""

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

engine = create_engine("sqlite:///soc.db", echo=False)

DDL = """
CREATE TABLE IF NOT EXISTS ataques (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    data             TIMESTAMP NOT NULL,
    tipo             TEXT NOT NULL,
    pais_origem      TEXT,
    duracao_segundos REAL,
    ip_origem        TEXT,
    severidade       TEXT
);

CREATE TABLE IF NOT EXISTS alertas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp    TIMESTAMP NOT NULL,
    nivel        TEXT NOT NULL,
    regra        TEXT NOT NULL,
    mensagem     TEXT NOT NULL,
    valor        TEXT,
    limiar       TEXT,
    resolvido    INTEGER DEFAULT 0,
    resolvido_em TIMESTAMP
);

CREATE TABLE IF NOT EXISTS paises_conhecidos (
    pais         TEXT PRIMARY KEY,
    primeira_vez TIMESTAMP NOT NULL
);
"""

def iniciar_banco():
    with engine.connect() as conn:
        for stmt in DDL.strip().split(";"):
            if stmt.strip():
                conn.execute(text(stmt))
        conn.commit()


class AtaquesRepo:
    def inserir(self, df: pd.DataFrame):
        df.to_sql("ataques", engine, if_exists="append", index=False)

    def ultima_hora(self) -> pd.DataFrame:
        return pd.read_sql(
            "SELECT * FROM ataques WHERE data >= datetime('now','-1 hour')",
            engine, parse_dates=["data"]
        )

    def por_pais_periodo(self, horas: int = 24) -> pd.DataFrame:
        return pd.read_sql(f"""
            SELECT
                pais_origem,
                COUNT(*)               AS total_ataques,
                ROUND(AVG(duracao_segundos), 2) AS media_duracao,
                MAX(duracao_segundos)  AS maior_ataque
            FROM ataques
            WHERE data >= datetime('now', '-{horas} hours')
            GROUP BY pais_origem
            ORDER BY total_ataques DESC
        """, engine)

    def historico_diario(self, dias: int = 30) -> pd.DataFrame:
        return pd.read_sql(f"""
            SELECT DATE(data) AS dia, tipo, COUNT(*) AS total
            FROM ataques
            WHERE data >= datetime('now', '-{dias} days')
            GROUP BY dia, tipo
            ORDER BY dia
        """, engine)


class AlertasRepo:
    def inserir(self, alerta: dict):
        pd.DataFrame([alerta]).to_sql("alertas", engine, if_exists="append", index=False)

    def abertos(self) -> pd.DataFrame:
        return pd.read_sql(
            "SELECT * FROM alertas WHERE resolvido = 0 ORDER BY timestamp DESC",
            engine, parse_dates=["timestamp"]
        )

    def resolver(self, alerta_id: int):
        with engine.connect() as conn:
            conn.execute(text(
                "UPDATE alertas SET resolvido=1, resolvido_em=datetime('now') WHERE id=:id"
            ), {"id": alerta_id})
            conn.commit()

    def historico(self, dias: int = 7) -> pd.DataFrame:
        return pd.read_sql(f"""
            SELECT DATE(timestamp) AS dia, nivel, COUNT(*) AS total
            FROM alertas
            WHERE timestamp >= datetime('now', '-{dias} days')
            GROUP BY dia, nivel
            ORDER BY dia
        """, engine)


class PaisesRepo:
    def conhecidos(self) -> set:
        df = pd.read_sql("SELECT pais FROM paises_conhecidos", engine)
        return set(df["pais"].tolist())

    def registrar_novos(self, paises: set) -> set:
        conhecidos = self.conhecidos()
        novos = paises - conhecidos
        if novos:
            pd.DataFrame({
                "pais": list(novos),
                "primeira_vez": datetime.now()
            }).to_sql("paises_conhecidos", engine, if_exists="append", index=False)
        return novos
