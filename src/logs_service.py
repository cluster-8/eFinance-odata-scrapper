import datetime
from .db import *

def get_logs(start_date, end_date):
    try:
        if not start_date and not end_date: return 'No start date and end date informed.'
        
        valid = validate_date(start_date) and validate_date(end_date)
        if not valid:
            return {
                "message": "Start date and end date must be informed in the following data format YYYY-MM-DD"
            }
        
        result = get_logs_by_date(start_date, end_date)
        parsed = parse_logs(result)
        
        return parsed
    except Exception as e:
        print(f'Get Logs Service error: {e}')
        
def get_logs_by_date(start_date, end_date):
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM logs WHERE date >= '{start_date}' AND date <= '{end_date}'")
        res = cur.fetchall()
        cur.close()
        return res 
    except Exception as e:
        print(f'Get Logs by Date Service error: {e}')
        
def parse_logs(logs):
    try:
        response = {}
        
        if not logs: 
            response['message'] = "No logs were found."
            return response
        
        parsed_logs = []
        for log in logs:
            parsed_logs.append({
                "id": log[0],
                "date": log[1],
                "type": log[2],
                "content": log[3],
                "createdAt": log[4]
            })
        
        response['data'] = parsed_logs
        return response
    except Exception as e:
        print(f'Parse Logs response error: {e}')
        
def validate_date(date):
    try:
        return datetime.date.fromisoformat(date)
    except Exception as e:
        print(f'Validate Date Error: {e}')        
        
        
