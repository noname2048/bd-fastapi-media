from starlette.responses import FileResponse
import uvicorn
import shutil
from typing import Optional
from pathlib import Path as SysPath
from fastapi import FastAPI, Request, Path, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
repo_dir = SysPath(__file__).parent.parent


@app.get("/")
async def hello():
    return {"message": "hello"}


@app.get("/form")
async def ret_form(request: Request):
    return templates.TemplateResponse(
        name="get_form.html", context={"request": request}
    )


@app.post("/form")
async def res_form(request: Request, a: Optional[UploadFile] = File(...)):
    with open(repo_dir / "media" / a.filename, "wb") as buffer:
        shutil.copyfileobj(a.file, buffer)
    return templates.TemplateResponse(
        "res.jinja.html", context={"request": request, "filename": a.filename}
    )


@app.get("/image/{filename}")
async def image(filename: str = Path(...)):
    return FileResponse(f"media/{filename}")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
