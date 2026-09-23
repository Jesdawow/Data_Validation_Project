import logging
from pathlib import Path

from src.data_loader import load_csv 
from src.validator import validate_customer_data

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "validation.log"

def configure_logging() -> None:
    """
    Configure logging to store validation results in a log file and print them to the console.
    """
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def main() -> None:
    # Configure logging to store validation results in a log file and print them to the console
    configure_logging()

    file_path = Path("data/invalid_customers.csv")  # Change this to the path of your CSV file

    logging.info("Starting validation for file: %s", file_path)

    data = load_csv(file_path)
    is_valid, result = validate_customer_data(data)

    if is_valid:
        logging.info("Validation successful for file: %s", file_path)

        print("Validation successful. Data is valid!")
        print(f"Rows: {len(result)}")
        print(f"Columns: {len(result.columns)}")

    else:
        logging.error("Validation failed for file: %s", file_path)

        print("Validation failed. See the error report below!")
        print()
        display_columns = ["column","failure_case", "index", "message"]
        print(result[display_columns].to_string(index=False))

if __name__ == "__main__":
    main()