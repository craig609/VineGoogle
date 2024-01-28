from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years):
    # Your existing calculation logic
    monthly_interest_rate = annual_interest_rate / 12 / 100
    total_payments = loan_term_years * 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -total_payments)
    return monthly_payment

def remaining_balance(loan_amount, annual_interest_rate, loan_term_years, months_paid):
    # Your existing calculation logic
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    remaining_balance = loan_amount * ((1 + annual_interest_rate / 12 / 100) ** months_paid) - (monthly_payment / (annual_interest_rate / 12 / 100)) * ((1 + annual_interest_rate / 12 / 100) ** months_paid - 1)
    return remaining_balance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        loan_amount = float(request.form['loan_amount'])
        annual_interest_rate = float(request.form['annual_interest_rate'])
        loan_term_years = int(request.form['loan_term_years'])
        months_paid = int(request.form['months_paid'])

        remaining_balances = []
        for month in range(months_paid + 1, loan_term_years * 12 + 1):
            remaining_balance_month = remaining_balance(loan_amount, annual_interest_rate, loan_term_years, month)
            remaining_balances.append(f'Month {month}: Remaining Balance = ${remaining_balance_month:.2f}')

        return render_template('result.html', remaining_balances=remaining_balances)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
