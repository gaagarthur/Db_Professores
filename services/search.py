import pandas as pd
import services.constants as cl
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

    file_path = BASE_DIR / "data" / "clean_Relatorio_Servidores.parquet"
    print(file_path)
    prof_per_disci = []

    total_prof = 0
    prof_perm = 0
    prof_temp = 0
    payload1 = {}
    prof_especial = []

#====================================================================================
    df = pd.read_parquet(file_path)

    prof_sala_direc = (
        df["FUNÇÃO"].apply(lambda x: "SALA DE AULA" in x)
        & df["TIPO_UNIDADE"].apply(lambda x: any(i in Direcs for i in x))
        ).sum().item()

    #print(f"sala de aula: {prof_sala_direc}")

    for D in Disciplinas:
        prof_per_disci.append(
            (
                df["DISCIPLINA"].apply(lambda x: D in x) 
                & (df["TIPO_UNIDADE"].apply(lambda x: any(i in Direcs for i in x)))
            ).sum().item()
        )


    prof_especial=(
        (
            df["DISCIPLINA"].apply(lambda x: any(i in cl.Especiais for i in x)) 
            & df["TIPO_UNIDADE"].apply(lambda x: any(i in Direcs for i in x))
            & df["FUNÇÃO"].apply(lambda x: "SALA DE AULA" in x)
        ).sum()
    )
    #print(f'prof_especial:{prof_especial}\n')


#====================================================================================

    for row in df.itertuples():
        if any(d in Direcs for d in row.TIPO_UNIDADE):
            if any(term in cargo for cargo in row.CARGO for term in cl.prof_terms):
                total_prof += 1
            for cargo in row.CARGO:
                if any(i in cargo for i in cl.lookup_prof_perm):
                    prof_perm +=1
                if any(i in cargo for i in cl.lookup_prof_temp):
                    prof_temp += 1
      
#====================================================================================
    
    chart_data = {d: prof_per_disci[idx] for idx, d in enumerate(Disciplinas)}

    summary = {
        "total_professores": total_prof,
        "professores_nao_temporarios": prof_perm,
        "professores_temporarios": prof_temp,
        "professores_em_sala": prof_sala_direc,
        "professores_special_ed": prof_especial,
    }

    #print(summary)
 
    return summary, chart_data

