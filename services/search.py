import pandas as pd
import services.constants as cl
import re
from pathlib import Path



def search_on_csv(file_path: str | None = None,Disciplinas: list[str]|None = None, Direcs: list[str]|None = None):

    BASE_DIR = Path(__file__).resolve().parent.parent

    if Disciplinas is None:
        Disciplinas = cl.DISCIPLINAS
    if Direcs is None:
        Direcs = cl.DIRECs
    else:
        temp_list = []
        for item in Direcs:
            temp_list.append(cl.DIRECs[int(item)-1])
        Direcs = temp_list

    #if file_path is None:
    file_path = BASE_DIR / "data" / "Relatorio_Servidores.csv"
    print(file_path)
    prof_per_disci = []
    total_prof = 0
    total_prof_nt = 0
    total_prof_temp = 0
    payload1 = {}
    prof_especial = []

#====================================================================================
    df = pd.read_csv(file_path)

    df["TIPO UNIDADE"] = (df["TIPO UNIDADE"].fillna("").apply(lambda s: re.findall(r"\d{2}ª DIREC", s)))

    df["DISCIPLINA"] = df["DISCIPLINA"].fillna("").str.split(", ")

    df["FUNÇÃO"] = df["FUNÇÃO"].fillna("").str.split(", ")


#======================== Prof in direc ==============================================

    prof_sala_direc = (
        df["FUNÇÃO"].apply(lambda x: "SALA DE AULA" in x)
        & df["TIPO UNIDADE"].apply(lambda x: any(i in Direcs for i in x))
        ).sum().item()

    print(prof_sala_direc)

    for D in Disciplinas:
        prof_per_disci.append(
            (
                df["DISCIPLINA"].apply(lambda x: D in x) 
                & (df["TIPO UNIDADE"].apply(lambda x: any(i in Direcs for i in x)))
            ).sum().item()
        )

    Especiais = ["AEE","Professor de Educação Especial Intérprete/Tradutor de Libras","Professor de Educação Especial","AEE LIBRAS"]
    
    prof_especial=(
        (
            df["DISCIPLINA"].apply(lambda x: any(i in Especiais for i in x)) 
            & df["TIPO UNIDADE"].apply(lambda x: any(i in Direcs for i in x))
            & df["FUNÇÃO"].apply(lambda x: "SALA DE AULA" in x)
        ).sum()
    )
    print(f'prof_especial:{prof_especial}\n')


#====================================================================================
    df = df.rename(columns=lambda c: c.replace(" ", "_"))

    for row in df.itertuples():
        if 'PRO' in row.CARGO and any(i in Direcs for i in row.TIPO_UNIDADE) :
            total_prof+=1
            if ('PROFESSOR TEMPORARIO' in row.CARGO):
                total_prof_temp += 1
                if ('PERM' not in row.CARGO):
                    total_prof_nt = total_prof-1
    
#====================================================================================
    
    chart_data = {d: prof_per_disci[idx] for idx, d in enumerate(Disciplinas)}

    summary = {
        "total_professores": total_prof,
        "professores_nao_temporarios": total_prof_nt,
        "professores_em_sala": prof_sala_direc,
    }

    print(summary)
 
    return summary, chart_data

