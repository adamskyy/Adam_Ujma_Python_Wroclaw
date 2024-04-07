from src.csv_handler import CSVHandler
from src.debt_simplifier import DebtSimplifier
import argparse
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)


# Define main function
def main():
    # Add argparse with two arguments: input_file_path and output_file_path
    parser = argparse.ArgumentParser(
        description="Project to minimize number of transactions across a group of people to settle debts."
    )
    parser.add_argument("input_file_path", type=str, help="Path to the input CSV file.")
    parser.add_argument(
        "output_file_path", type=str, help="Path to the output CSV file."
    )
    args = parser.parse_args()

    # Read transactions from input CSV file
    transactions = CSVHandler.read_transactions_from_csv(args.input_file_path)

    # Minimize cash flow
    optimized_transactions = DebtSimplifier.minimize_cash_flow(transactions)

    # Write optimized transactions to output CSV file
    CSVHandler.write_transactions_to_csv(optimized_transactions, args.output_file_path)


if __name__ == "__main__":
    main()
