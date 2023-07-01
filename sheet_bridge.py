import gspread
from const import SHEET_NAME

client = gspread.service_account(filename="client_secret.json")


def add_ticket(issue_key: str):
    try:
        sheet, last_row_index = get_last_row()
    except Exception as e:
        return str(e)

    row = [issue_key]

    try:
        insert_ticket(row=row, index=last_row_index, sheet=sheet)
        return f"{issue_key} added to sheet"
    except Exception as e:
        return str(e)


def insert_ticket(row, index, sheet):
    for i in range(len(row)):
        sheet.update_cell(index, i + 1, row[i])


def get_last_row():
    sheet_id = get_last_created_sheet_id()
    sheet = client.open(SHEET_NAME).get_worksheet_by_id(sheet_id)
    last_row_index = len(sheet.get_all_values()) + 1
    return sheet, last_row_index


def get_last_created_sheet_id():
    sheets = client.open(SHEET_NAME).worksheets()
    return sheets[-2].id
