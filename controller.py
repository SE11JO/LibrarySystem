from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import config

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
USER_TABLE_NAME = config.USER_TABLE_NAME
BOOK_TABLE_NAME = config.BOOK_TABLE_NAME

resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)


def create_table_user():
    table = resource.create_table(
        TableName=USER_TABLE_NAME,  # Name of the table
        KeySchema=[
            {
                'AttributeName': 'Email',
                'KeyType': 'HASH'  # RANGE = sort key, HASH = partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Email',  # Name of the attribute
                'AttributeType': 'S'  # N = Number (B= Binary, S = String)
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


UserTable = resource.Table('Library-System-UserTable')


def register_new_user(email, name, password):
    response = UserTable.put_item(
        Item={
            'Email': email,
            'Name': name,
            'Password': password,
        }
    )
    return response


def read_user_information(email):
    response = UserTable.get_item(
        Key={
            'Email': email
        },
        AttributesToGet=[
            'Email',
            'Password',
            'Name'
        ]
    )
    return response


table = resource.Table(BOOK_TABLE_NAME)


def search_library_book(book_title):
    response = table.scan(
        FilterExpression=Attr('title').contains(book_title)
    )

    items = response['Items']

    return items


def change_rental_status(title, ren_name, ren_date):
    response = table.update_item(
        Key={
            'title': title
        },

        AttributeUpdates={
            'rental': {
                'Value': False,
                'Action': 'PUT'
            },
            'ren_name': {
                'Value': ren_name,
                'Action': 'PUT'
            },
            'ren_date': {
                'Value': ren_date,
                'Action': 'PUT'
            }
        }
    )
    return response


def check_rental_possible(title):
    response = table.get_item(
        Key={
            'title': title
        },
        AttributesToGet=[
            'rental'
        ]
    )
    return response
    # ?????? ???????????? true


def rental_search_book(ren_name):
    response = table.scan(
        FilterExpression=Attr('ren_name').eq(ren_name)
    )

    items = response['Items']

    return items
