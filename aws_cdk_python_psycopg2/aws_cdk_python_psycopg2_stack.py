from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_iam as iam,
    Duration,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct
import os


class AwsCdkPythonPsycopg2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the name of the secret in Secrets Manager
        secret_name = "local/database_url"

        # Define the Lambda Layer
        pythonlib_layer = _lambda.LayerVersion(
            self,
            "PyhonLibLayer",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "../layers/pythonlib_layer.zip")
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="sqlalchemy and psycopg2-binary packages",
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Define the Lambda function with environment variables
        my_lambda = _lambda.Function(
            self,
            id="MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="app.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"SECRET_NAME": secret_name, "ENV": "local"},
            layers=[pythonlib_layer],
        )

        # Define the IAM policy to grant Lambda function access to Secrets Manager
        my_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["secretsmanager:GetSecretValue"],
                resources=[
                    f"arn:aws:secretsmanager:{self.region}:{self.account}:secret:{secret_name}-*"
                ],
            )
        )
