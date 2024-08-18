import boto3
from datetime import datetime
import json
import os

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello, world!'
    }