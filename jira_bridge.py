from jira import JIRA
from const import USERNAME, PASSWORD, SERVER, PLATFORM_BOARD

jira_connector = JIRA(
    basic_auth=(USERNAME, PASSWORD),
    options={"server": SERVER},
)

platform_sprint_id = jira_connector.sprints(PLATFORM_BOARD)[-1].id
platform_sprint_name = jira_connector.sprints(PLATFORM_BOARD)[-1].name


def create_ticket(name, sprint, estimate):
    response = {}

    issue_dict = {
        "project": {"key": "PLAT"},
        "summary": name,
        "description": "",
        "issuetype": {"name": "Task"},
    }

    new_issue = jira_connector.create_issue(fields=issue_dict)
    response["key"] = new_issue.key

    if sprint:
        add_sprint(new_issue.key)
        response["sprint"] = f"Added to {platform_sprint_name}"

    if estimate != 0:
        add_estimate(new_issue.key, estimate)
        response["estimate"] = f"Estimate {estimate} set"

    return response


def add_estimate(issue_key, estimate):
    issue = jira_connector.issue(str(issue_key))
    issue.update(fields={"customfield_10106": estimate})


def add_sprint(issue_key):
    jira_connector.add_issues_to_sprint(
        sprint_id=platform_sprint_id, issue_keys=[str(issue_key)]
    )
