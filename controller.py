import boto3
from boto3.dynamodb.conditions import Key, Attr
import config


AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
BOOK_TABLE_NAME = config.BOOK_TABLE_NAME

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

table = resource.Table(BOOK_TABLE_NAME)


def search_library_book (book_title) :
    
    response = table.scan(
        FilterExpression=Attr('title').contains(book_title)
    )

    items = response['Items']

    return items

def change_rental_status(title, ren_name, ren_date):
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
            },
            'ren_date' : {
                'Value'     : ren_date,
                'Action'    : 'PUT'
            }
        }
    )
    return response

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

