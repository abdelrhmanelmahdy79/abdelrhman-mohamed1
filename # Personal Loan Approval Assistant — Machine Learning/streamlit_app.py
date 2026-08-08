

import pickle
import pandas as pd
import streamlit as st


with open('risk_model.pkl', 'rb') as f:
    risk_model = pickle.load(f)

with open('approval_model.pkl', 'rb') as f:
    approval_model = pickle.load(f)


st.title(" Personal Loan Approval Assistant")
st.write("Fill in your details below and click the button to check your loan status.")


age = st.number_input("Age", min_value=18, max_value=100, value=30)

monthly_income = st.number_input("Monthly Income (EGP)", min_value=0, value=15000)

employment_status = st.selectbox(
    "Employment Status",
    ["Employed", "Self-Employed", "Unemployed"]
)

years_employed = st.number_input("Years at current job", min_value=0, value=3)

credit_history_years = st.number_input("Credit history (years)", min_value=0, value=5)

existing_loans = st.number_input("Number of existing loans", min_value=0, value=1)

late_payments = st.number_input("Late payments last year", min_value=0, value=0)

defaulted_before = st.radio("Have you ever defaulted on a loan?", ["No", "Yes"])

requested_amount = st.number_input("Requested loan amount (EGP)", min_value=1000, value=40000)

monthly_debt = st.number_input("Current monthly debt payments (EGP)", min_value=0, value=1500)


if st.button("Check My Loan Application"):

    
    debt_to_income = monthly_debt / monthly_income if monthly_income > 0 else 0
    loan_to_income = requested_amount / (monthly_income * 12) if monthly_income > 0 else 0

    
    credit_score = (
        650
        + credit_history_years * 5
        - late_payments * 20
        - (100 if defaulted_before == "Yes" else 0)
        - existing_loans * 10
        - debt_to_income * 120
        - loan_to_income * 60
    )
    credit_score = max(300, min(850, credit_score))  # keep between 300-850

   
    employment_employed = 1 if employment_status == "Employed" else 0
    employment_self_employed = 1 if employment_status == "Self-Employed" else 0
    employment_unemployed = 1 if employment_status == "Unemployed" else 0

    applicant = pd.DataFrame([{
        'age': age,
        'monthly_income': monthly_income,
        'years_employed': years_employed,
        'credit_history_years': credit_history_years,
        'existing_loans': existing_loans,
        'late_payments': late_payments,
        'defaulted_before': 1 if defaulted_before == "Yes" else 0,
        'requested_amount': requested_amount,
        'monthly_debt': monthly_debt,
        'credit_score': credit_score,
        'debt_to_income': debt_to_income,
        'loan_to_income': loan_to_income,
        'employment_status_Employed': employment_employed,
        'employment_status_Self-Employed': employment_self_employed,
        'employment_status_Unemployed': employment_unemployed,
    }])

    predicted_risk = risk_model.predict(applicant)[0]
    predicted_approval = approval_model.predict(applicant)[0]

   
    st.subheader("Result")
    st.write(f"**Estimated Credit Score:** {credit_score}")
    st.write(f"**Risk Level:** {predicted_risk}")

    if predicted_approval == 1:
        st.success(" Congratulations! Your loan is APPROVED.")
    else:
        st.error(" Sorry, your loan application was NOT approved.")
