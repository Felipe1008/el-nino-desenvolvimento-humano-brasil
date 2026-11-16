"""Etapa 3 - Teste e validação: esquema (Pydantic) + testes de consistência."""
import sys

import pandas as pd
from pydantic import BaseModel, Field, ValidationError

import config as cfg


class Observacao(BaseModel):
    year: int = Field(ge=cfg.ANO_INICIAL, le=cfg.ANO_FINAL)
    hdi: float = Field(ge=0, le=1)
    i_saude: float = Field(ge=0, le=1)
    i_educ: float = Field(ge=0, le=1)
    i_renda: float = Field(ge=0, le=1)
    oni: float = Field(ge=-4, le=4)
    oni_lag1: float = Field(ge=-4, le=4)
    pib_pc_ppp: float = Field(gt=0)


def main():
    df = pd.read_csv(cfg.DATASET)
    erros = []

    # Teste 1: esquema, tipos e intervalos válidos (linha a linha)
    for registro in df.to_dict("records"):
        try:
            Observacao(**registro)
        except ValidationError as e:
            erros.append(f"Ano {registro.get('year')}: {e.errors()[0]['msg']}")

    # Teste 2: série completa e sem anos faltando
    esperados = set(range(cfg.ANO_INICIAL, cfg.ANO_FINAL + 1))
    faltando = esperados - set(df["year"])
    if faltando:
        erros.append(f"Anos ausentes: {sorted(faltando)}")

    # Teste 3: o IDH recalculado pelos subíndices deve bater com o IDH publicado
    idh_calc = (df["i_saude"] * df["i_educ"] * df["i_renda"]) ** (1 / 3)
    dif_max = (df["hdi"] - idh_calc).abs().max()
    print(f"Maior diferença IDH publicado x recalculado: {dif_max:.4f}")
    if dif_max > 0.01:
        erros.append("IDH recalculado diverge do publicado (> 0,01): revise os subíndices.")

    if erros:
        print("\nFALHAS NA VALIDAÇÃO:")
        for e in erros:
            print(" -", e)
        sys.exit(1)
    print(f"Validação aprovada ({len(df)} observações).")


if __name__ == "__main__":
    main()
