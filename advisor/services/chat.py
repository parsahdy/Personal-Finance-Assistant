from finance.services.dashboard import DashboardService
from finance.services.reports import ReportService
from finance.services.budgeting import BudgetService

from advisor.services.intentclassifier import IntentClassifier
from advisor.prompts.chat_prompt import chat_prompt
from advisor.llm.ollama_client import OllamaClient


class FinancialChatServices:

    @staticmethod
    def chat(user, question):
        
        question = question.lower()

        intent = IntentClassifier.classify(
            question=question 
        )

        action = intent.get("action")
        year = intent.get("year")
        month = intent.get("month")
        category = intent.get("category")

        if action == "largest_income":
            data = DashboardService.get_largest_income(
                user=user,
                year=year,
                month=month
            )

        elif action == "largest_expense":
            data = DashboardService.get_largest_expense(
                user=user,
                year=year,
                month=month
            )
        
        elif action == "monthly_income":
            data = ReportService.get_monthly_summary(
                user=user,
                year=year,
                month=month
            )
        
        elif action == "monthly_expense":
            data = ReportService.get_monthly_summary(
                user=user,
                year=year,
                month=month
            )
        
        elif action == "saving_rate":
            data = DashboardService.get_saving_rate(
                user=user,
                year=year,
                month=month
            )
        
        elif action == "largest_category":
            data = DashboardService.get_largest_category(
                user=user,
                year=year,
                month=month
            )
        
        elif action == "budget_status":
            data = BudgetService.get_budget_data(
                user=user,
                category=category,
                year=year,
                month=month
            )
        
        elif action == "remaining_budget":
            data = BudgetService.remaining_budget(
                user=user,
                category=category,
                year=year,
                month=month
            )
        
        else:
            raise ValueError(
                f"Unsupported action: {action}"
            ) 
            
        prompt_text = chat_prompt.format(
                question=question,
                financial_data=data
            )
        response = OllamaClient.generate(
            prompt=prompt_text
        )

        return response
