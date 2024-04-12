# import numpy_financial as npf
from models import LoanSchedule, LoanSummary


def calculate_monthly_payment(
    amount: float, annual_interest_rate: float, loan_term_months: int
) -> float:
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    # monthly_pmt = -npf.pmt(monthly_interest_rate, loan_term_months, amount)
    monthly_payment = amount  * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
    return monthly_payment


def loan_schedule(
    amount: float, annual_interest_rate: float, loan_term_months: int
) -> list:
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    # monthly_pmt = -npf.pmt(monthly_interest_rate, loan_term_months, amount)
    monthly_pmt = calculate_monthly_payment(amount, annual_interest_rate, loan_term_months)
    remaining_balance = amount
    schedule = []

    for month in range(1, loan_term_months + 1):
        interest_pmt = remaining_balance * monthly_interest_rate
        principal_pmt = monthly_pmt - interest_pmt
        remaining_balance -= principal_pmt

        if remaining_balance < 0:
            principal_pmt += remaining_balance
            remaining_balance = 0.0

        schedule.append(
            LoanSchedule(
                month=month,
                remaining_balance=remaining_balance,
                monthly_payment=monthly_pmt,
            )

        )

        if remaining_balance <= 0:
            break

    return schedule


def loan_summary(
    amount: float, annual_interest_rate: float, loan_term_months: int, month: int
) -> LoanSummary:
    if month < 1 or month > loan_term_months:
        raise ValueError("Invalid month number")

    monthly_interest_rate = (annual_interest_rate / 100) / 12
    monthly_pmt = calculate_monthly_payment(amount, annual_interest_rate, loan_term_months)
    total_interest_paid = 0.0
    total_principal_paid = 0.0
    remaining_balance = amount

    for m in range(1, month + 1):
        interest_pmt = remaining_balance * monthly_interest_rate
        principal_pmt = monthly_pmt - interest_pmt
        remaining_balance -= principal_pmt

        total_principal_paid += principal_pmt
        total_interest_paid += interest_pmt

        if remaining_balance <= 0:
            break

    current_principal_balance = max(remaining_balance, 0.0)


    return LoanSummary(
        current_principal_balance=current_principal_balance,
        total_principal_paid=total_principal_paid,
        total_interest_paid=total_interest_paid,
    )
