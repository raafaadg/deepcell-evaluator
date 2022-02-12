import boto3
import os
from .evaluator import Evaluator
from aws_lambda_powertools.utilities.data_classes.appsync import scalar_types_utils

class DynamoDB():
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.resource = boto3.resource('dynamodb')
        self.table = self.resource.Table(os.getenv('DYNAMODB_TABLE_NAME', 'deepcell'))
        self.ITEM = {}
        
    def add_evaluation(self, sub:str = 'EMPTY', string:str = 'EMPTY'):
        response = Evaluator(sub=sub, string=string).to_json()
        ID = scalar_types_utils.make_id()
        TIMESTAMP = scalar_types_utils.aws_datetime()
        self.ITEM = {
                'id': ID,
                'sub': sub,
                'string': string,
                'result': str(response['result']),
                'message': response['message'],
                'conditions': response['conditions'],
                'timestamp': TIMESTAMP,
            }
        response_ddb = self.table.put_item(
            Item = self.ITEM
        )
       
        if response_ddb['ResponseMetadata']['HTTPStatusCode'] == 200:
            return self.ITEM
        return {'message':response_ddb}
    
    def get_evaluation(self, id:str):
        response_ddb = self.table.get_item(
            Key = {
                'id': id
            },
            AttributesToGet=[
                'sub', 'string', 'result', 'message', 'conditions', 'timestamp'
            ]
        )
        
        if response_ddb['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'id': str(id),
                'sub': response_ddb['Item']['sub'],
                'string': response_ddb['Item']['string'],
                'result': str(response_ddb['Item']['result']),
                'message': response_ddb['Item']['message'],
                'conditions': response_ddb['Item']['conditions'],
                'timestamp': response_ddb['Item']['timestamp']
            }
        return {'message':'Invalid ID!'}
    
    
    def update_evaluation(self, id:str, data:dict):
        response = Evaluator(data['sub'], data['string']).to_json()
        response_ddb = self.table.update_item(
            Key = {
                'id': id
            },
            AttributeUpdates={
                'sub': {
                    'Value'  : data['sub'],
                    'Action' : 'PUT' 
                },
                'string': {
                    'Value'  : data['string'],
                    'Action' : 'PUT'
                },
                'conditions': {
                    'Value'  : response['conditions'],
                    'Action' : 'PUT'
                },
                'result': {
                    'Value'  : response['result'],
                    'Action' : 'PUT'
                },
                'message': {
                    'Value'  : response['message'],
                    'Action' : 'PUT'
                },
                'timestamp': {
                    'Value'  : scalar_types_utils.aws_datetime(),
                    'Action' : 'PUT'
                }
            },
            ReturnValues = "UPDATED_NEW"
        )
        if response_ddb['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'id': id,
                'sub': response_ddb['Attributes']['sub'],
                'string': response_ddb['Attributes']['string'],
                'result': str(response_ddb['Attributes']['result']),
                'message': response_ddb['Attributes']['message'],
                'conditions': response_ddb['Attributes']['conditions'],
                'timestamp': response_ddb['Attributes']['timestamp']
            }
        return {'message':'Invalid ID!'}
    
    def delete_evaluation(self, id:str):
        response_ddb = self.table.delete_item(
            Key = {
                'id': id
            }
        )
        
        if response_ddb['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {'message':'Delete Complete!'}
        return {'message':'Delete Fail!'}
        
    def list_evaluations(self, limit):

        response = self.table.scan()
        data = response['Items']
        
        if len(data) > limit:
            return data[0:limit]
        
        while ('LastEvaluatedKey' in response and len(data) <= limit):
            response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
            
        resp = []
        for d in data:
            d['result'] = str(d['result']).replace("Decimal('","").replace("')","")
            resp.append(d)
            
        return resp

ddb = DynamoDB()