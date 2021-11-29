from pprint import pprint
import boto3
from botocore.exceptions import ClientError


def put_table(id, title, author, publish, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')
    response = table.put_item(
        Item={
            'id': id,
            'title': title,
            'author': author,
            'publish': publish,
            'rental': True,
            'ren_name': '',
            'ren_date': ''
        }
    )

    return response


def get_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
            region_name='ap-northeast-2')

    response = dynamodb.Table('library')

    return response


def select_all(table_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
            region_name='ap-northeast-2')

    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']
    return print(data)

    
