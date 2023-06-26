import uvicorn
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status, Request
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
def redirect():
    response = RedirectResponse(url="/docs")
    return response


@app.post("/create_ticket")
def create_ticket(
    name: str = Form(...),
    estimate: int = Form(0),
):
    resp = {"name": name, "estimate": estimate}
    return resp


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
