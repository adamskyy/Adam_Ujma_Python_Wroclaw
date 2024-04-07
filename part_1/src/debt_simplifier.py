from typing import List, Tuple, Dict
from collections import defaultdict


class DebtSimplifier:
    @classmethod
    def minimize_cash_flow(
        cls, transactions: List[Tuple[str, str, int]]
    ) -> List[Tuple[str, str, int]]:
        """
        Minimizes the cash flow among a group of people based on a list of transactions.
        Each transaction is expected to be in the format: creditor, debtor, amount.
        Returns a list of optimized transactions in the format: debtor, creditor, amount.
        """
        net_amounts = cls._calculate_net_amounts(transactions)
        optimized_transactions = []

        while not cls._all_balances_settled(net_amounts):
            max_debtor, max_creditor = cls._identify_max_debtor_creditor(net_amounts)
            min_amount = min(-net_amounts[max_debtor], net_amounts[max_creditor])

            net_amounts[max_debtor] += min_amount
            net_amounts[max_creditor] -= min_amount

            optimized_transactions.append((max_debtor, max_creditor, min_amount))

        return optimized_transactions

    @staticmethod
    def _calculate_net_amounts(
        transactions: List[Tuple[str, str, int]]
    ) -> Dict[str, int]:
        """
        Calculates the net amount each person should pay or receive.
        Return a dictionary mapping each person to their net amount.
        """
        net_amounts = defaultdict(int)
        for creditor, debtor, amount in transactions:
            net_amounts[debtor] -= amount
            net_amounts[creditor] += amount
        net_amounts = {
            person: amount for person, amount in net_amounts.items() if amount != 0
        }
        return dict(net_amounts)

    @staticmethod
    def _all_balances_settled(net_amounts: Dict[str, int]) -> bool:
        """
        Checks if all balances are settled.
        Returns True if all balances are settled, False otherwise.
        """
        return all(amount == 0 for amount in net_amounts.values())

    @staticmethod
    def _identify_max_debtor_creditor(net_amounts: Dict[str, int]) -> Tuple[str, str]:
        """Identifies the maximum debtor and creditor. Returns the tuple with their names."""
        max_debtor = min(net_amounts, key=net_amounts.get)
        max_creditor = max(net_amounts, key=net_amounts.get)
        return max_debtor, max_creditor
