"""
Gera dados simulados de ataques para demonstração.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def gerar_dados(n=1000, seed=42) -> pd.DataFrame:
    np.random.seed(seed)

    tipos = ["DDoS", "Phishing", "Ransomware", "BruteForce", "SQLInjection"]
    paises = [
        "China", "Rússia", "Estados Unidos", "Brasil", "Irã",
        "Coreia do Norte", "Índia", "Alemanha", "Ucrânia", "Nigéria",
        "Romênia", "Vietnã", "Paquistão", "Turquia", "Indonésia"
    ]

    agora = datetime.now()

    df = pd.DataFrame({
        "data": [
            agora - timedelta(
                days=np.random.randint(0, 30),
                hours=np.random.randint(0, 24),
                minutes=np.random.randint(0, 60)
            )
            for _ in range(n)
        ],
        "tipo":             np.random.choice(tipos, n, p=[0.5, 0.2, 0.1, 0.1, 0.1]),
        "pais_origem":      np.random.choice(paises, n),
        "duracao_segundos": np.random.exponential(scale=200, size=n).round(2),
        "ip_origem":        [f"{np.random.randint(1,255)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(1,255)}" for _ in range(n)],
        "severidade":       np.random.choice(["baixa", "media", "alta", "critica"], n),
    })

    return df
