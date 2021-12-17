from pprint import pprint
import boto3
import json
from botocore.exceptions import ClientError
from flask.templating import render_template
from flask.wrappers import Response
from werkzeug.wrappers import response
from flask import jsonify
from boto3.dynamodb.conditions import Key, Attr


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


def update_table(b_title, id, title, author, publish, rental, ren_date, ren_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')
    print(b_title)
    response = table.update_item(
        Key={
            'title':b_title
        },
        AttributeUpdates = {
            'id' : {
                'Value' : id,
                'Action' : 'PUT'
            },
            'author' : { 
                'Value' : author,
                'Action' : 'PUT'
            },
            'publish' : { 
                'Value' : publish,
                'Action' : 'PUT'
            },
            'rental' : { 
                'Value' : rental,
                'Action' : 'PUT'
            },
            'ren_date' : { 
                'Value' : ren_date,
                'Action' : 'PUT'
            },
            'ren_name' : { 
                'Value' : ren_name,
                'Action' : 'PUT'
            }

        }
    )
    return response


def get_book(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
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
            aws_access_key_id='AKIARKVEYCRB5V6OTNXL',
            aws_secret_access_key='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',
            region_name='ap-northeast-2')

    table = dynamodb.Table('library')

    try:
        response=table.delete_item(
            Key={
                'title':title
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response