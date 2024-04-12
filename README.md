# Greystone Backend Challenge

## Description

REST API developed with FastAPI for a Loan Amortization app, designed to manage users and their loans.

## Installation

1. Clone the repository:

- `git clone https://github.com/hr7n/fastapi-backend`
- `cd fastapi-backend`

2. Install the required dependencies:

- `pip install -r requirements.txt`

3. Run the application:

- `uvicorn main:app`

## Dependencies

This project uses the following major dependencies:

- **FastAPI**: For creating the REST API.
- **SQLModel**: For ORM operations with SQLite database.
- **SQLite**: Used as the database engine, compatible with version 3.39.5 or higher.
- **Uvicorn**: As the ASGI server to run FastAPI.
- **Pytest**: For running tests.

## Usage

Core endpoints:

- `POST /users/: Create a new user.`
- `POST /loans/: Create a new loan.`
- `GET /loans/{loan_id}/schedule: Fetch the amortization schedule for a specific loan.`
- `GET /loans/{loan_id}/summary/{month}: Get a summary of a loan for a specific month.`
- `GET /users/{user_id}/loans: List all loans associated with a user.`
- `POST /loans/{loan_id}/share/{user_id}: Share a loan with another user.`

Additional endpoints:

- `GET /users/{user_id}: Returns user information.`
- `PUT /users/{user_id}: Update user information.`
- `DELETE /users/{user_id}: Delete a user from the database.`
- `GET /loans/{loan_id}: Returns information about a loan.`
- `GET /loans/{loan_id}/users: List all users associated with a loan.`

## Tests

To run the tests, execute:
`pytest`

- `test_calculate_monthly_payment:`
  - This test verifies the calculate_monthly_payment function. It uses predefined test cases that include loan amounts, annual interest rates, loan terms (in months), and the expected monthly payment.
- `test_loan_schedule:`
  - This test checks the loan_schedule function, ensuring it correctly generates a complete amortization schedule for a given loan. It validates that the schedule's length matches the loan term, the first month's details are accurate, and the loan is fully paid off by the last month. The test also confirms that the monthly payment and remaining balance calculations align with expectations derived from the numpy_financial.pmt function.
- `test_loan_summary:`
  - This test evaluates the loan_summary function, ensuring it accurately calculates and returns a summary of the loan's status at a specified month. It tests against predefined scenarios that include the loan amount, annual interest rate, loan term in months, and a specific month for which the summary is requested. The expected outcomes for the current principal balance, total principal paid, and total interest paid are compared against the function's output. This test confirms that the function provides precise financial information crucial for monitoring loan repayment progress.

## Questions

If you have any questions, reach out to me at michaelhorton722@gmail.com.
