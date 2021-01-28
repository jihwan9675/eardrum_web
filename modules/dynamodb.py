import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import os, hashlib

def dynamoDBsignin(id, password):
    aws_access_key_id = os.environ.get('aws_access_key_id')
    aws_secret_access_key = os.environ.get('aws_secret_access_key')
    region_name = "ap-northeast-2" # us-east-1
    dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    table = dynamodb.Table('webUser')

    try:
        response = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(response)
        if response.get('Count')==0:
            response = table.put_item(
                Item={
                    'id': id,
                    "pw" : password
                }
            )
            return True
        else:
            return False
    
def dynamoDBcheckLogin(id, password):
    aws_access_key_id = os.environ.get('aws_access_key_id')
    aws_secret_access_key = os.environ.get('aws_secret_access_key')
    region_name = "ap-northeast-2" # us-east-1
    dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    table = dynamodb.Table('webUser')

    try:
        response = table.query(
            KeyConditionExpression=Key('id').eq(id) & Key('pw').eq(password)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(response)
        if response.get('Count')==1:
            return True
        else:
            return False

def makemd5(password):
    after_password = password.encode('utf-8')
    password_hash = hashlib.md5()
    password_hash.update(after_password)
    
    return password_hash.hexdigest()