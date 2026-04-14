import pandas as pd
import numpy as np

# Gera um dataset sujo simulando logs de acesso de rede
np.random.seed(42)

dados = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12],  # id 10 duplicado
    "ip_origem": [
        "192.168.1.1", "10.0.0.5", None, "172.16.0.3", "192.168.1.1",
        "999.999.999.999",  # IP invalido
        "10.0.0.8", "172.16.0.10", "192.168.2.50", "10.0.0.5",
        "10.0.0.5",  # linha duplicada
        None,  # ip nulo
        "192.168.3.1"
    ],
    "tipo": [
        "login", "scan", "login", None, "brute_force",
        "scan", None, "login", "exfiltration", "scan",
        "scan", "login", "ddos"
    ],
    "data": [
        "2024-01-15", "2024-01-16", "2024/01/17", "16-01-2024",
        "2024-01-18", "2024-01-19", "nao_e_data",  # data invalida
        "2024-01-20", "2024-01-21", "2024-01-22",
        "2024-01-22", "2024-01-23", "2024-01-24"
    ],
    "porta": [
        22, 80, 443, 22, 22,
        -1,   # porta invalida (negativa)
        None, 3389, 443, 80,
        80, 22, 65536  # porta invalida (fora do range)
    ],
    "tentativas": [
        3, 1, 5, None, 100,
        2, 1, 4, 7, 1,
        1, None, 9
    ]
}

df = pd.DataFrame(dados)
df.to_csv("logs_sujos.csv", index=False)
print("Dataset sujo gerado: logs_sujos.csv")
print(df)
