from flask import Flask, jsonify, request
from flask_cors import CORS

import  logging

from src.scrapper import * 
from src.predict import *
from src.logs_service import *
from src.populate_historic import *

app = Flask(__name__)
CORS(app)

@app.route('/run-scrapper', methods=['GET'])
def run_scrapper():
    try:
        run_update_database()
        logging.info('Database updated successfully!')
        return jsonify('"message": "Database updated successfully!"')
    
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
        
@app.route('/logs', methods=['GET'])
def logs():
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        response = get_logs(start, end)
        return jsonify(response)
    except Exception as e:
        print(f'Logs error: {e}')
        return jsonify(f'"error": "{e}"')

@app.route('/populate-historic', methods=['GET'])
def run_populate_historic():
    try:
        populate_tariffs_historic()
        logging.info('Database updated with historic data successfully!')
        return jsonify('"message": "Database updated with historic data successfully!"')
    
    except Exception as e:
        logging.error('Populate Historic error', exc_info=True)
        print(f'Populate Historic error: {e}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)