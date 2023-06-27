from jira import JIRA
from const import USERNAME, PASSWORD, SERVER, PLATFORM_BOARD, TO_DONE_ID

jira_connector = JIRA(
    basic_auth=(USERNAME, PASSWORD),
    options={"server": SERVER},
)

platform_sprint_id = jira_connector.sprints(PLATFORM_BOARD)[-1].id
platform_sprint_name = jira_connector.sprints(PLATFORM_BOARD)[-1].name


def create_ticket(name: str, assignee: str, estimate: int, sprint: bool, done: bool) -> dict:
    response = {}

    issue_dict = {
        "project": {"key": "PLAT"},
        "summary": name,
        "description": "",
        "issuetype": {"name": "Task"},
    }

    new_issue = jira_connector.create_issue(fields=issue_dict)
    new_issue_key = str(new_issue.key)
    response["key"] = new_issue_key

    if assignee:
        add_assignee(new_issue_key, assignee)
        response["assignee"] = f"Assigned to {assignee}"

    if estimate != 0:
        add_estimate(new_issue_key, estimate)
        response["estimate"] = f"Estimate {estimate} set"

    if sprint:
        add_sprint(new_issue_key)
        response["sprint"] = f"Added to {platform_sprint_name}"

    if done:
        set_done(new_issue_key)
        response["status"] = f"Mark as done"

    return response


def user_map(name: str) -> str:
    pass


def add_assignee(issue_key: str, assignee: str) -> None:
    pass


def add_estimate(issue_key: str, estimate: int) -> None:
    issue = jira_connector.issue(issue_key)
    issue.update(fields={"customfield_10106": estimate})


def add_sprint(issue_key: str) -> None:
    jira_connector.add_issues_to_sprint(
        sprint_id=platform_sprint_id, issue_keys=[issue_key]
    )


def set_done(issue_key: str) -> None:
    jira_connector.transition_issue(issue_key, TO_DONE_ID)
