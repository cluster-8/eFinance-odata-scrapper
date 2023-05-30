from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import scrapper
import predict

app = Flask(__name__)
CORS(app)
 
@app.route('/run-scrapper', methods=['GET'])
def run_scrapper():
    try:
        result = scrapper.run_update_database()
        print("Result: ", result)
        return jsonify('Database updated successfully!', result)
    except Exception as e:
        print(f'Run Scrapper error: {e}')
        
@app.route('/predict-tariff', methods=['POST'])
def predict_tariff():
    try:
        data = request.get_json(force=True)
        service_id, instituition_id = data['serviceId'], data['instituitionId']
        result = predict.get_prediction(service_id, instituition_id)
        
        if "message" in result: return jsonify(result), 200
        
        return jsonify(result)
    
    except Exception as e:
        print(f'Predict Tariff error: {e}')
         
if __name__ == '__main__':
    app.run(debug=True)