"""Etapa 1 - Extração: baixa ONI (NOAA) e PIB per capita PPP (Banco Mundial).
O arquivo do IDH (PNUD) deve ser baixado manualmente e salvo em data/raw/."""
import sys

import requests

import config as cfg


def baixar(url, destino, params=None):
    resposta = requests.get(url, params=params, timeout=60)
    resposta.raise_for_status()
    destino.write_bytes(resposta.content)
    print(f"OK: {destino.name} ({len(resposta.content)} bytes)")


def main():
    baixar(cfg.ONI_URL, cfg.ONI_FILE)
    baixar(
        cfg.WB_URL,
        cfg.GDP_FILE,
        params={
            "format": "json",
            "per_page": 100,
            "date": f"{cfg.ANO_INICIAL}:{cfg.ANO_FINAL}",
        },
    )
    if not cfg.UNDP_FILE.exists():
        print(
            f"\nATENÇÃO: baixe o arquivo de série histórica do IDH no Data Center "
            f"do PNUD e salve como:\n  {cfg.UNDP_FILE}"
        )
        sys.exit(1)
    print("Extração concluída.")


if __name__ == "__main__":
    main()
