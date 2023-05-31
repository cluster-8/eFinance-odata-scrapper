import pickle
from .database import *
import codecs
import csv
from datetime import date

def build_json_response(tariffs: list, prediction):
    
    prediction_value = prediction.tail(1).values[0]
    today = date.today()
    
    values = [val[-2] for val in tariffs]
    dates = [val[-1] for val in tariffs]
    
    response = {
        "instituition": f"{tariffs[0][0]}",
        "service": f"{tariffs[0][1]}",
        "unity": f"{tariffs[0][2]}",
        "periodicity": f"{tariffs[0][3]}",
        "currency": f"{tariffs[0][4]}",
        "code": f"{tariffs[0][5]}",
        "type": f"{tariffs[0][6]}",
        "prediction": {
                "value": prediction_value,
                "date" : today,
            },
        "historic": {
            "values": values,
            "dates": dates,
        }
    }
     
    return response

def tariffs_to_csv(tariffs: list):
    with codecs.open('./models/DATA.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["Date","Close"]
        if not tariffs: return False
        writer.writerow(header)
        for tariff in tariffs:
            row = [tariff[-1].strftime('%Y-%m-%d'), tariff[-2]]
            writer.writerow(row)
    return True

def get_tariffs(service_id: str, instituition_id: str):
    try:
        result = get_all_tariffs_by_instituition_and_service(service_id, instituition_id)
        return result
    except Exception as e:
        print(f'Get Tariffs error: {e}')

def run_serializer():
    try:
        file = open(r'./models/serializer.py', 'r').read()
        return exec(file)
    except Exception as e:
        print(f'Run Serializer error: {e}')

def get_prediction(service_id, instituition_id):  
   try:
        # get data
        tariffs = get_tariffs(service_id, instituition_id)
       
       # generate csv
        csv_created = tariffs_to_csv(tariffs)
        if not csv_created:
            return {
                "message": "Não há tarifas para o serviço selecionado."
            }
       
       # serilizar model
        run_serializer()
        
        # load model
        model = pickle.load(open('./models/auto_arima.pkl','rb'))
        
        # get prediction
        prediction = model.predict(n_periods=2)
        
        # mount json response
        json_response = build_json_response(tariffs, prediction)
        
        # return json response
        return json_response
   except Exception as e:
       print(f'Get Prediction error: {e}')
    