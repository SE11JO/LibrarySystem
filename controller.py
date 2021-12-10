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
