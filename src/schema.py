import pandera.pandas as pa
from pandera import Check
import pandas as pd

def contains_valid_dates(series: pd.Series) -> bool:
    # Check that all values can be interpreted as valid dates in the format YYYY-MM-DD (even if they are impossible dates like 2023-02-30)
    parsed_dates = pd.to_datetime(
        series, 
        format="%Y-%m-%d", 
        errors="coerce",
    )

    return bool(parsed_dates.notna().all())


# Define the rules that the customer dataset must follow using Pandera
customer_schema = pa.DataFrameSchema(
    {
        "customer_id": pa.Column(
            int,
            checks=Check.greater_than(0),
            nullable=False,
            unique=True,
        ),
        "age": pa.Column(
            int,
            checks=Check.in_range(18, 100),
            nullable=False,
        ),
        "annual_income": pa.Column(
            int,
            checks=Check.in_range(0, 300_000),
            nullable=False,
        ),
        "segment": pa.Column(
            str,
            checks=Check.isin(["consumer", "business", "enterprise"]),
            nullable=False,
        ),
        "country": pa.Column(
            str,
            checks=Check.isin(["Sweden", "Norway", "Denmark", "Finland"]),
            nullable=False,
        ),
        "active": pa.Column(
            bool,
            nullable=False,
        ),
        "signup_date": pa.Column(
            str,
            checks=[Check.str_matches(r"^\d{4}-\d{2}-\d{2}$"), Check(contains_valid_dates)],
            nullable=False,
        ),
    },
    # Reject columns that are not part of the schema
    strict=True,
)