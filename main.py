from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
@app.get("/")
async def root(request: Request):
    with open('database.json') as file:
        data = json.load(file)
    return templates.TemplateResponse("index.html", {"request" : request, "tododict" : data})

@app.get("/delete/{id}")
async def delete_task(request: Request, id: str):
    with open('database.json') as file:
        data = json.load(file)
    del data[id]
    with open('database.json', 'w') as file:
        json.dump(data, file)
    return RedirectResponse("/", 303)

@app.post("/add")
async def add_task(request: Request):
    with open('database.json') as file:
        data = json.load(file)
    formdata = await request.form()
    newdata = {}
    i = 1
    for identifier in data:
        newdata[str(i)] = data[identifier]
        i += 1
    newdata[str(i)] = formdata["newtodo"]
    print(newdata)
    with open('database.json','w') as file:
        json.dump(newdata,file)
    return RedirectResponse("/", 303)