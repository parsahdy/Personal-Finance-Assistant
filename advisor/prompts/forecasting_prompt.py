from langchain_core.prompts import PromptTemplate


template = """
You are a personal finance predictor.

User question:
{question}

Forecast result:
{data}

Explain the prediction in simple language.
"""

forcasting_propmt = PromptTemplate(
    input_variables=["question", "data"],
    template=template
)