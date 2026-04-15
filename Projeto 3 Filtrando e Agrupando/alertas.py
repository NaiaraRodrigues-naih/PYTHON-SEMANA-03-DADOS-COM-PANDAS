"""
Motor de detecção e geração de alertas.
"""

from datetime import datetime
from banco import AtaquesRepo, AlertasRepo, PaisesRepo

LIMIARES = {
    "ataques_por_hora": 50,
    "duracao_media_seg": 300,
    "volume_total":      500,
}


def verificar_e_persistir() -> list[dict]:
    ataques = AtaquesRepo()
    alertas = AlertasRepo()
    paises  = PaisesRepo()

    ddos  = ataques.ultima_hora()
    ddos  = ddos[ddos["tipo"] == "DDoS"]
    agora = datetime.now().isoformat()
    gerados = []

    if ddos.empty:
        return gerados

    # Regra 1: volume por país
    for pais, total in ddos.groupby("pais_origem").size().items():
        if total >= LIMIARES["ataques_por_hora"]:
            a = {"timestamp": agora, "nivel": "CRITICO", "regra": "volume_por_pais",
                 "mensagem": f"{pais} disparou {total} ataques na última hora",
                 "valor": str(total), "limiar": str(LIMIARES["ataques_por_hora"])}
            alertas.inserir(a)
            gerados.append(a)

    # Regra 2: duração média alta
    for pais, media in ddos.groupby("pais_origem")["duracao_segundos"].mean().items():
        if media >= LIMIARES["duracao_media_seg"]:
            a = {"timestamp": agora, "nivel": "AVISO", "regra": "duracao_alta",
                 "mensagem": f"{pais} com duração média de {media:.0f}s",
                 "valor": str(round(media, 2)), "limiar": str(LIMIARES["duracao_media_seg"])}
            alertas.inserir(a)
            gerados.append(a)

    # Regra 3: país novo
    novos = paises.registrar_novos(set(ddos["pais_origem"].dropna().unique()))
    for pais in novos:
        a = {"timestamp": agora, "nivel": "INFO", "regra": "pais_novo",
             "mensagem": f"Novo país detectado: {pais}",
             "valor": pais, "limiar": None}
        alertas.inserir(a)
        gerados.append(a)

    # Regra 4: volume total
    if len(ddos) >= LIMIARES["volume_total"]:
        a = {"timestamp": agora, "nivel": "CRITICO", "regra": "volume_total",
             "mensagem": f"Volume total: {len(ddos)} ataques na última hora",
             "valor": str(len(ddos)), "limiar": str(LIMIARES["volume_total"])}
        alertas.inserir(a)
        gerados.append(a)

    return gerados
