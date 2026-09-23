import pandas as pd
import pandera.pandas as pa

from src.schema import customer_schema

def format_error_report(error_report: pd.DataFrame) -> pd.DataFrame:
    """
    Make Pandera validation errors more readable
    """
    formatted_report = error_report.copy()

    formatted_report["column"] = formatted_report["column"].fillna("schema")
    formatted_report["index"] = formatted_report["index"].fillna("-")

    def create_message(row: pd.Series) -> str:
        # Create readable error messages based on the check and failure_case
        column = row["column"]
        check = str(row["check"])
        failure_case = row["failure_case"]

        if check == "field_uniqueness":
            return "Value must be unique"

        if "in_range" in check and column == "age":
            return "Age must be between 18 and 100"

        if "in_range" in check and column == "annual_income":
            return "Annual income must be between 0 and 300,000"

        if "isin" in check and column == "segment":
            return "Segment must be one of: consumer, business, enterprise"

        if "isin" in check and column == "country":
            return "Country is not allowed. Must be one of: Sweden, Norway, Denmark, Finland"

        if check == "not_nullable":
            return "Missing value is not allowed"

        if "dtype" in check:
            return "incorrect data type"

        if "str_matches" in check:
            return "Date must be in the format YYYY-MM-DD"

        if check == "contains_valid_dates":
            return "Date must be a valid date"

        if check == "column_in_dataframe":
            return f"Required column is missing: {failure_case}"

        if check == "column_in_:schema":
            return f"Unexpected column found: {failure_case}"

        return "Validation failed"

    formatted_report["message"] = formatted_report.apply(create_message, axis=1)

    return formatted_report[["column", "check", "failure_case", "index", "message"]]


def validate_customer_data(data: pd.DataFrame, ) -> tuple[bool, pd.DataFrame]:
    """
    Validate the customer data against the Pandera schema.

    Returns:
        tuple[bool, pd.DataFrame]:
        True and the validated DataFrame if validation is successful
        False and a Dataframe containing validation errors if validation fails.
    """
    try:
        validated_data = customer_schema.validate(data, lazy=True)

        return True, validated_data

    except pa.errors.SchemaErrors as error:
        error_report = error.failure_cases[
            ["column", "check", "failure_case", "index"]
        ]
        formatted_report = format_error_report(error_report)
        
        return False, formatted_report