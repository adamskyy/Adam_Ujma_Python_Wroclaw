import logging
import io
import json
from typing import Any, Dict, List, Tuple, TYPE_CHECKING
import boto3
from src.aws import get_s3_client, get_sqs_client
from src.config import get_config
from src.csv_handler import CSVHandler
from src.debt_simplifier import DebtSimplifier

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_sqs import SQSClient

logger = logging.getLogger(__name__)

def process_message(message: Dict[str, Any], s3_client: "S3Client") -> None:
    """Process a message from the SQS queue."""
    # Extract debts_id from message
    message_body = json.loads(message['Body'])
    # Extract the debts_id
    debts_id = message_body['debts_id']
    
    logger.info(f"Processing debts file: {debts_id}")
    
    # Read file directly from S3 into memory
    transactions = read_file_from_s3(s3_client, debts_id)
    
    # Process CSV content
    optimized_transactions = DebtSimplifier.minimize_cash_flow(transactions)
    logger.info(f"Optimized transactions for {debts_id}")
    
    # Upload optimized transactions back to S3
    upload_file_to_s3(s3_client, f"{debts_id}_results", optimized_transactions)
    

def poll_sqs_queue(sqs_client: "SQSClient", s3_client: "S3Client") -> None:
    """Poll the SQS queue for messages."""
    config = get_config()
    while True:
        messages = sqs_client.receive_message(
            QueueUrl=config.worker_queue_url,
            MaxNumberOfMessages=5, # Should be adjusted based on the number of messages expected
            WaitTimeSeconds=20, # Should be adjusted based on the expected wait time
        ).get('Messages', [])

        logger.info(f"Received messegas: {len(messages)}")
        logger.info(f"Messages: {messages}")
        
        for message in messages:
            process_message(message, s3_client)
            sqs_client.delete_message(
                QueueUrl=config.worker_queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )

def read_file_from_s3(s3_client: "S3Client", key: str) -> List[Tuple[str, str, int]]:
    """Read a file from S3 and return the transactions."""
    config = get_config()
    logger.info(f"Reading file from S3: {key}")
    try:
        response = s3_client.get_object(Bucket=config.debts_bucket_name, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        transactions = CSVHandler.read_transactions_from_content(file_content)
        return transactions
    except s3_client.exceptions.NoSuchKey:
        logger.error(f"File not found in S3: {key}")
        raise


def upload_file_to_s3(s3_client: "S3Client", key: str, transactions: List[Tuple[str, str, int]]) -> None:
    """Upload a file with the optimized transactions to S3."""
    config = get_config()
    logger.info(f"Uploading file to S3: {key}")
    try:
        csv_content = CSVHandler.write_transactions_to_content(transactions)
        fileobj = io.BytesIO(csv_content.encode('utf-8'))
        s3_client.upload_fileobj(Bucket=config.debts_bucket_name, Key=key, Fileobj=fileobj)
    except Exception as e:
        logger.error(f"Failed to upload file to S3: {key}")
        raise e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting worker service...")
    
    s3_client = get_s3_client()
    sqs_client = get_sqs_client()
    
    poll_sqs_queue(sqs_client, s3_client)