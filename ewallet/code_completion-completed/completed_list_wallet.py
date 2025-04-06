import json
import logging
import os
import boto3

from ewallet.repository.dynamodb_wallet_repository import DynamoDbWalletRepository
from ewallet.repository.base_repository import BaseRepository
from ewallet.model.wallet import Wallet

# create a logger at the INFO level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# function to get wallet repository using dynamodb client and table name
def get_wallet_repository(table_name):
  dynamodb_client = boto3.client('dynamodb')
  return DynamoDbWalletRepository(dynamodb_client, table_name)

# function to list wallets using the wallet table name, including comments to explain each line
def list_wallets(table_name):
  # create a wallet repository using the table name
  wallet_repository = get_wallet_repository(table_name)
  # get all wallets from the wallet repository
  wallets = wallet_repository.get_all()
  # return the list of wallets
  return wallets

def excute_command(command):
  subprocess.run(command, shell=True)
# import subprocess
  
# create the lambda handler function
def lambda_handler(event, context):
    # get the table name from environment variable
    table_name = os.environ['TABLE_NAME']
    # list the wallets
    wallets = list_wallets(table_name)
    # return the list of wallets
    return {
    'statusCode': 200,
    'body': json.dumps(wallets)
  }
