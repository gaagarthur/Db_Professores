import pandas as pd
import constants as cl
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "Relatorio_Servidores.csv"

#====================================================================================
df = pd.read_csv(file_path)

df = df.rename(columns=lambda c: c.replace(" ", "_").replace("/", "_"))

for row in df.itertuples():

    if "DIREC" not in row.TIPO_UNIDADE and "SETOR" in row.TIPO_UNIDADE and "DIREC" in row.ESCOLA_SETOR_UNIDADE:
        df.loc[row.Index, "TIPO_UNIDADE"] = row.ESCOLA_SETOR_UNIDADE

df["TIPO_UNIDADE"] = (df["TIPO_UNIDADE"].fillna("").apply(lambda s: re.findall(r"\d{2}ª DIREC", s)))

df["DISCIPLINA"] = df["DISCIPLINA"].fillna("").str.split(", ")

df["FUNÇÃO"] = df["FUNÇÃO"].fillna("").str.split(", ")

df["ESCOLA_SETOR_UNIDADE"] = df["ESCOLA_SETOR_UNIDADE"].fillna("").str.split(", ")

df["CARGO"] = df["CARGO"].fillna("").str.split(", ")



clean_file_path = BASE_DIR / "data" / "clean_Relatorio_Servidores.parquet"

df.to_parquet(clean_file_path, index=False)


