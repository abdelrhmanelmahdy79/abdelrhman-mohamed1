# abdelrhman-mohamed1
Personal Loan Approval Assistant


An AI application that assesses credit risk and automates personal loan approval decisions based on an applicant's financial history.

Built for the AI for App & Web Development course - Final Project (Finance track).

 What it does

The system takes an applicant's financial information and predicts:

Estimated Credit Score (300-850)
Risk Level (Low / Medium / High)
Loan Decision (Approved / Not Approved)

Two machine learning models power the predictions:

Random Forest Classifier predicts the risk level
Decision Tree Classifier predicts the final approval decision

Both models are trained on a synthetic dataset of 2,000 applicants, using credit history, existing debt, past defaults, and the ratio of requested loan / monthly debt to income.

## Two apps, one model

| App | Who it's for | Built with |
|---|---|---|
| streamlit_app.py | Loan applicants (web) | Streamlit |
| flet_app.py | Bank agents (desktop) | Flet |

Both apps load the same trained models (risk_model.pkl, approval_model.pkl), so there is no duplicated logic between them.

## Project structure

```
Loan_Approval_ML.ipynb   notebook: data generation, feature engineering, model training
loan_applicants.csv      synthetic training dataset
risk_model.pkl           trained Random Forest model
approval_model.pkl       trained Decision Tree model
streamlit_app.py         web app for applicants
flet_app.py              desktop app for bank agents
```

## Setup

```
pip install pandas numpy scikit-learn streamlit flet
```

## Running the project

Web app (applicants):
```
py -m streamlit run streamlit_app.py
```

Desktop app (bank agents):
```
python flet_app.py
```

Retrain the models (optional):
Open Loan_Approval_ML.ipynb in Jupyter or VS Code and run all cells. This regenerates the dataset, retrains both models, and overwrites the .pkl files.

## Tech stack

Python, Pandas, NumPy, Scikit-Learn (Decision Tree / Random Forest), Streamlit, Flet

## Disclaimer

This tool produces an automated pre-decision for demonstration/educational purposes only and does not represent a real bank's final lending decision.
