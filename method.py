import boto3
from boto3.dynamodb.conditions import Key, Attr
import config

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME


def put_table(id, title, author, publish, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME)

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
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-northeast-2')

    response = dynamodb.Table('library')

    return response


def select_all(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')
    response = table.scan()
    data = response['Items']

    return data


def update_table(b_title, id, title, author, publish, rental, ren_date, ren_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')
    print(b_title)
    response = table.update_item(
        Key={
            'title': b_title
        },
        AttributeUpdates={
            'id': {
                'Value': id,
                'Action': 'PUT'
            },
            'author': {
                'Value': author,
                'Action': 'PUT'
            },
            'publish': {
                'Value': publish,
                'Action': 'PUT'
            },
            'rental': {
                'Value': rental,
                'Action': 'PUT'
            },
            'ren_date': {
                'Value': ren_date,
                'Action': 'PUT'
            },
            'ren_name': {
                'Value': ren_name,
                'Action': 'PUT'
            }

        }
    )
    return response


def get_book(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')

    response = table.scan(
        FilterExpression=Attr('title').contains(title)
    )

    items = response['Items']
    return items


def delete_table(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')

    response = table.delete_item(
        Key={
            'title': title
        }
    )

    return response
