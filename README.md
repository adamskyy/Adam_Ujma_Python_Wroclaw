# Adam_Ujma_Python_Wroclaw
Recruitment task - Ocado Technology

## Task 1

### Overview
The DebtSimplifier class provides a method to minimize cash flow among a group of people based on a list of transactions. This solution employs a greedy algorithm approach to reduce the complexity of debts by optimizing transactions.

### Algorithm Type
Greedy Algorithm - It iteratively picks the best current solution with the hope of finding the global optimum. In this context, it selects the maximum debtor and creditor in each iteration to settle debts efficiently.

### Time and Space Complexity
Time Complexity: O(n^2), where n is the number of unique individuals involved in the transactions. This complexity arises from iteratively identifying the maximum debtor and creditor in each loop until all balances are settled.  
Space Complexity: O(n), due to storing the net amounts for each individual in a dictionary.

### Pseudocode
1. For each person, calculate net amount (credits - debts).
2. Repeat until all persons are settled:
   a. Identify the person with the maximum credit (maxCreditor) and the person with the maximum debit (maxDebtor).  
   b. Determine the minimum amount between maxCreditor's credit and maxDebtor's debit, let this be minAmount.  
   c. Transfer minAmount from maxDebtor to maxCreditor.  
   d. Adjust the net amounts for maxDebtor and maxCreditor by subtracting minAmount from each.  
   e. If minAmount equals maxDebtor's debit, remove maxDebtor from consideration for future iterations.  
   f. If minAmount equals maxCreditor's credit, remove maxCreditor from consideration for future iterations.
3. Continue until no debts remain.


### Code Organization
The DebtSimplifier class helps simplify debts among people by calculating the minimum transactions needed, while the CSVHandler class manages reading and writing transaction data in CSV format. Both classes use static methods, meaning they don't hold any data from one method call to the next, making them simple and easy to use. They are separate to keep the code organized and clear. This design makes it easier for others to understand and use these utilities in different projects.

## Tests

The tests for DebtSimplifier and CSVHandler classes include unit tests, which examine individual methods to ensure they work correctly, and integration tests, which test the classes' functionalities together with real-world scenarios. For CSVHandler, tests cover reading and writing CSV files under various conditions, checking for errors and correct outputs. DebtSimplifier tests focus on internal logic, like calculating net amounts and simplifying debts, and also include scenarios that mimic actual use, such as processing transactions from CSV files and comparing the results with expected outputs. These tests aim to verify both the isolated and combined functionality of the classes, ensuring reliability and correctness.  
Additionally in the tests for DebtSimplifier and CSVHandler, two key assumptions were made: 
1) Debtor and creditor must be different individuals
2) Transaction amounts must be positive integers.

To run the tests execute from the /part_1 folder:
```
python -m unittest discover -s tests/
```


## Task 2
To implement the worker according to the requirements in the second task, I also used scripts designed to configure the s3-client and sqs-client, and read config from files contained in /api (aws.py and config.py)  
Worker has been implemented according to the requirements outlined in the instructions for the task fulfills the functionality:
1. receive data from the SQS queue
2. optimizes transfers
3. save the result in S3
It uses the DebtSimplifier and CSVHandler implemented for first task.

I tested implemented worker with integration tests written in /api/test/
```
poetry run pytest test/test_api_flow.py
```  
and with manual tests.
To run the tests, I had to make small changes to api/conftest.py so that it would execute correctly.