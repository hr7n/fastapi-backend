from loan_calc import calculate_monthly_payment, loan_schedule, loan_summary
from pytest import approx


def test_calculate_monthly_payment():
    test_cases = [(100000, 5, 360, 536.82), (50000, 3, 120, 483.32)]

    for amount, annual_interest_rate, loan_term_months, expected in test_cases:
        calculated = calculate_monthly_payment(
            amount, annual_interest_rate, loan_term_months
        )
        assert calculated == approx(expected, abs=0.6)


def test_loan_schedule():
    amount = 10000
    annual_interest_rate = 5
    loan_term_months = 360

    monthly_interest_rate = (annual_interest_rate / 100) / 12
    expected_monthly_pmt = amount  * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
    schedule = loan_schedule(amount, annual_interest_rate, loan_term_months)

    assert (
        len(schedule) == loan_term_months
    ), "Loan term does not match length of schedule."

    first_month = schedule[0]

    assert first_month.month == 1, "First month should be 1"
    assert (
        first_month.monthly_payment == expected_monthly_pmt
    ), "Monthly payment different than expected"
    assert (
        first_month.remaining_balance < amount
    ), "Remaining balance should be less than principal"

    last_month = schedule[-1]
    assert (
        last_month.remaining_balance == 0.0
    ), "Loan should be fully paid off by last month"

def test_loan_summary():
    test_cases = [
        {
            'amount': 100000,
            'annual_interest_rate': 5,
            'loan_term_months': 12,
            'month': 6,
            'expected': {
                'current_principal_balance': 50623.66,
                'total_principal_paid': 49376.33,
                'total_interest_paid': 1988.15,
            }

        },
    ]

    for case in test_cases:
        summary = loan_summary(
            amount=case["amount"],
            annual_interest_rate=case["annual_interest_rate"],
            loan_term_months=case["loan_term_months"],
            month=case["month"],
        )

        assert summary.current_principal_balance == approx(case["expected"]["current_principal_balance"], abs=0.01), 'Current principal balance does not match expected'
        assert summary.total_principal_paid == approx(case["expected"]["total_principal_paid"], abs=0.01), 'Total principal balance does not match expected'
        assert summary.total_interest_paid == approx(case["expected"]["total_interest_paid"], abs=0.01), 'Total interest paid does not match expected'