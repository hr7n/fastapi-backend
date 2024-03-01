import numpy_financial as npf


def calculate_monthly_payment(
    amount: float, annual_interest_rate: float, loan_term_months: int
) -> float:
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    monthly_pmt = -npf.pmt(monthly_interest_rate, loan_term_months, amount)
    return monthly_pmt


def loan_schedule(amount: float, annual_interest_rate: float, loan_term_months: int):
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    monthly_pmt = -npf.pmt(monthly_interest_rate, loan_term_months, amount)
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
            {
                "month": month,
                "remaining_balance": remaining_balance,
                "monthly_payment": monthly_pmt,
            }
        )

        if remaining_balance <= 0:
            break
    return schedule


amount = 100000
annual_interest_rate = 5
loan_term_months = 360

schedule = loan_schedule(amount, annual_interest_rate, loan_term_months)
for payment_info in schedule[:12]:
    print(payment_info)
