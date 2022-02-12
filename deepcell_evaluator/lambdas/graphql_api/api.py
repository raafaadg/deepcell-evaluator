import sys
import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import AppSyncResolver

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.dynamodb import ddb
    
tracer = Tracer(service="sample_resolver")
logger = Logger(service="sample_resolver")

app = AppSyncResolver()


@app.resolver(type_name="Mutation", field_name="createEvaluation")
def evaluate(sub: str, string:str):
    _, response = ddb.add_evaluation(sub, string)
    return response

@app.resolver(type_name="Mutation", field_name="deleteEvaluation")
def delete(id:str):
    try :
        _, response = ddb.delete_evaluation(id)
        return response
    except:
        return f'ID :{id} not found.'

@app.resolver(type_name="Query", field_name="allEvaluations")
def list(limit):
    try:
        limit = int(limit)
        
        if limit > 20 or str(limit) == '0' or str(limit) == '':
            limit = 20
    except:
        return []
    return ddb.list_evaluations(limit)


@app.resolver(type_name="Query", field_name="getEvaluation")
def check(id:str):
    if id:
        _, response = ddb.get_evaluation(id)
        return response
    return f'ID :{id} not found.'

@app.resolver(type_name="Mutation", field_name="updateEvaluation")
def update(id:str, sub:str, string:str):
    data = {
        "sub":sub,
        "string":string
    }
    try :
        _, response = ddb.update_evaluation(id, data)
        return response
    except:
        return 'ID :{id} not found.'
    
@logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    return app.resolve(event, context)