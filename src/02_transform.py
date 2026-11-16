"""Etapa 2 - Transformação: limpa, alinha (anual) e consolida as três bases."""
import json

import numpy as np
import pandas as pd

import config as cfg


def carregar_oni():
    """ONI trimestral -> média anual da anomalia + defasagem de 1 ano."""
    df = pd.read_csv(cfg.ONI_FILE, sep=r"\s+")  # colunas: SEAS YR TOTAL ANOM
    anual = df.groupby("YR")["ANOM"].mean().rename("oni").to_frame()
    anual["oni_lag1"] = anual["oni"].shift(1)  # lag calculado ANTES do recorte
    return anual.rename_axis("year").reset_index()


def carregar_idh():
    """Arquivo do PNUD (formato longo: 1 linha por indicador e ano) -> 1 linha por ano."""
    df = pd.read_excel(cfg.UNDP_FILE)
    df = df[df["countryIsoCode"] == "BRA"]
    if df.empty:
        raise ValueError("Brasil (BRA) não encontrado no arquivo do PNUD.")

    indicadores = ["hdi", "le", "eys", "mys", "gnipc"]
    df = df[df["indicatorCode"].isin(indicadores)]
    out = (
        df.pivot(index="year", columns="indicatorCode", values="actualValue")
        .reindex(columns=indicadores)
        .loc[cfg.ANO_INICIAL : cfg.ANO_FINAL]
        .reset_index()
    )
    out.columns.name = None

    # Subíndices pela metodologia do PNUD (limites mínimo/máximo vigentes desde 2010)
    out["i_saude"] = ((out["le"] - 20) / (85 - 20)).clip(0, 1)
    i_mys = (out["mys"] / 15).clip(0, 1)
    i_eys = (out["eys"] / 18).clip(0, 1)
    out["i_educ"] = (i_mys + i_eys) / 2
    out["i_renda"] = (
        (np.log(out["gnipc"]) - np.log(100)) / (np.log(75000) - np.log(100))
    ).clip(0, 1)
    return out


def carregar_pib():
    dados = json.loads(cfg.GDP_FILE.read_text(encoding="utf-8"))
    linhas = dados[1]
    df = pd.DataFrame(
        {
            "year": [int(l["date"]) for l in linhas],
            "pib_pc_ppp": [l["value"] for l in linhas],
        }
    ).dropna()
    df["pib_pc_ppp"] = df["pib_pc_ppp"].astype(float)
    return df


def main():
    df = (
        carregar_idh()
        .merge(carregar_oni(), on="year", how="inner")
        .merge(carregar_pib(), on="year", how="inner")
    )
    df = df[df["year"].between(cfg.ANO_INICIAL, cfg.ANO_FINAL)].sort_values("year")

    # Séries de tendência (IDH, PIB) -> também em variação anual, para evitar
    # correlação espúria entre duas séries que apenas crescem ao longo do tempo
    df["ln_pib"] = np.log(df["pib_pc_ppp"])
    for coluna in ("hdi", "i_saude", "i_educ", "i_renda", "ln_pib"):
        df[f"d_{coluna}"] = df[coluna].diff()

    df.to_csv(cfg.DATASET, index=False)
    print(f"Dataset salvo em {cfg.DATASET} ({len(df)} linhas)")


if __name__ == "__main__":
    main()
