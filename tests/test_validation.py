import pandas as pd
import pytest

from src.data_loader import load_csv
from src.validator import validate_customer_data

def test_load_valid_csv():
    # Check that a valid CSV file is loaded correctly as a DataFrame
    data = load_csv("data/valid_customers.csv")

    assert isinstance(data, pd.DataFrame)
    assert len(data) == 1500

def test_missing_csv_raises_error() -> None:
    # A missing CSV file should raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_csv("data/non_existent_file.csv")

def test_valid_customer_data_passes_validation():
    # Valid customer data should pass validation
    data = load_csv("data/valid_customers.csv")

    is_valid, result = validate_customer_data(data)

    assert is_valid is True
    assert isinstance(result, pd.DataFrame)

def test_invalid_customer_data_fails_validation() -> None:
    # Invalid customer data should fail validation
    data = load_csv("data/invalid_customers.csv")

    is_valid, result = validate_customer_data(data)

    assert is_valid is False
    assert isinstance(result, pd.DataFrame)

def test_invalid_data_contains_expected_error_columns() -> None:
    # The error report should contain the most important error details
    data = load_csv("data/invalid_customers.csv")

    is_valid, result = validate_customer_data(data)

    assert is_valid is False
    assert {"column", "check", "failure_case", "index"}.issubset(result.columns)

def test_invalid_signup_date_is_reported() -> None:
    # Invalid signup_date values should be reported in the error report
    data = load_csv("data/invalid_customers.csv")

    is_valid, result = validate_customer_data(data)

    assert is_valid is False
    assert "signup_date" in result["column"].values

def test_impossible_signup_date_Fails_validation() -> None:
    # A correctly formatted but impossible date should fail validation
    data = pd.DataFrame(
        {
            "customer_id": [1],
            "age": [30],
            "annual_income": [50000],
            "segment": ["consumer"],
            "country": ["Sweden"],
            "active": [True],
            "signup_date": ["2025-99-99"],  # Invalid date
        }
    )
    is_valid, result = validate_customer_data(data)

    assert is_valid is False
    assert "signup_date" in result["column"].values

def test_missing_required_column_fails_validation() -> None:
    # Removing a required column should make the dataset invalid
    data = load_csv("data/valid_customers.csv")
    data = data.drop(columns=["country"])  # Remove a required column

    is_valid, result = validate_customer_data(data)

    assert is_valid is False
    assert "country" in result["failure_case"].values

def test_unexpected_extra_column_fails_validation() -> None:
    # strict = True should reject any extra columns that are not part of the schema
    data = load_csv("data/valid_customers.csv")
    data["unexpected_column"] = "extra"  # Add an extra column

    is_valid, result = validate_customer_data(data)

    assert is_valid is False
    assert "unexpected_column" in result["failure_case"].values

def test_error_report_is_formatted() -> None:
    # The error report should be formatted to be more readable
    data = load_csv("data/valid_customers.csv")
    data = data.drop(columns=["country"])  # Remove a required column

    is_valid, result = validate_customer_data(data)

    assert is_valid is False
    assert "schema" in result["column"].values
    assert "-" in result["index"].values