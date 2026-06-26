import random
import csv

# =========================
# INTENTS
# =========================

INTENTS = {
    "complaint": {
        "anger": [
            "this is unacceptable",
            "i am extremely unhappy with this",
            "this has been very frustrating",
            "i am fed up with this issue",
        ],
        "polite": [
            "i am not satisfied with the service",
            "this did not meet my expectations",
            "i expected better handling",
        ],
        "indirect": [
            "this issue keeps happening",
            "this problem has occurred again",
            "i am surprised this is still unresolved",
        ],
        "escalation": [
            "this needs immediate attention",
            "i want this issue escalated",
            "this matter requires urgent resolution",
        ],
    },

    "service_issue": {
        "delay": [
            "no one is responding",
            "still waiting for a response",
            "support has not replied yet",
        ],
        "pending": [
            "my issue is unresolved",
            "the request is still pending",
            "this ticket is not closed",
        ],
        "followup": [
            "following up on my request",
            "checking status of my issue",
            "requesting an update",
        ],
    },

    "connectivity_issue": {
        "slow": [
            "internet speed is very slow",
            "network performance is poor",
            "connection speed has dropped",
        ],
        "unstable": [
            "connection keeps disconnecting",
            "wifi is unstable",
            "network drops frequently",
        ],
        "impact": [
            "unable to work due to internet",
            "network issues affecting work",
            "connectivity disrupting tasks",
        ],
    },

    "it_support": {
        "hardware": [
            "printer is not working",
            "keyboard is broken",
            "monitor not displaying",
        ],
        "startup": [
            "laptop not turning on",
            "system fails to boot",
            "computer does not start",
        ],
        "software": [
            "application keeps crashing",
            "software not opening",
            "system running very slow",
        ],
    },

    "leave_request": {
        "formal": [
            "i would like to apply for leave",
            "requesting approval for leave",
            "submitting a leave request",
        ],
        "casual": [
            "i need a day off",
            "can i take leave tomorrow",
            "planning to take leave",
        ],
        "urgent": [
            "need urgent leave approval",
            "leave required due to emergency",
            "immediate leave needed",
        ],
    },

    "salary_query": {
        "missing": [
            "salary not credited",
            "payment not received",
            "pay missing from account",
        ],
        "incorrect": [
            "salary amount incorrect",
            "wrong salary credited",
            "payroll calculation issue",
        ],
        "delay": [
            "salary delayed this month",
            "payment pending",
            "payroll processing delayed",
        ],
    },

    "account_issue": {
        "login": [
            "cannot login to account",
            "unable to sign in",
            "login failing repeatedly",
        ],
        "locked": [
            "account locked",
            "access blocked",
            "account disabled",
        ],
        "reset": [
            "password reset not working",
            "reset link expired",
            "unable to change password",
        ],
    },

    "support_request": {
        "general": [
            "need assistance",
            "please help me",
            "requesting support",
        ],
        "urgent": [
            "need immediate help",
            "urgent support required",
            "please assist urgently",
        ],
    },

    "general_question": {
        "movies": [
            "suggest a good movie",
            "what should i watch",
            "recommend a film",
        ],
        "series": [
            "recommend a web series",
            "any good series to watch",
            "popular shows suggestion",
        ],
        "technology": [
            "which phone should i buy",
            "best laptop for students",
            "recommend good gadgets",
        ],
    },

    "personal_advice": {
        "finance": [
            "how can i save money",
            "tips to manage expenses",
            "need financial advice",
        ],
        "mental": [
            "feeling stressed lately",
            "i feel anxious",
            "how to handle stress",
        ],
        "productivity": [
            "how to improve focus",
            "difficulty concentrating",
            "time management tips",
        ],
    },

    "general_query": {
        "status": [
            "any update on my request",
            "please confirm status",
            "waiting for an update",
        ],
        "followup": [
            "just checking in",
            "following up",
            "checking progress",
        ],
    },

    "positive_feedback": {
        "appreciation": [
            "thank you for the quick support",
            "great service provided",
            "very helpful assistance",
        ],
        "satisfaction": [
            "issue resolved successfully",
            "happy with the service",
            "problem solved",
        ],
    },
}

# =========================
# INTENT-AWARE OPERATORS
# =========================

OPENERS_SUPPORT = [
    "dear team,",
    "hi support team,",
    "hello,",
    "please note that",
    "i am writing to inform you that",
    "i am disappointed to inform that",
    "",
]

OPENERS_GENERAL = [
    "hi,",
    "hello,",
    "just wanted to ask",
    "could you please suggest",
    "",
]

CONTEXTS_SUPPORT = [
    "",
    "since yesterday",
    "for the past few days",
    "during working hours",
    "on multiple occasions",
    "after the recent update",
]

CONTEXTS_GENERAL = [
    "",
    "today",
    "recently",
    "this week",
]

CLOSERS_SUPPORT = [
    "",
    "please look into this",
    "requesting your assistance",
    "this needs urgent attention",
]

CLOSERS_GENERAL = [
    "",
    "thanks in advance",
    "looking forward to your response",
]

# =========================
# SENTENCE GENERATOR
# =========================

def generate_sentence(core, intent):
    if intent in ["general_question", "personal_advice", "positive_feedback"]:
        return " ".join(
            filter(
                None,
                [
                    random.choice(OPENERS_GENERAL),
                    core,
                    random.choice(CONTEXTS_GENERAL),
                    random.choice(CLOSERS_GENERAL),
                ]
            )
        )
    else:
        return " ".join(
            filter(
                None,
                [
                    random.choice(OPENERS_SUPPORT),
                    core,
                    random.choice(CONTEXTS_SUPPORT),
                    random.choice(CLOSERS_SUPPORT),
                ]
            )
        )

# =========================
# DATA GENERATION
# =========================

ROWS_PER_INTENT = 150
rows = []

for intent, groups in INTENTS.items():
    semantic_groups = list(groups.values())

    for _ in range(ROWS_PER_INTENT):
        group = random.choice(semantic_groups)
        core_text = random.choice(group)
        sentence = generate_sentence(core_text, intent)
        rows.append([sentence, intent])

with open("intent_Dataset_2.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "intent"])
    writer.writerows(rows)

print("✅ Dataset generated:", len(rows), "rows")

