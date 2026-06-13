from sklearn.linear_model import LinearRegression

class MLPredictor:

    @staticmethod
    def get_income_forecast(incomes, x):

        if len(incomes) < 2:
            return None
        
        X = [[i] for i in range(len(incomes))]
        y = [income["income"] for income in incomes]
        
        reg = LinearRegression()
        reg.fit(X, y)

        predicted_amount = reg.predict([[x]])
        return float(predicted_amount[0])


    @staticmethod
    def get_expense_forecats(expenses, x):

        if len(expenses) < 2:
            return None

        X = [[i] for i in range(len(expenses))]
        y = [expense["expense"] for expense in expenses]
        
        reg = LinearRegression()
        reg.fit(X, y)

        predicted_amount = reg.predict([[x]])
        return float(predicted_amount[0])


    @staticmethod
    def get_saving_rate_forecast(saving_rates, x):

        if len(saving_rates) < 2:
            return None

        X = [[i] for i in range(len(saving_rates))]
        y = [saving_rate["saving_rate"] for saving_rate in saving_rates]
        
        reg = LinearRegression()
        reg.fit(X, y)

        predicted_amount = reg.predict([[x]])
        return float(predicted_amount[0])