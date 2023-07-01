import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse, JSONResponse
from jira_bridge import create_ticket
from sheet_bridge import add_ticket

app = FastAPI()


@app.get("/", include_in_schema=False)
def redirect():
    response = RedirectResponse(url="/docs")
    return response


@app.post("/create_ticket")
def create_ticket_endpoint(
    name: str = Form(...),
    assignee: str = Form(None),
    estimate: int = Form(0),
    set_as_support: bool = Form(False),
    sprint: bool = Form(True),
    done: bool = Form(False),
    add_to_sheet: bool = Form(False),
):
    response_data = {}

    ticket = create_ticket(name, assignee, estimate, set_as_support, sprint, done)
    response_data["jira"] = ticket

    if add_to_sheet:
        sheet = add_ticket(str(ticket["key"]))
        response_data["GSheet"] = sheet

    return JSONResponse(response_data, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
