from flask import Flask, jsonify
import scrapper
import logging
import log
 
app = Flask(__name__)
 
@app.route('/run-scrapper', methods=['GET'])
def run_scrapper():
    try:
        scrapper.run_update_database()
        logging.info('Database updated successfully!')
        return jsonify('Database updated successfully!')
    except Exception as e:
        logging.error('Run Scrapper error', exc_info=True)
        print(f'Run Scrapper error: {e}')
        
@app.route('/predict-tariff', methods=['GET'])
def predict_tariff():
    try:
        logging.info('Predicting mock!')
        return jsonify("Predicting mock!")
    except Exception as e:
        logging.error('Predict Tariff error', exc_info=True)
        print(f'Predict Tariff error: {e}')
         
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)