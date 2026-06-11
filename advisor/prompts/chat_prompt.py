from langchain_core.prompts import PromptTemplate


template = """
You are a personal financial assistant.

Question:
{question}

Financial Data:
{financial_data}

Answer the user.
"""

chat_prompt = PromptTemplate(
    input_variables=[
        "question",
        "financial_data"
    ],
    template=template
)