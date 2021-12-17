import boto3
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import config

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME

resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

table = resource.Table('Library')

def check_rental_possible(title):
    response = table.get_item(
        Key = {
            'title'    :title
        },
        AttributesToGet=[
            'rental'
        ]
    )
    return response
    #렌탈 가능할때 true

def change_rental_status(title, ren_name):
    response = table.update_item(
        Key = {
            'title'    :title
        },

        AttributeUpdates = {
            'rental' : {
                'Value'     : False,
                'Action'    : 'PUT'
            },
            'ren_name' : {
                'Value'     : ren_name,
                'Action'    : 'PUT'
            }
        }
    )
    return response

def return_book(title):
    response = table.update_item(
        Key = {
            'title'    :title
        },

        AttributeUpdates = {
            'rental' : {
                'Value'     : True,
                'Action'    : 'PUT'
            },
            'ren_name' : {
                'Value'     : 'none',
                'Action'    : 'PUT'
            },
            'ren_date' : {
                'Value'     : 'none',
                'Action'    : 'PUT'
            }
        }
    )
    return response

def rental_search_book(ren_name):
    response = table.scan(
        FilterExpression=Attr('ren_name').eq(ren_name)
    )

    items = response['Items']
    
    return items