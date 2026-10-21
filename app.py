import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the trained model
with open('loan.pkl', 'rb') as f:
  model = pickle.load(f)

# HTML Template with modern, attractive styling using Tailwind CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan Eligibility Prediction Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900 min-h-screen text-slate-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl w-full bg-slate-800/80 backdrop-blur-md rounded-2xl shadow-2xl border border-slate-700 overflow-hidden p-8">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
                Loan Eligibility Predictor
            </h2>
            <p class="mt-2 text-sm text-slate-400">
                Fill in the applicant details below to instantly check loan approval status.
            </p>
        </div>

        {% if prediction_text %}
        <div class="mb-6 p-4 rounded-xl text-center font-semibold text-lg shadow-lg transition-all duration-300 {% if 'Approved' in prediction_text %} bg-emerald-900/60 border border-emerald-500 text-emerald-300 {% else %} bg-rose-900/60 border border-rose-500 text-rose-300 {% endif %}">
            {{ prediction_text }}
        </div>
        {% endif %}

        <form action="/predict" method="POST" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Gender -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Gender</label>
                <select name="Gender" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="1">Male</option>
                    <option value="0">Female</option>
                </select>
            </div>

            <!-- Married -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Married</label>
                <select name="Married" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                </select>
            </div>

            <!-- Dependents -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Dependents</label>
                <select name="Dependents" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3+</option>
                </select>
            </div>

            <!-- Education -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Education</label>
                <select name="Education" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="1">Graduate</option>
                    <option value="0">Not Graduate</option>
                </select>
            </div>

            <!-- Self Employed -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Self Employed</label>
                <select name="Self_Employed" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                </select>
            </div>

            <!-- Applicant Income -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Applicant Income ($)</label>
                <input type="number" name="ApplicantIncome" placeholder="e.g. 5000" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
            </div>

            <!-- Coapplicant Income -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Coapplicant Income ($)</label>
                <input type="number" name="CoapplicantIncome" placeholder="e.g. 1500" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
            </div>

            <!-- Loan Amount -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Loan Amount (in thousands)</label>
                <input type="number" name="LoanAmount" placeholder="e.g. 120" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
            </div>

            <!-- Loan Amount Term -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Loan Amount Term (Months)</label>
                <input type="number" name="Loan_Amount_Term" placeholder="e.g. 360" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
            </div>

            <!-- Credit History -->
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Credit History</label>
                <select name="Credit_History" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="1">1.0 (Good / Cleared Debts)</option>
                    <option value="0">0.0 (Bad / Outstanding)</option>
                </select>
            </div>

            <!-- Property Area -->
            <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-300 mb-1">Property Area</label>
                <select name="Property_Area" required class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                    <option value="2">Urban</option>
                    <option value="1">Semiurban</option>
                    <option value="0">Rural</option>
                </select>
            </div>

            <!-- Submit Button -->
            <div class="md:col-span-2 mt-4">
                <button type="submit" class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-emerald-400">
                    Predict Loan Eligibility
                </button>
            </div>
        </form>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
  return render_template_string(HTML_TEMPLATE)


@app.route('/predict', methods=['POST'])
def predict():
  try:
    # Collecting form inputs in exact feature order expected by model:
    # ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
    #  'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
    #  'Loan_Amount_Term', 'Credit_History', 'Property_Area']
    features = [
        float(request.form['Gender']),
        float(request.form['Married']),
        float(request.form['Dependents']),
        float(request.form['Education']),
        float(request.form['Self_Employed']),
        float(request.form['ApplicantIncome']),
        float(request.form['CoapplicantIncome']),
        float(request.form['LoanAmount']),
        float(request.form['Loan_Amount_Term']),
        float(request.form['Credit_History']),
        float(request.form['Property_Area']),
    ]

    final_features = np.array([features])
    prediction = model.predict(final_features)

    # Interpreting prediction output (1/Y for Approved, 0/N for Rejected)
    if prediction[0] == 1 or prediction[0] == 'Y':
      result_text = (
          'Congratulations! Your Loan Application is Approved 🎉'
      )
    else:
      result_text = 'Sorry, Your Loan Application is Rejected ❌'

    return render_template_string(
        HTML_TEMPLATE, prediction_text=result_text
    )

  except Exception as e:
    error_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-slate-900 min-h-screen flex items-center justify-center p-4">
            <div class="bg-rose-950 border border-rose-500 text-rose-200 p-8 rounded-2xl text-center max-w-md shadow-2xl">
                <h3 class="text-2xl font-bold mb-2">Prediction Error</h3>
                <p class="text-sm text-rose-300 mb-6">{str(e)}</p>
                <a href="/" class="bg-white text-slate-900 font-semibold px-6 py-2.5 rounded-lg shadow hover:bg-slate-100 transition">Go Back</a>
            </div>
        </body>
        </html>
        """
    return render_template_string(error_template)


if __name__ == '__main__':
  app.run(debug=True)
