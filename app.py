from flask import Flask, render_template,request
import joblib
import math
import numpy as np
import pandas as pd







app = Flask(__name__)


model = joblib.load('model_log.pkl')










@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
   
  # Retrieve the form data
    gender_input = request.form['gender']
    # Map 'M' to 1 and 'F' to 0
    gender = 1.0 if gender_input == 'M' else 0.0


    married = float(request.form['married'])

    
    





    dependents = float(request.form['dependents'])




    education = float(request.form['education'])


    self_employed = float(request.form['self_employed'])


    applicant_income = float(request.form['applicant_income'])


    coapplicant_income = float(request.form['coapplicant_income'])


    loan_amount = float(request.form['loan_amount'])/10


    loan_amount_term = float(request.form['loan_amount_term'])


    credit_history = float(request.form['credit_history'])


    property_area = float(request.form['property_area'])

    # Perform calculations on input data
    applicant_income = math.sqrt(applicant_income)
    coapplicant_income = math.sqrt(coapplicant_income)
    loan_amount = math.sqrt(loan_amount)
    loan_amount_term = math.sqrt(loan_amount_term)

    # Create a DataFrame with the input data
    input_data = np.array([gender, married, dependents, education, self_employed, applicant_income,
                           coapplicant_income, loan_amount, loan_amount_term, credit_history, property_area])
    df = pd.DataFrame([input_data], columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                                             'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                                             'Loan_Amount_Term', 'Credit_History', 'Property_Area'])

    # Make predictions using the loaded model
    predictions = model.predict(df)

   

    #approval_status = "Loan Application Rejected" if predictions[0] == 0 else "Loan Application Approved"

    # Render the result template with the approval status
    #return render_template('result.html', prediction_result=approval_status)
    
    # ...
    if predictions[0] == 1:
        prediction_result_class = "approved"
        prediction_result_message = "Congratulations! Your loan application has been approved."
    else:
        prediction_result_class = "rejected"
        prediction_result_message = "We regret to inform you that your loan application has been rejected."

    # Render the result template with the appropriate class and message
    return render_template('result.html', prediction_result_class=prediction_result_class, prediction_result_message=prediction_result_message)
# ...

    

if __name__ == '__main__':
    app.run()
