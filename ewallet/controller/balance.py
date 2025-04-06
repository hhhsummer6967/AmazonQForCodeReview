import json
import os
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
wallets_table = dynamodb.Table(os.environ['WALLETS_TABLE'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Get wallet ID from path parameters
        wallet_id = event['pathParameters']['id']
        
        # Get wallet details from DynamoDB
        response = wallets_table.get_item(
            Key={
                'id': wallet_id
            }
        )
        
        # Check if wallet exists
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': f'Wallet with ID {wallet_id} not found'
                })
            }
        
        wallet = response['Item']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'wallet_id': wallet['id'],
                'balance': wallet.get('balance', '0'),
                'currency': wallet.get('currency', 'USD'),
                'last_updated': wallet.get('last_updated')
            }, cls=DecimalEncoder)
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': f'Internal server error: {str(e)}'
            })
        }
