
from moto import mock_dynamodb2
import boto3
import os 

mock_create_valid_evaluation = {
            "sub": "ABCABC",
            "string": "ABCABCABCABCABCABC"
        }

mock_create_invalid_evaluation = {
            "sub": "ABCABC",
            "string": "DFABCGHABC"
        }
       

@mock_dynamodb2
def setup_mocks():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName= os.environ['TABLE_NAME'],
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
    )
    
    table.put_item(
        Item=mock_composer
    )

    table.put_item(
        Item=mock_song
    )

    table.put_item(
        Item=another_mock_song
    )