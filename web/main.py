from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pathlib import Path
import services.constants as cl
from services.search import search_on_csv
from services.search_inep import total_count

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

#app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/")
def render_dashboard(request: Request):
    """Renders the initial empty dashboard page."""
    return templates.TemplateResponse(
        request=request,
        name = "index.html",
        context = {
            "direcs": cl.DIRECs,
            "disciplinas": cl.DISCIPLINAS,
            "options_teachers": cl.options_professores,
            "options_students": cl.options_students,
            "instructions": cl.INSTRUCTIONS,
        },
    )

@app.post("/search")
def run_search(
    request: Request,
    direcs: List[str] = Form(default=[]),
    data_origin: str = Form(...),
    group_type: Optional[str] = Form(None),
    selections: List[str] = Form(None)
):

    outgoing_direcs = [str(i + 1) for i, d in enumerate(cl.DIRECs) if d in direcs]

    summary = None
    chart_data = {}

    if data_origin == "SIGEDUC":
        summary, chart_data = search_on_csv(
            Disciplinas = selections,
            Direcs = outgoing_direcs
        )

    else:
        chart_data = total_count(
            direc=outgoing_direcs,
            selections=selections,
            group_type=group_type
        )

    return templates.TemplateResponse(
        name = "partials/results.html",
        request= request,
        context ={
            "origin": data_origin,
            "summary": summary,
            "chart_data": chart_data,
        },
    )