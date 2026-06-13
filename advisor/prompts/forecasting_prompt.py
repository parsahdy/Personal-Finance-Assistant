from langchain_core.prompts import PromptTemplate


template = """
You are Personal finance predictor.
you forecast the future income, expense or saving rate of a user based on data given to you.

data: {data}

"""

forcasting_propmt = PromptTemplate(
    input_variables=["data"],
    template=template
)