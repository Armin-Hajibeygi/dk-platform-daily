import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse, JSONResponse
from jira_bridge import create_ticket

app = FastAPI()


@app.get("/", include_in_schema=False)
def redirect():
    response = RedirectResponse(url="/docs")
    return response


@app.post("/create_ticket")
def create_ticket_endpoint(
    name: str = Form(...),
    sprint: bool = Form(True),
    estimate: int = Form(0),
):
    ticket = create_ticket(name, sprint, estimate)
    response_data = {"data": ticket}
    return JSONResponse(response_data, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
