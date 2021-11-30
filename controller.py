import boto3

table_name = 'TEST'


def read_from_Table(id, client):
    Table = client.Table(table_name)
    response = Table.get_item(
        Key={
            'id': id
        },
        AttributesToGet=[
            'name'
        ]
    )
    return response