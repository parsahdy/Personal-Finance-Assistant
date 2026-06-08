from langchain_core.prompts import PromptTemplate


template = """
You are a financial advisor.

User Financial Data:

Income: {total_income}
Expense: {total_expense}
Saving Rate: {saving_rate}
Largest Category: {largest_category}

Analyze the user's financial situation and provide recommendations.
"""

financial_advisor_prompt = PromptTemplate(
    input_variables=[
        "total_income",
        "total_expense",
        "saving_rate",
        "largest_category",
    ],
    template=template
)