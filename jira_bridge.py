from jira import JIRA
from const import USERNAME, PASSWORD, SERVER, PLATFORM_BOARD, TO_DONE_ID

jira_connector = JIRA(
    basic_auth=(USERNAME, PASSWORD),
    options={"server": SERVER},
)


def create_ticket(
    name: str,
    assignee: str,
    estimate: float,
    set_as_support: bool,
    sprint: bool,
    done: bool,
) -> dict:
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
    response["url"] = f"https://dkjira.digikala.com/browse/{new_issue_key}"

    if assignee:
        response["assignee"] = add_assignee(new_issue_key, assignee)

    if estimate != 0:
        response["estimate"] = add_estimate(new_issue_key, estimate)

    if set_as_support:
        response["epic"] = set_support_epic(new_issue_key)
        response["impact"] = set_impact(new_issue_key)

    if sprint:
        response["sprint"] = add_sprint(new_issue_key)

    if done:
        response["status"] = set_done(new_issue_key)

    return response


def get_username(name: str) -> str:
    user_map = {
        "armin": "armin.hajibeygi",
        "ali": "a.daneshmand",
        "parsa": "mo.rostami",
        "bahram": "amir.bahrami",
        "milad": "m.teimouri",
        "hashem": "MohammadMahdi.Saeedi",
        "mehdi": "MohammadMahdi.Saeedi",
    }
    return user_map.get(name.lower(), None)


def add_assignee(issue_key: str, assignee: str) -> str:
    username = get_username(assignee)
    issue = jira_connector.issue(issue_key)
    try:
        issue.update(assignee={"name": username})
        return f"Assigned to {username}"
    except:
        return "Can't Assign"


def add_estimate(issue_key: str, estimate: float) -> str:
    issue = jira_connector.issue(issue_key)
    ESTIMATE_FIELD = "customfield_10106"

    try:
        issue.update(fields={ESTIMATE_FIELD: estimate})
        return f"Estimate {estimate} set"
    except:
        return "Can't set the estimate"


def set_support_epic(issue_key: str) -> str:
    EPIC_FIELD = "customfield_10102"
    SUPPORT_EPIC_KEY = "PLAT-362"
    issue = jira_connector.issue(issue_key)

    try:
        issue.update(fields={EPIC_FIELD: SUPPORT_EPIC_KEY})
        return "Support Epic Set"
    except:
        return f"Can't set Support Epic"


def set_impact(issue_key: str) -> str:
    IMPACT_FIELD = "customfield_10201"
    SUPPORT_IMPACT = "30"
    issue = jira_connector.issue(issue_key)

    try:
        issue.update(fields={IMPACT_FIELD: {"value": SUPPORT_IMPACT}})
        return f"Set impact 30"
    except:
        return f"Can't set the impact"


def add_sprint(issue_key: str) -> str:
    platform_sprint_id = jira_connector.sprints(PLATFORM_BOARD)[-1].id
    platform_sprint_name = jira_connector.sprints(PLATFORM_BOARD)[-1].name

    try:
        jira_connector.add_issues_to_sprint(
            sprint_id=platform_sprint_id, issue_keys=[issue_key]
        )
        return f"Added to {platform_sprint_name}"
    except:
        return "Can't set the sprint"


def set_done(issue_key: str) -> str:
    try:
        jira_connector.transition_issue(issue_key, TO_DONE_ID)
        return "Mark as done"
    except:
        return "Can't move to done"
