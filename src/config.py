"""Configurações centrais do pipeline (caminhos, período e fontes)."""
from pathlib import Path

# Diretório raiz do projeto
BASE = Path(__file__).resolve().parent.parent

RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"
RESULTS = BASE / "results"

for pasta in (RAW, PROCESSED, RESULTS):
    pasta.mkdir(parents=True, exist_ok=True)

ANO_INICIAL = 1990
ANO_FINAL = 2023

# Fontes automáticas
# PIB per capita PPP em US$ internacionais constantes (2021)
ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

WB_URL = "https://api.worldbank.org/v2/country/BRA/indicator/NY.GDP.PCAP.PP.KD"

# Arquivos locais
ONI_FILE = RAW / "oni.txt"
GDP_FILE = RAW / "gdp_ppp_brazil.json"
UNDP_FILE = RAW / "idh_e_indicadores_anuais_Brasil.xlsx"

DATASET = PROCESSED / "dataset.csv"
