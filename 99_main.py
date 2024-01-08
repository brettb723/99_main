import streamlit as st
import pandas as pd

# Page Configuration with Custom CSS for Enhanced Styling
st.set_page_config(page_title="99 Main Street Redevelopment Underwriting", 
                   page_icon="🏗️", 
                   layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .big-font {
        font-size:18px !important;
    }
    .bold-font {
        font-weight: bold;
    }
    .highlight {
        background-color: lightyellow;
    }
    .metric-label {
        color: darkblue;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: darkslategray;
        margin-bottom: 0px;
    }
    .sub-section-header {
        font-size: 20px;
        font-weight: bold;
        color: darkslateblue;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Introduction with Enhanced Formatting
st.title("🏗️ 99 Main Street Redevelopment Underwriting Tool")
st.markdown("""
    <span class="big-font">Welcome to the interactive financial underwriting tool for the redevelopment of 
    <span class="bold-font">99 Main Street, Waterville, Maine</span>. This application is designed to help 
    investors, stakeholders, and developers analyze the financial viability of converting this property into luxury 
    apartments with commercial space on the ground floor.</span>
    """, unsafe_allow_html=True)

st.markdown("""
    <span class="big-font">Provide the required information to generate a comprehensive financial analysis, including cost estimations, 
    revenue projections, and ROI calculations.</span>
    """, unsafe_allow_html=True)

st.write("---")

# Sidebar: Quick Project Overview
st.sidebar.header("📌 Project Overview")
st.sidebar.markdown("""
    - **Location**: 99 Main Street, Waterville, Maine
    - **Project**: Conversion into 6 luxury apartments and commercial space
    - **Floors**: Upper three floors for apartments; ground floor for commercial use
    - **Goal**: Evaluate financial feasibility and expected returns
""")

# Main Content
# Project Details Section
st.markdown('<div class="section-header">Project Details</div>', unsafe_allow_html=True)
st.markdown('<div class="big-font">Enter and review key information about the property, purchase price, and renovation estimates.</div>', unsafe_allow_html=True)

# Purchase Price and Building Size Inputs
purchase_price = st.number_input("Purchase Price of the Property ($)", min_value=0.0, value=430000.0, format="%.2f")
building_size = st.number_input("Total Building Size (sq ft)", min_value=0.0, value=13000.0, format="%.2f")
renovation_cost_per_sqft = st.number_input("Renovation Cost per Square Foot ($)", min_value=0.0, value=100.0, format="%.2f")

# Calculating Total Renovation Cost
total_renovation_cost = building_size * renovation_cost_per_sqft

# Total Project Cost
total_project_cost = purchase_price + total_renovation_cost
st.metric(label="Total Project Cost", value=f"${total_project_cost:,.2f}")
# Equity and Debt Amounts
equity_percentage = st.slider("Equity Portion (%)", min_value=0.0, max_value=100.0, value=25.0)
equity_amount = (equity_percentage / 100) * total_project_cost
debt_amount = total_project_cost - equity_amount
st.metric(label="Equity Amount", value=f"${equity_amount:,.2f}")
st.metric(label="Debt Amount", value=f"${debt_amount:,.2f}")

st.write("---")

# Pro-forma Analysis Section
st.markdown('<div class="section-header">Pro-forma Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="big-font">Analyze the projected revenues, operating expenses, cash flows, and investment returns.</div>', unsafe_allow_html=True)


# Revenue Projections
st.markdown('<div class="sub-section-header">Revenue Projections</div>', unsafe_allow_html=True)
total_monthly_rent = 0
for unit in range(1, 8):
    rent = st.number_input(f"Rent for Unit {unit} (Monthly $)", min_value=0.0, value=2500.0, format="%.2f", key=f"rent_{unit}")
    total_monthly_rent += rent
annual_rent_income = total_monthly_rent * 12

st.metric(label="Annual Revenue from All Units", value=f"${annual_rent_income:,.2f}")

# ...

# Operating Expenses
st.markdown('<div class="sub-section-header">Operating Expenses</div>', unsafe_allow_html=True)

# Input for Rates
tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, value=1.25, format="%.2f")
maintenance_rate = st.number_input("Maintenance Rate (%)", min_value=0.0, value=7.0, format="%.2f")
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=6.5, format="%.2f")
vacancy_rate = st.number_input("Vacancy Rate (%)", min_value=0.0, value=7.0, format="%.2f")

# Calculating Dollar Amounts Based on Rates
annual_taxes = (tax_rate / 100) * total_project_cost
annual_maintenance_cost = (maintenance_rate / 100) * annual_rent_income
annual_interest_expense = (interest_rate / 100) * debt_amount
vacancy_expense = (vacancy_rate / 100) * annual_rent_income

# Other Operating Expenses Inputs
insurance_cost = st.number_input("Annual Insurance Cost ($)", min_value=0.0, value=5000.0, format="%.2f")
water_sewer_cost = st.number_input("Annual Water & Sewer Cost ($)", min_value=0.0, value=3000.0, format="%.2f")
electricity_cost = st.number_input("Annual Electricity Cost ($)", min_value=0.0, value=2000.0, format="%.2f")
management_cost = (6.0 / 100) * annual_rent_income  # 6% Management Fee

# Displaying Operating Expenses in a Table Format
st.markdown("#### Operating Expenses Summary")
expenses_data = {
    "Expense": ["Annual Taxes", "Maintenance", "Vacancy", "Insurance", "Water & Sewer", "Electricity", "Management"],
    "Amount": [annual_taxes, annual_maintenance_cost, vacancy_expense, insurance_cost, water_sewer_cost, electricity_cost, management_cost]
}
df_expenses = pd.DataFrame(expenses_data)
df_expenses['Running Total'] = df_expenses['Amount'].cumsum()

# Formatting the values as currency
df_expenses['Amount'] = df_expenses['Amount'].apply(lambda x: f"${x:,.2f}")
df_expenses['Running Total'] = df_expenses['Running Total'].apply(lambda x: f"${x:,.2f}")


st.table(df_expenses.assign(hack='').set_index('hack'))  # Trick to hide index

# Total Expenses Calculation
total_expenses = df_expenses['Amount'].str.replace('$', '').str.replace(',', '').astype(float).sum()
st.metric(label="Total Annual Operating Expenses", value=f"${total_expenses:,.2f}")


# Capitalization Rate (Cap Rate)
net_operating_income = annual_rent_income - total_expenses
cap_rate = (net_operating_income / total_project_cost) * 100
st.metric(label="Total Project Cost", value=f"${total_project_cost:,.2f}")
st.metric(label="Net Operating Income (NOI)", value=f"${net_operating_income:,.2f}")
st.metric(label="Capitalization Rate (Cap Rate)", value=f"{cap_rate:.2f}%")
# Free Cash Flow (FCF)
free_cash_flow = net_operating_income - annual_interest_expense
st.metric(label="Free Cash Flow (FCF)", value=f"${free_cash_flow:,.2f}")

# Footer
st.write("---")
st.markdown("""
    <span class="bold-font">Developed for the 99 Main Street Redevelopment Project. © Standard Properties </span>
    """, unsafe_allow_html=True)
