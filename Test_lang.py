from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# Initialize model
llm = ChatOllama(
    model="qwen2.5:3b",  # 
    temperature=0.2,
)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You ONLY write the plain text BODY of an email reply.
You NEVER write anything else.

Forbidden things (never output them):
- subject
- subject line
- Dear
- Hi
- Hello
- Hey
- Regards
- Best regards
- Best
- Thanks
- Thank you
- Cheers
- Sincerely
- Kind regards
- signature
- name
- phone
- email address
- any closing line
- any greeting line
- markdown
- quotes
- explanation
- "Here is"
- "The reply is"

Rules you MUST follow 100%:
1. Read the incoming email carefully.
2. Write ONLY the reply paragraphs.
3. Keep professional and polite tone unless the email is casual.
4. Answer every important point from the email.
5. Output raw text only — nothing before or after the message body.

Just the email body. Nothing else."""
    ),
    ("human", "{email}")
]
)
# Run
chain = prompt | llm

def genrate(email):
    response = chain.invoke({
    "email": email
    })

    # print(response.content)
    return response.content

# res=genrate("I need the 2 days of leave in office for fever ")
# print(res)

# # ✅ Token usage (THIS IS WHAT YOU WANT)
# usage = response.response_metadata.get("token_usage", {})

# print("\nToken usage:")
# print("Prompt tokens :", usage.get("prompt_tokens"))
# print("Completion tokens :", usage.get("completion_tokens"))
# print("Total tokens :", usage.get("total_tokens"))




