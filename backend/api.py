from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import backend.classicfication as clf

app = FastAPI()
app.mount('/static', StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend")


@app.post("/api/predict")
async def predict_text(request: Request):
    data = await request.json()
    text = data["text"]
    
    if len(text) < 150:
        return {"result": "В тексте меньше 150 символов", "error": True}

    predicted_class = clf.classification_text(text)
    
    return {"result": predicted_class, "error": False}

@app.get("/")
async def read_index_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/api/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}
