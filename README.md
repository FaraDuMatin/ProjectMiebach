# SLA Tower

Gives every Jira ticket an honest deadline in its own country's working calendar, and shows what breaches next.

```mermaid
flowchart LR
    jira@{ img: "https://raw.githubusercontent.com/FaraDuMatin/ProjectMiebach/main/docs/jira.png", label: "Jira Cloud", pos: "b", w: 60, h: 60 }

    subgraph azure["Azure App Service"]
        direction TB
        django@{ img: "https://raw.githubusercontent.com/FaraDuMatin/ProjectMiebach/main/docs/django.png", label: "SLA engine", pos: "b", w: 60, h: 60 }
        webhook["Webhook"]
        sync["sync_jira"]
        api["REST API"]

        webhook --> django
        sync --> django
        django --> api
    end

    db@{ img: "https://raw.githubusercontent.com/FaraDuMatin/ProjectMiebach/main/docs/postgress.png", label: "PostgreSQL", pos: "b", w: 60, h: 60 }
    board@{ img: "https://raw.githubusercontent.com/FaraDuMatin/ProjectMiebach/main/docs/react.png", label: "React board", pos: "b", w: 60, h: 60 }

    jira -- "issue created or updated" --> webhook
    jira -- "periodic pull" --> sync
    django -- "due date" --> db
    django -- "due date written back" --> jira
    db --> api
    api --> board
```
