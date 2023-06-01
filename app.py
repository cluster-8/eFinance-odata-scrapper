from flask import Flask, jsonify, request
from flask_cors import CORS

import  logging

from src.scrapper import * 
from src.predict import *

app = Flask(__name__)
CORS(app)

@app.route('/run-scrapper', methods=['GET'])
def run_scrapper():
    try:
        run_update_database()
        logging.info('Database updated successfully!')
        return jsonify('Database updated successfully!')
    
    except Exception as e:
        logging.error('Run Scrapper error', exc_info=True)
        print(f'Run Scrapper error: {e}')
        
@app.route('/predict-tariff', methods=['POST'])
def predict_tariff():
    try:
        logging.info('Predicting tariff!')
        data = request.get_json(force=True)
        service_id, instituition_id = data['serviceId'], data['instituitionId']
        result = get_prediction(service_id, instituition_id)
        if "message" in result: return jsonify(result), 200
        
        return jsonify(result)
    
    except Exception as e:
        logging.error('Predict Tariff error', exc_info=True)
        print(f'Predict Tariff error: {e}')
        
@app.route('/', methods=['GET'])
def hello():
    return jsonify('Hello World')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)