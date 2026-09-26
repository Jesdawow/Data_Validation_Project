# Customer Data Validation with Pandera

This project demonstrates how Pandera can be used to validate customer data before it's used for analysis or other workflows.

The example data is based on a fictional Nordic service company that receives customer data as a CSV file. All datasets are synthetic and were created specifically for this project.

## What the project does

The program reads a customer CSV file and validates it against a Pandera schema.

The validation checks include:

- required columns and data types
- missing values
- duplicate customer IDs
- numerical ranges
- allowed categories
- valid date formats and calendar dates
- unexpected columns

If the data is invalid, the program prints a readable error report in the terminal. Validation runs are also recorded in `logs/validation.log`.

The project also includes automated tests using pytest.

## Project Structure

```text
├── data/
│   ├── valid_customers.csv
│   └── invalid_customers.csv
├── logs/ # Generated upon running main.py
│   └── validation.log # Generated upon running main.py
├── report/
│   ├── images/
│   │   ├── invalid_output.png
│   │   ├── pytest_output.png
│   │   ├── valid_output.png
│   └── report.md
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── schema.py
│   └── validator.py
├── tests/
│   └── test_validation.py
├── main.py
├── pytest.ini
├── README.md
└── requirements.txt
```

## Installation

Python 3.13.7 was used for this project.

```powershell
git clone https://github.com/Jesdawow/Data_Validation_Project.git
cd data_validation_project
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running the project

Select the CSV file to validate in main.py:
```bash
file_path = Path("data/valid_customers.csv")
```
or to demonstrate validation errors use:
```bash
file_path = Path("data/invalid_customers.csv")
```

Then run:
```bash
python main.py
```

To run the tests:
```bash
pytest -v
```

The project currently contains 10 automated tests.

## Data

The CSV files contains synthetic data with the following columns:
- customer_id - unique customer ID.
- age - customer age, expected to be between 18 and 100.
- annual_income - customer annual income, expected to be between 0 and 300,000
- segment - customer segment: consumer, business or enterprise.
- country - customer country: Sweden, Norway, Denmark or Finland.
- active - whether the customer is currently active.
- signup_date - date when the customer was registered.

The data does not represent real customers or a real company.

## Dependencies

Main external packages:

- pandas
- Pandera
- pytest

Exact versions are listed in `requirements.txt`
