import boto3
import json
import os


def get_secret(secret_name, region_name="eu-north-1"):
    """
    Fetch a secret from AWS Secrets Manager.
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret = response["SecretString"]
            return json.loads(secret)
        else:
            return json.loads(response["SecretBinary"].decode("utf-8"))
    except Exception as e:
        raise Exception(f"Error fetching secret: {str(e)}")
