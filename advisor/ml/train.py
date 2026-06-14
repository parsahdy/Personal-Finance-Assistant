from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class MLPredictor:

    @staticmethod
    def get_income_forecast(incomes, future_x):

        if len(incomes) < 2:
            return None
        
        X = [[i] for i in range(len(incomes))]
        y = [income["income"] for income in incomes]

        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        
        reg = LinearRegression()
        reg.fit(X_poly, y)

        predicted_amount = reg.predict([[future_x]])
        return float(predicted_amount[0])


    @staticmethod
    def get_expense_forecat(expenses, future_x):

        if len(expenses) < 2:
            return None

        X = [[i] for i in range(len(expenses))]
        y = [expense["expense"] for expense in expenses]
        
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        
        reg = LinearRegression()
        reg.fit(X_poly, y)

        predicted_amount = reg.predict([[future_x]])
        return float(predicted_amount[0])


    @staticmethod
    def get_saving_rate_forecast(saving_rates, future_x):

        if len(saving_rates) < 2:
            return None

        X = [[i] for i in range(len(saving_rates))]
        y = [saving_rate["saving_rate"] for saving_rate in saving_rates]
        
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        
        reg = LinearRegression()
        reg.fit(X_poly, y)

        predicted_amount = reg.predict([[future_x]])
        return float(predicted_amount[0])