import unittest
from src.debt_simplifier import DebtSimplifier
from src.csv_handler import CSVHandler


class TestDebtSimplifierUnit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up resources before any tests are run"""
        cls.debt_files = [
            "tests/test_data/debts_1.csv",
            "tests/test_data/debts_2.csv",
            "tests/test_data/debts_3.csv",
        ]
        cls.result_files = [
            "tests/test_data/results_1.csv",
            "tests/test_data/results_2.csv",
            "tests/test_data/results_3.csv",
        ]

    def test_calculate_net_amounts_simple(self):
        transactions = [
            ("Alice", "Bob", 100),
            ("Bob", "Charlie", 50),
            ("Charlie", "Alice", 30),
        ]
        expected_net_amounts = {"Alice": 70, "Bob": -50, "Charlie": -20}
        net_amounts = DebtSimplifier._calculate_net_amounts(transactions)
        self.assertEqual(net_amounts, expected_net_amounts)

    def test_identify_max_debtor_creditor(self):
        net_amounts = {"Alice": -100, "Bob": 50, "Charlie": 50}
        expected = ("Alice", "Bob")
        result = DebtSimplifier._identify_max_debtor_creditor(net_amounts)
        self.assertEqual(result, expected)

    def test_minimize_cash_flow(self):
        transactions = [
            ("Alice", "Bob", 10),
            ("Bob", "Alice", 5),
            ("Charlie", "Bob", 5),
            ("John", "Michael", 13),
        ]
        expected_optimized_transactions = [
            ("Michael", "John", 13),
            ("Bob", "Alice", 5),
            ("Bob", "Charlie", 5),
        ]
        optimized_transactions = DebtSimplifier.minimize_cash_flow(transactions)
        self.assertCountEqual(optimized_transactions, expected_optimized_transactions)

    def test_all_balances_settled_true(self):
        net_amounts = {"Alice": 0, "Bob": 0, "Charlie": 0}
        self.assertTrue(
            DebtSimplifier._all_balances_settled(net_amounts),
            "Should return True when all balances are settled",
        )

    def test_all_balances_settled_false(self):
        net_amounts = {"Alice": 100, "Bob": -100, "Charlie": 0}
        self.assertFalse(
            DebtSimplifier._all_balances_settled(net_amounts),
            "Should return False when any balance is not settled",
        )

    def test_minimize_cash_flow_1(self):
        """Test minimizing cash flow for the first set of transactions"""
        self._test_minimize_cash_flow(0)

    def test_minimize_cash_flow_2(self):
        """Test minimizing cash flow for the second set of transactions"""
        self._test_minimize_cash_flow(1)

    def test_minimize_cash_flow_3(self):
        """Test minimizing cash flow for the third set of transactions"""
        self._test_minimize_cash_flow(2)

    def _test_minimize_cash_flow(self, index):
        # Read the debts from file
        transactions = CSVHandler.read_transactions_from_csv(self.debt_files[index])
        # Process the transactions with DebtSimplifier
        optimized_transactions = DebtSimplifier.minimize_cash_flow(transactions)
        # Read the expected results
        expected_results = CSVHandler.read_transactions_from_csv(
            self.result_files[index]
        )

        self.assertCountEqual(
            optimized_transactions,
            expected_results,
            "The optimized transactions do not match the expected results",
        )


if __name__ == "__main__":
    unittest.main()
