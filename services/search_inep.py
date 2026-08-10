import pandas as pd
import json
from pathlib import Path
from services.columns_to_search import students_columns, teachers_columns

def total_count(direc: list[str] | None = None, selections: list[str] | None = None, group_type: str | None = None):
    if not selections or not group_type:
        return {}

    if direc is None:
        direc = [str(i) for i in range(1, 17)]

    if group_type == "Professores":
        searchable_dict = teachers_columns
        filename = "NUMBER_TEACHERS_2025.csv"
    else:
        searchable_dict = students_columns
        filename = "MATRICULAS.csv"
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_file = BASE_DIR / "data" / filename
    direcs_json_file = BASE_DIR / "data" / "direcs.json"

    df = pd.read_csv(data_file)
    output_dict = {}

    with open(direcs_json_file, "r", encoding="utf-8") as f:
        direcs_json = json.load(f)

    for item in selections:
        if item not in searchable_dict:
            continue
        for col in searchable_dict[item]:
            result = 0
            for d in direc:
                mask = df.iloc[:, 0].isin(direcs_json[d])
                result += df.loc[mask, col].sum().sum()
            output_dict.setdefault(item, []).append((col, int(result)))

    return output_dict

