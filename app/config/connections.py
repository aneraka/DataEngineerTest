import json
import boto3
from . import settings
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine, URL

ENGINE = create_engine(
    URL.create(
        drivername='postgresql',
        database=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        username=settings.DB_USER,
        password=settings.DB_PASS
    )
)



def conn_bd():
    return ENGINE

def session_db() -> Session:
    return Session(ENGINE)


def close_db(connection):
    connection.close()


def s3_client():
    return boto3.client(
        's3',
        region_name=settings.AWS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )


def get_aws_session():
    return boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )


def get_s3_resource(session: boto3.Session):
    return session.resource("s3")
