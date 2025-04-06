import json
import logging
import os
import boto3

from ewallet.repository.dynamodb_wallet_repository import DynamoDbWalletRepository
from ewallet.repository.base_repository import BaseRepository
from ewallet.model.wallet import Wallet

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_wallet_repository(dynamodb_client, table_name) -> BaseRepository:
  return DynamoDbWalletRepository(dynamodb_client, table_name)

def save_wallet(wallet, wallet_table_name):
  wallet_repository = get_wallet_repository(boto3.client('dynamodb'), wallet_table_name)
  wallet_repository.save(wallet)

def lambda_handler(event, context):
  try:
    logger.info('Event: {}'.format(event))
    logger.info('Context: {}'.format(context))

    wallet_table_name = os.getenv('WALLETS_TABLE')
    if (not wallet_table_name):
      raise Exception('Table name missing')

    try:
      payload = json.loads(event['body'])
    except Exception as error:
      return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Bad Request'})
      }

    if ('name' not in payload):
      return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Wallet name missing'})
      }

    wallet = Wallet(payload['name'])
    save_wallet(wallet, wallet_table_name)

    response = {
      'statusCode': 201,

      'body': json.dumps(wallet.__dict__)
    }
    logger.info("Response: %s", response)

    return response

  except Exception as error:
    logger.info('Error: {}'.format(error))
    return {
      'statusCode': 500,
      'body': {'message': error}
    }
