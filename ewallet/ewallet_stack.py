from os import path
import os
from aws_cdk import (
  StackProps,
  Stack,
  CfnOutput
)
from constructs import Construct
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_dynamodb as dynamodb

ApiGatewayEndpointStackOutput = 'ApiEndpoint'
ApiGatewayDomainStackOutput = 'ApiDomain'
ApiGatewayStageStackOutput = 'ApiStage'

class EWalletStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)


    wallets_table = dynamodb.Table(self, 'WalletsTable',
      partition_key=dynamodb.Attribute(
        name='id',
        type=dynamodb.AttributeType.STRING
      )
    )

    transactions_table = dynamodb.Table(self, 'TransactionsTable',
      partition_key=dynamodb.Attribute(
        name='id',
        type=dynamodb.AttributeType.STRING
      )
    )

    create_wallet_function = lambda_.Function(self, 'CreateWalletFunction',
      runtime=lambda_.Runtime.PYTHON_3_9,
      code=lambda_.AssetCode.from_asset(path.join(os.getcwd(), 'ewallet/model')),
      handler='create_wallet.lambda_handler',
      environment={
        "WALLETS_TABLE": wallets_table.table_name
      },
      tracing=lambda_.Tracing.ACTIVE
    )
    wallets_table.grant_read_write_data(create_wallet_function)


    withdraw_function = lambda_.Function(self, 'WithdrawFunction',
      runtime=lambda_.Runtime.PYTHON_3_9,
      code=lambda_.AssetCode.from_asset(path.join(os.getcwd(), 'ewallet/controller')),
      handler='withdraw.lambda_handler',
      environment={
        "WALLETS_TABLE": wallets_table.table_name,
        "TRANSACTIONS_TABLE": transactions_table.table_name
      },
      tracing=lambda_.Tracing.ACTIVE
    )
    wallets_table.grant_read_data(withdraw_function)
    transactions_table.grant_read_write_data(withdraw_function)

    apiGateway = apigateway.RestApi(self, 'ApiGateway',
      default_cors_preflight_options=apigateway.CorsOptions(
        allow_credentials=True,
        allow_origins=apigateway.Cors.ALL_ORIGINS,
        allow_methods=["GET", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Content-Length", "X-Requested-With"]
      )
    )

    api = apiGateway.root.add_resource('api')

    wallets = api.add_resource('wallets',
      default_cors_preflight_options=apigateway.CorsOptions(
        allow_credentials=True,
        allow_origins=apigateway.Cors.ALL_ORIGINS,
        allow_methods=["GET", "PUT", "DELETE", "OPTIONS", "POST"],
        allow_headers=["Content-Type", "Authorization", "Content-Length", "X-Requested-With"]
      )
    )
    wallets.add_method('POST', apigateway.LambdaIntegration(create_wallet_function))

    wallets.add_resource('{id}',
      default_cors_preflight_options=apigateway.CorsOptions(
        allow_credentials=True,
        allow_origins=apigateway.Cors.ALL_ORIGINS,
        allow_methods=["GET", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Content-Length", "X-Requested-With"]
      )
    )

    withdraw = api.add_resource('withdraw',
      default_cors_preflight_options=apigateway.CorsOptions(
        allow_credentials=True,
        allow_origins=apigateway.Cors.ALL_ORIGINS,
        allow_methods=["PUT", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Content-Length", "X-Requested-With"]
      )
    )

    wallet_withdraw = withdraw.add_resource('{id}',
      default_cors_preflight_options=apigateway.CorsOptions(
        allow_credentials=True,
        allow_origins=apigateway.Cors.ALL_ORIGINS,
        allow_methods=["PUT", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Content-Length", "X-Requested-With"]
      )
    )
    wallet_withdraw.add_method('PUT', apigateway.LambdaIntegration(withdraw_function))

    CfnOutput(self, ApiGatewayEndpointStackOutput,
      value=apiGateway.url
    )

    CfnOutput(self, ApiGatewayDomainStackOutput,
      value=apiGateway.url.split('/')[2]
    )

    CfnOutput(self, ApiGatewayStageStackOutput,
      value=apiGateway.deployment_stage.stage_name
    )
