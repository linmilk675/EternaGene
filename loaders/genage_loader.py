import pandas as pd
import os
import zipfile
import requests
from io import BytesIO

GENAGE_ZIP_URL = "https://genomics.senescence.info/genes/human_genes.zip"
GENAGE_LOCAL_CSV = "data/genage_human.csv"

def download_and_extract_genage():
    response = requests.get(GENAGE_ZIP_URL)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as z:
        csv_name = [name for name in z.namelist() if name.endswith(".csv")][0]
        with z.open(csv_name) as csv_file:
            df = pd.read_csv(csv_file)
            os.makedirs("data", exist_ok=True)
            df.to_csv(GENAGE_LOCAL_CSV, index=False)
            return df

def load_genage_data(use_cache=True):
    if use_cache and os.path.exists(GENAGE_LOCAL_CSV):
        return pd.read_csv(GENAGE_LOCAL_CSV)
    return download_and_extract_genage()

def is_longevity_gene(gene_name, genage_df):
    return gene_name.upper() in genage_df["symbol"].str.upper().values

