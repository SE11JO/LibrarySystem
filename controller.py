from boto3 import resource
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

table = resource.Table('books')

def read_books(id):
    response = table.get_item(
        Key = {
            'id'    :id
        },
        AttributesToGet=[
            'title'
        ]
    )
    return response

def check_rental_possible(id):
    response = table.get_item(
        Key = {
            'id'    :id
        },
        AttributesToGet=[
            'rental'
        ]
    )
    return response
    #렌탈 가능할때 true

def change_rental_status(id, ren_name):
    response = table.update_item(
        Key = {
            'id'    :id
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

def return_book(id):
    response = table.update_item(
        Key = {
            'id'    :id
        },

        AttributeUpdates = {
            'rental' : {
                'Value'     : True,
                'Action'    : 'PUT'
            },
            'ren_name' : {
                'Value'     : 'none',
                'Action'    : 'PUT'
            }
        }
    )
    return response

