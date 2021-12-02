from pprint import pprint
import boto3
import json
from botocore.exceptions import ClientError
from flask.wrappers import Response
from werkzeug.wrappers import response
from flask import jsonify


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


def select_all(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')
    response = table.scan()
    data = response['Items']

    return data


def update_table(id, title, author, publish, rental, ren_date, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')

    response = table.update_item(
        Key={
            'id': id,
            'title': title,
            'author': author,
            'publish': publish,
            'rental': rental,
            'ren_date': ren_date
        }
    )
    return response
