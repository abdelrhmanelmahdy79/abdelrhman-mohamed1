

import pickle
import pandas as pd
import flet as ft


with open('risk_model.pkl', 'rb') as f:
    risk_model = pickle.load(f)

with open('approval_model.pkl', 'rb') as f:
    approval_model = pickle.load(f)


def main(page: ft.Page):
    page.title = "Loan Approval Assistant - Bank Agent"
    page.window.width = 500
    page.window.height = 750
    page.scroll = ft.ScrollMode.AUTO

   
    age = ft.TextField(label="Age", value="30")
    monthly_income = ft.TextField(label="Monthly Income (EGP)", value="15000")
    employment_status = ft.Dropdown(
        label="Employment Status",
        options=[
            ft.dropdown.Option("Employed"),
            ft.dropdown.Option("Self-Employed"),
            ft.dropdown.Option("Unemployed"),
        ],
        value="Employed"
    )
    years_employed = ft.TextField(label="Years employed", value="3")
    credit_history_years = ft.TextField(label="Credit history (years)", value="5")
    existing_loans = ft.TextField(label="Existing loans", value="1")
    late_payments = ft.TextField(label="Late payments last year", value="0")
    defaulted_before = ft.Checkbox(label="Defaulted before?", value=False)
    requested_amount = ft.TextField(label="Requested amount (EGP)", value="40000")
    monthly_debt = ft.TextField(label="Monthly debt payments (EGP)", value="1500")

  
    result_text = ft.Text(value="", size=18)


    def check_application(e):
        income = float(monthly_income.value)
        history_years = float(credit_history_years.value)
        late = float(late_payments.value)
        loans = float(existing_loans.value)
        debt = float(monthly_debt.value)
        requested = float(requested_amount.value)
        defaulted = 1 if defaulted_before.value else 0

        debt_to_income = debt / income if income > 0 else 0
        loan_to_income = requested / (income * 12) if income > 0 else 0

        credit_score = (
            650 + history_years * 5 - late * 20 - defaulted * 100 - loans * 10
            - debt_to_income * 120 - loan_to_income * 60
        )
        credit_score = max(300, min(850, credit_score))

        emp = employment_status.value
        employment_employed = 1 if emp == "Employed" else 0
        employment_self_employed = 1 if emp == "Self-Employed" else 0
        employment_unemployed = 1 if emp == "Unemployed" else 0

        applicant = pd.DataFrame([{
            'age': float(age.value),
            'monthly_income': income,
            'years_employed': float(years_employed.value),
            'credit_history_years': history_years,
            'existing_loans': loans,
            'late_payments': late,
            'defaulted_before': defaulted,
            'requested_amount': requested,
            'monthly_debt': debt,
            'credit_score': credit_score,
            'debt_to_income': debt_to_income,
            'loan_to_income': loan_to_income,
            'employment_status_Employed': employment_employed,
            'employment_status_Self-Employed': employment_self_employed,
            'employment_status_Unemployed': employment_unemployed,
        }])

        predicted_risk = risk_model.predict(applicant)[0]
        predicted_approval = approval_model.predict(applicant)[0]

        decision = "✅ APPROVED" if predicted_approval == 1 else "❌ NOT APPROVED"

        result_text.value = (
            f"Credit Score: {credit_score}\n"
            f"Risk Level: {predicted_risk}\n"
            f"Decision: {decision}"
        )
        page.update()

    
    page.add(
        ft.Text("Loan Approval Assistant - Bank Agent", size=22, weight=ft.FontWeight.BOLD),
        age,
        monthly_income,
        employment_status,
        years_employed,
        credit_history_years,
        existing_loans,
        late_payments,
        defaulted_before,
        requested_amount,
        monthly_debt,
        ft.ElevatedButton("Check Application", on_click=check_application),
        result_text,
    )


ft.app(target=main)
