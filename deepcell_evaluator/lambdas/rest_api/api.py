from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils.dynamodb import ddb

app = Flask(__name__)

SWAGGER_URL = '/docs'
API_URL = ('https://s3.amazonaws.com/deepcell-evaluator.com/swagger.json')
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Deepcell REST API Docs"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT)
cors = CORS(app)

@app.route('/ping', methods=['POST', 'GET'])
def ping():
    return jsonify(status='200', message={'return': 'pong'})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    sub = request.args.get('sub','EMPTY')
    string = request.args.get('string','EMPTY')
    response = ddb.add_evaluation(sub=sub, string=string)
    return jsonify(status=200, message=response)

@app.route('/delete', methods=['POST', 'DELETE'])
def delete():
    try :
        id = str(request.args.get('id'))
        response = ddb.delete_evaluation(id)
        return jsonify(status=200, message=response)
    except:
        return jsonify(status=400, message=f'ID :{id} not found.')

@app.route('/list', methods=['GET', 'POST'])
def list():
    limit = request.args.get('limit', 20)
    try:
        limit = int(limit)
        
        if limit > 20 or str(limit) == '0' or str(limit) == '':
            limit = 20
    except:
        return jsonify(status=400, message=f'Invalid Limit: {limit}')
    response = ddb.list_evaluations(limit)
    return jsonify(status=200, message=response)


@app.route('/check', methods=['GET'])
def check():
    id = str(request.args.get('id'))
    print(id)
    if id:
        response = ddb.get_evaluation(id)
        return jsonify(status=200, message=response)
    return jsonify(status=400, message=f'ID :{id} not found.')

@app.route('/update', methods=['POST', 'PATCH'])
def update():
    data = request.get_json()
    id = str(request.args.get('id'))
    try :
        response = ddb.update_evaluation(id, data)
        return jsonify(status=200, message=response)
    except:
        return jsonify(status=400, message=f'ID :{id} not found.')
    
if __name__ == '__main__':
    app.run()