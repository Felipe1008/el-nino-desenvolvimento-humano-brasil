"""Etapa 4 - Anslise estatistica: correlacao de Pearson e regressao com defasagem.

Especificacoes rodadas:
  - principal       : ONI, ONI(t-1) e controle de PIB (em nivel e em variacao anual)
  - sem_pib         : ONI e ONI(t-1), SEM o PIB (efeito total, incluindo o canal economico)
  - sem_2020-2022   : igual a principal, excluindo os anos da pandemia (so variacao anual)
As especificacoes extras usam apenas a variacao anual, pois as regressoes em nivel
apresentam forte autocorrelacao (Durbin-Watson baixo) e sao apenas complementares.
"""
import pandas as pd
import statsmodels.api as sm
from scipy.stats import pearsonr

import config as cfg

DEPENDENTES = {
    "hdi": "IDH",
    "i_saude": "Saúde (longevidade)",
    "i_educ": "Educação",
    "i_renda": "Renda",
}
ALFA = 0.05
ANOS_PANDEMIA = (2020, 2021, 2022)  


def correlacoes(df):
    linhas = []
    for dep, nome in DEPENDENTES.items():
        for versao, coluna in (("nível", dep), ("variação anual", f"d_{dep}")):
            sub = df[["oni", coluna]].dropna()
            r, p = pearsonr(sub["oni"], sub[coluna])
            linhas.append(
                {"dimensão": nome, "versão": versao, "r": r, "p_valor": p, "n": len(sub)}
            )
    out = pd.DataFrame(linhas)
    # Correção de Bonferroni pelo número de testes realizados
    out["p_bonferroni"] = (out["p_valor"] * len(out)).clip(upper=1)
    out["significativo_5%"] = out["p_valor"] < ALFA
    out["significativo_5%_bonferroni"] = out["p_bonferroni"] < ALFA
    return out


def regressao(df, dep, nome, versao, especificacao="principal"):
    if versao == "variação anual":
        colunas = [f"d_{dep}", "oni", "oni_lag1"]
        if especificacao != "sem_pib":
            colunas.append("d_ln_pib")
    else:
        colunas = [dep, "oni", "oni_lag1", "ln_pib"]

    base = df
    if especificacao == "sem_2020-2022":
        base = df[~df["year"].isin(ANOS_PANDEMIA)]

    dados = base[colunas].dropna()
    y = dados[colunas[0]]
    X = sm.add_constant(dados[colunas[1:]])
    # Erros-padrão robustos à autocorrelação (HAC / Newey-West)
    modelo = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 1})

    sufixo = "" if especificacao == "principal" else f"_{especificacao}"
    arquivo = f"regressao_{dep}_{versao.replace(' ', '_')}{sufixo}.txt"
    (cfg.RESULTS / arquivo).write_text(str(modelo.summary()), encoding="utf-8")

    linhas = []
    for termo in modelo.params.index:
        linhas.append(
            {
                "dimensão": nome,
                "versão": versao,
                "especificação": especificacao,
                "termo": termo,
                "coeficiente": modelo.params[termo],
                "erro_padrão": modelo.bse[termo],
                "p_valor": modelo.pvalues[termo],
                "R2": modelo.rsquared,
                "n": int(modelo.nobs),
            }
        )
    return linhas


def main():
    df = pd.read_csv(cfg.DATASET)

    corr = correlacoes(df)
    corr.to_csv(cfg.RESULTS / "correlacoes.csv", index=False)
    corr.to_excel(cfg.RESULTS / "correlacoes.xlsx", index=False)
    print(corr.round(4).to_string(index=False))

    linhas = []
    for dep, nome in DEPENDENTES.items():
        linhas += regressao(df, dep, nome, "variação anual", "principal")
        linhas += regressao(df, dep, nome, "nível", "principal")
        linhas += regressao(df, dep, nome, "variação anual", "sem_pib")
        linhas += regressao(df, dep, nome, "variação anual", "sem_2020-2022")
    reg = pd.DataFrame(linhas)
    reg.to_csv(cfg.RESULTS / "regressoes.csv", index=False)
    # O Excel (.xlsx) preserva os números sem corromper a notação científica
    reg.to_excel(cfg.RESULTS / "regressoes.xlsx", index=False)

    # Resumo comparativo: coeficientes do ONI em cada especificação
    resumo = reg[reg["termo"].isin(["oni", "oni_lag1"])]
    resumo = resumo[resumo["versão"] == "variação anual"]
    print("\nCoeficientes do ONI (variação anual) por especificação:")
    print(
        resumo[["dimensão", "especificação", "termo", "coeficiente", "p_valor", "n"]]
        .round(4)
        .to_string(index=False)
    )
    print(f"\nResultados salvos em {cfg.RESULTS}")


if __name__ == "__main__":
    main()
