import requests
from django.conf import settings


class JiraClient:
    def __init__(self):
        self.base_url = settings.JIRA_BASE_URL.rstrip("/") + "/rest/api/3"
        self.auth = (settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
        self.fields = "summary,status,priority,created,duedate," + settings.JIRA_COUNTRY_FIELD

    def get(self, path, params=None):
        response = requests.get(self.base_url + path, auth=self.auth, params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    def put(self, path, body):
        response = requests.put(self.base_url + path, auth=self.auth, json=body, timeout=15)
        response.raise_for_status()

    def search_issues(self, jql):
        issues = []
        next_page_token = None
        while True:
            params = {"jql": jql, "maxResults": 100, "fields": self.fields}
            if next_page_token:
                params["nextPageToken"] = next_page_token
            data = self.get("/search/jql", params)
            issues.extend(data["issues"])
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                return issues

    def get_issue(self, key):
        return self.get("/issue/" + key, {"fields": self.fields})

    def set_due_date(self, key, date):
        self.put("/issue/" + key, {"fields": {"duedate": date.isoformat()}})
