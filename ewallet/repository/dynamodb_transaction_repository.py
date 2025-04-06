import boto3
import uuid
from datetime import datetime
from typing import Any, Optional

from ewallet.repository.transaction_repository import TransactionRepository
from ewallet.model.transaction import Transaction, TransactionStatus, TransactionType
from ewallet.model.wallet import Wallet

class DynamoDbTransactionRepository(TransactionRepository):
  """
  Concrete class that implements the TransactionRepository interface.
  This class is responsible for interacting with the DynamoDB database.
  """
  def __init__(self, dynamodb_client: boto3.client, table_name: str, wallet_index_name: str):
    self.dynamodb_client = dynamodb_client
    self.table_name = table_name
    self.wallet_index_name = wallet_index_name

  def save(self, transaction: Transaction) -> str:
    """
    Saves a transaction to the DynamoDB database.

    :param transaction: The transaction to save.
    :return: The id of the saved transaction.
    :rtype: str
    """
    transaction.id = str(uuid.uuid4())

    self.dynamodb_client.put_item(
      TableName=self.table_name,
      Item={
        'id': {'S': transaction.id},
        'wallet_id': {'N': str(transaction.wallet.id)},
        'amount': {'N': str(transaction.amount)},
        'currency': {'S': transaction.currency},
        'type': {'S': transaction.type.name},
        'status': {'S': transaction.status.name},
        'created_at': {'S': transaction.created_at.isoformat()}
      }
    )

    return transaction.id

  def find(self, transaction_id: str) -> Optional[Any]:
    """
    Finds a transaction in the DynamoDB database by id.

    :param str transaction_id: The id of the transaction to find.
    :return: The found transaction.
    :rtype: Any
    """
    response = self.dynamodb_client.get_item(
      TableName=self.table_name,
      Key={'id': {'S': transaction_id}}
    )

    if 'Item' not in response:
      return None

    transaction = Transaction(
      None,
      float(response['Item']['amount']['N']),
      response['Item']['currency']['S'],
      TransactionType[response['Item']['type']['S']]
    )
    transaction.id = response['Item']['id']['S']
    transaction.status = TransactionStatus[response['Item']['status']['S']]
    transaction.created_at = datetime.fromisoformat(response['Item']['created_at']['S'])

    return transaction

  def list_transactions_by_wallet(self, wallet: Wallet) -> list[Transaction]:
    """
    Lists all transactions for a given wallet.

    :param wallet: The wallet to list transactions for.
    :return: A list of transactions for the given wallet.
    :rtype: list[Transaction]
    """
    response = self.dynamodb_client.query(
      TableName=self.table_name,
      IndexName=self.wallet_index_name,
      KeyConditionExpression='wallet_id = :wallet_id',
      ExpressionAttributeValues={':wallet_id': {'N': str(wallet.id)}}
    )

    transactions = []
    for item in response['Items']:
      transaction =Transaction(
        wallet=wallet,
        amount=float(item['amount']['N']),
        currency=item['currency']['S'],
        type=TransactionType[item['type']['S']])
      transaction.id = item['id']['S']
      transaction.status = TransactionStatus[transaction.status]
      transaction.created_at = datetime.fromisoformat(item['created_at']['S'])
      transactions.append(transaction)

    return transactions