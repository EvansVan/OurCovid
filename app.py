import json
import os
import logging
import time

from flask import Flask, jsonify, request,Response,g
from src.estimator import estimator
from src.serializer import DataSerializer

from dicttoxml import dicttoxml
from marshmallow import ValidationError

from marshmallow import ValidationError

app = Flask(__name__)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def log_requests(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path == '/robots.txt':
        return response
    elif request.path.startswith('/static'):
        return response

    now = int(round(time.time() * 1000))
    duration = now - g.start_time
    if duration < 10 and duration > 0:
        duration = "0"+str(duration)
    method = request.method
    resp_code = response.status_code
    request_url = request.path

    with open("log.txt", "a+") as f:
        f.write(f"{method}\t{request_url}\t{resp_code}\t{duration}ms\n")
        f.close()
    return response

@app.route('/', methods=['GET'])
def index():
    return "<h2>Deployment Succeeded</h2>"

@app.route('/api/v1/on-covid-19', methods=['POST', 'GET'], endpoint='estimator')
@app.route('/api/v1/on-covid-19/json', methods=['POST', 'GET'], endpoint="estimator")
def estimate_effects():
    """Estimates the effect of COVID-19 based on the data passed."""
    if not request.json:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {}, "errors": {"general": "Json data required"}}), 400

    serializer = DataSerializer()
    try:
        data = serializer.load(request.get_json())
    except ValidationError as err:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {}, "errors": err.messages}), 400

    return Response(response=json.dumps(estimator(data)), status=200, content_type='application/json')

@app.route('/api/v1/on-covid-19/xml', methods=['POST', 'GET'], endpoint='estimator_xml')
def estimate_effects_xml():
    """Estimates the effects of COVID-19 and returns data in XML format."""
    if not request.json:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {},
                        "errors": {"general": "Json data required"}}), 400

    serializer = DataSerializer()
    try:
        data = serializer.load(request.get_json())
    except ValidationError as err:
        return jsonify({"data": request.get_json(), "impact": {}, "severImpact": {}, "errors": err.messages}), 400

    xml = dicttoxml(estimator(data))
    return Response(response=xml, status=200, mimetype='application/xml')

@app.route('/api/v1/on-covid-19/logs', methods=['GET'], endpoint='logs')
def get_logs():
    f = open("log.txt", "r").read()
    return Response(f, mimetype="text/plain")

if __name__ == "__main__":
    app.run()
