import unittest
import os
from src.csv_handler import CSVHandler


class TestCSVHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up resources before any tests are run"""
        cls.valid_file_path = "tests/test_data/valid_transactions.csv"
        cls.invalid_file_path = "tests/test_data/invalid_transactions.csv"
        cls.invalid_amount_file_path = "tests/test_data/invalid_amount_transactions.csv"
        cls.floating_number_amount_file_path = (
            "tests/test_data/floating_number_transactions.csv"
        )
        cls.output_file_path = "tests/test_data/output_transactions.csv"
        # Create a valid CSV file for reading tests
        with open(cls.valid_file_path, "w", encoding="utf-8", newline="") as file:
            file.write("Alice,Bob,100\nBob,Charlie,200\n")
        # Prepare an invalid CSV file with missing values
        with open(
            cls.invalid_file_path, mode="w", encoding="utf-8", newline=""
        ) as file:
            file.write("Alice,Bob\nBob,Charlie,TwoHundred\nAlice,,100\n")
        # Prepare an invalid CSV file with invalid amount values
        with open(
            cls.invalid_amount_file_path, mode="w", encoding="utf-8", newline=""
        ) as file:
            file.write("Alice,Bob,100\nBob,Charlie,-200\n")
        # Prepare a CSV file with floating point amount values
        with open(
            cls.floating_number_amount_file_path, mode="w", encoding="utf-8", newline=""
        ) as file:
            file.write("Alice,Bob,100.5\nBob,Charlie,200.7\n")

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all tests have run"""
        os.remove(cls.valid_file_path)
        os.remove(cls.invalid_file_path)
        os.remove(cls.invalid_amount_file_path)
        os.remove(cls.floating_number_amount_file_path)
        if os.path.exists(cls.output_file_path):
            os.remove(cls.output_file_path)

    def test_read_transactions_from_csv_valid(self):
        """Test reading transactions from a valid CSV file"""
        transactions = CSVHandler.read_transactions_from_csv(self.valid_file_path)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0], ("Alice", "Bob", 100))
        self.assertEqual(transactions[1], ("Bob", "Charlie", 200))

    def test_read_transactions_from_csv_invalid_row(self):
        """Test handling of invalid rows in the CSV file"""
        with self.assertRaises(ValueError):
            CSVHandler.read_transactions_from_csv(self.invalid_file_path)

    def test_read_transactions_from_csv_invalid_amount(self):
        """Test handling of invalid amount values in the CSV file"""
        with self.assertRaises(ValueError):
            CSVHandler.read_transactions_from_csv(self.invalid_amount_file_path)

    def test_read_transactions_from_csv_file_not_found(self):
        """Test file not found exception"""
        with self.assertRaises(FileNotFoundError):
            CSVHandler.read_transactions_from_csv("non_existent_file.csv")

    def test_read_transactions_from_csv_floating_point_amount(self):
        """Test handling of floating point amount values in the CSV file"""
        with self.assertRaises(ValueError):
            CSVHandler.read_transactions_from_csv(self.floating_number_amount_file_path)

    def test_write_transactions_to_csv(self):
        """Test writing transactions to a CSV file"""
        transactions = [("Charlie", "Alice", 150), ("Dave", "Charlie", 50)]
        CSVHandler.write_transactions_to_csv(transactions, self.output_file_path)
        self.assertTrue(os.path.exists(self.output_file_path))
        # Read back the file to check if the transactions were written correctly
        with open(self.output_file_path, "r", encoding="utf-8") as file:
            contents = file.read()
        self.assertIn("Charlie,Alice,150", contents)
        self.assertIn("Dave,Charlie,50", contents)


if __name__ == "__main__":
    unittest.main()
