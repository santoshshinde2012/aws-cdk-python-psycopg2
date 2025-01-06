from shared.get_secret import get_secret
from urllib.parse import quote_plus
import os


def get_dburl(secret_name, region_name="eu-north-1"):
    """
    Fetch a secret from AWS Secrets Manager.
    """
    try:
        if os.getenv("ENV") == "local":
            DATABASE_URL = (
                "postgresql://postgres:postgres@host.docker.internal:5432/testdb"
            )
            return DATABASE_URL
        else:
            secret = get_secret(secret_name)
            username = secret.get("username")
            password = secret.get("password")
            host = secret.get("host")
            port = secret.get("port")
            dbname = secret.get("dbname")
            engine = secret.get("engine")

            if not all([username, password, host, port, dbname, engine]):
                raise ValueError("One or more required secret fields are missing!")

            encoded_password = quote_plus(password)
            DATABASE_URL = (
                f"postgresql://{username}:{encoded_password}@{host}:{port}/{dbname}"
            )
            return DATABASE_URL
    except Exception as e:
        raise Exception(f"Error fetching secret: {str(e)}")
