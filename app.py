from flask import Flask, jsonify
import scrapper
 
app = Flask(__name__)
 
@app.route('/run-scrapper', methods=['GET'])
def run_scrapper():
    try:
        scrapper.run_update_database()
        return jsonify('Database updated successfully!')
    except Exception as e:
        print(f'Run Scrapper error: {e}')
        
@app.route('/predict-tariff', methods=['GET'])
def predict_tariff():
    try:
        return jsonify("Predicting mock!")
    except Exception as e:
        print(f'Predict Tariff error: {e}')
         
if __name__ == '__main__':
    app.run(debug=True)