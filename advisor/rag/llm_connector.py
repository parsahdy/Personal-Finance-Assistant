from finance.services.dashboard import DashboardService
from advisor.llm import ollama_client
from advisor.prompts.recommendation_prompt import recomendation_prompt
from .rag_manager import retrieve



def llm_connector(user, question):

    docs = retrieve(question)
    retrieval_data = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    user_financial_data = DashboardService.get_summary(user=user)

    prompt_text = recomendation_prompt.format(
        question=question,
        retrieval_data=retrieval_data,
        user_financial_data=user_financial_data
    )

    return ollama_client.generate(
        prompt=prompt_text
    )