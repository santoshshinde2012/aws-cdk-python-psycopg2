import os

class Config:
    SECRET_NAME = os.getenv("SECRET_NAME")

    if not SECRET_NAME:
        raise ValueError("Environment variable SECRET_NAME is not set!")
