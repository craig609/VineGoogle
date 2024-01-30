from flask import Flask, request, jsonify, make_response

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

@app.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Your existing POST request handling
    if request.method == 'POST':
        data = request.get_json()

        loan_amount = float(data['loan_amount'])
        annual_interest_rate = float(data['annual_interest_rate'])
        loan_term_years = int(data['loan_term_years'])
        months_paid = int(data['months_paid'])

        remaining_balances = []
        for month in range(months_paid + 1, loan_term_years * 12 + 1):
            remaining_balance_month = remaining_balance(loan_amount, annual_interest_rate, loan_term_years, month)
            remaining_balances.append({'month': month, 'remaining_balance': remaining_balance_month})

        response = jsonify({'remaining_balances': remaining_balances})

        # Set CORS headers
        response.headers['Access-Control-Allow-Origin'] = 'https://storage.googleapis.com'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
