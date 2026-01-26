"""Constants for the save chain."""

ALLOWED_CATEGORIES = {
    "people_management",
    "project_management",
    "budget",
    "hiring",
    "client",
    "reminder",
    "idea",
    "external_reference"
}

ALLOWED_SUBCATEGORIES = {
    "people_management": {
        "1on1", "performance_feedback", "conflict", "promotion"
    },
    "project_management": {
        "status_update", "risk", "dependency", "delivery_issue"
    },
    "hiring": {
        "interview_feedback", "offer_decision", "referral"
    }
}
