import os
import json
from log import logging
from flask import Flask, request
from app import main


# Create app var from Flask package
server = Flask(__name__)
# Set path of current app dirname
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('app.py')

# Troubleshooting route
@server.route('/')
def home_route():
    response = { "message": "welcome to the remodel application" }
    res = server.response_class(response=json.dumps(response), status=200, mimetype='application/json')
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


# Webhook route
@server.route('/analyze', methods=['POST'])
def analyze_route():
    try:
        j = json.loads(request.data)
        property_analysis_data = main(j)
        res = server.response_class(response=json.dumps(property_analysis_data), status=200, mimetype='application/json')
        logger.info("Successfully analyzed property.")
    except Exception as e:
        res = server.response_class(response=json.dumps({'text': f'Error sending property assumptions. Error: {str(e)}'}), status=200, mimetype='application/json')
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res