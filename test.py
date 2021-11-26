import boto3

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id = 'AKIARKVEYCRB5V6OTNXL',
    aws_secret_access_key = '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',
    region_name = 'ap-northeast-2'
    )

table = dynamodb.create_table(
    TableName = 'users',
    KeySchema = [
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'last_name',
            'KeyType': 'RANGE'
        }
    ],

    AttributeDefinitions = [
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'last_name',
            'AttributeType': 'S'
        }
    ],

    ProvisionedThroughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

table.meta.client.get_waiter('table_exists').wait(TableName='users')

print(table.item_count)