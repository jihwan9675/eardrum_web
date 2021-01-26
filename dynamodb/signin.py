import boto3
from botocore.exceptions import ClientError
import os

def signin(id, password, grade, dynamodb=None):
    if not dynamodb:
        aws_access_key_id = os.environ.get('aws_access_key_id')
        aws_secret_access_key = os.environ.get('aws_secret_access_key')
        region_name = "ap-northeast-2" # us-east-1
        dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    table = dynamodb.Table('earUser')
    response = table.put_item(
       Item={
            'id': id,
            "password" : password,
            'grade': grade
        }
    )

    return response

def check_login(id, password,grade):

    aws_access_key_id = os.environ.get('aws_access_key_id')
    aws_secret_access_key = os.environ.get('aws_secret_access_key')
    region_name = "ap-northeast-2" # us-east-1
    dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    table = dynamodb.Table('User')

    try:
        response = table.get_item(Key={'id': id, "pw":password})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if response.get('Item'):
            print("login")
        else:
            print("check your id or pw")


if __name__ == '__main__':
    movie_resp = signin("11", "11", "1", 0)
    check_login("vatech", "vatech12","2")
