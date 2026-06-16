from langchain_core.prompts import PromptTemplate



template = """
User Financial Situation:

Financial Knowledge:
{retrieval_data}

and

{retrieval_data}

Question:
{question}

Answer based on the retrieval_data and user_financial_data.
"""

recomendation_prompt = PromptTemplate(
    input_variables=["question", "retrieval_data", "user_financial_data"],
    template=template
)