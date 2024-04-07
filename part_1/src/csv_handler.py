import csv
import io
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class CSVHandler:
    @staticmethod
    def read_transactions_from_csv(file_path: str) -> List[Tuple[str, str, int]]:
        """
        Reads transactions from a CSV file located at the given file path.
        Each transaction is expected to be in the format: creditor, debtor, amount
        where amount is a positive integer.
        Returns a list of transactions.
        """
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                return CSVHandler._read_transactions(file)
        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"Could not read file: {file_path}")
            raise e

    @staticmethod
    def read_transactions_from_content(file_content: str) -> List[Tuple[str, str, int]]:
        """
        Reads transactions from a string containing CSV formatted data.
        Each transaction is expected to be in the format: creditor, debtor, amount
        where amount is a positive integer.
        Returns a list of transactions in the format: debtor, creditor, amount.
        """
        file = io.StringIO(file_content)
        return CSVHandler._read_transactions(file)

    @staticmethod
    def _read_transactions(file: io.StringIO) -> List[Tuple[str, str, int]]:
        """
        Helper method to read transactions from a file-like object.
        Returns a list of transactions in the format: debtor, creditor, amount.
        Raises ValueError if the file contains invalid data.
        """
        transactions = []
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) != 3:
                logger.error(f"Invalid row: {row}")
                raise ValueError(f"Invalid row: {row}")
            debtor, creditor, amount = row
            if debtor == creditor:
                logger.error(
                    "Invalid transaction: debtor and creditor are same (debtor: {debtor}, creditor: {creditor})"
                )
                raise ValueError(
                    f"Invalid transaction: debtor and creditor are same (debtor: {debtor}, creditor: {creditor})"
                )
            if not amount.isdigit() or int(amount) <= 0:
                logger.error(f"Invalid amount: {amount}")
                raise ValueError(f"Invalid amount: {amount}")
            transactions.append((debtor, creditor, int(amount)))
        return transactions

    @staticmethod
    def write_transactions_to_csv(
        transactions: List[Tuple[str, str, int]], file_path: str
    ) -> None:
        """
        Method to write transactions to a CSV file located at the given file path.
        Raises FileNotFoundError or PermissionError if the file cannot be written.
        """
        try:
            with open(file_path, mode="w", encoding="utf-8", newline="") as file:
                CSVHandler._write_transactions(transactions, file)
        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"Could not write file: {file_path}")
            raise

    @staticmethod
    def write_transactions_to_content(transactions: List[Tuple[str, str, int]]) -> str:
        """
        Method to write transactions to a string in CSV format.
        Returns the CSV formatted string.
        """
        file = io.StringIO()
        CSVHandler._write_transactions(transactions, file)
        return file.getvalue()

    @staticmethod
    def _write_transactions(
        transactions: List[Tuple[str, str, int]], file: io.StringIO
    ) -> None:
        """
        Helper method to write transactions to a file-like object.
        """
        csv_writer = csv.writer(file)
        for transaction in transactions:
            csv_writer.writerow(transaction)
