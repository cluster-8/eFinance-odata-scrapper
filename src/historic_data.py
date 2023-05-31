from .database import *
from datetime import datetime

CURRENT_DAY = datetime.now().day
CURRENT_MONTH = datetime.now().month
CURRENT_YEAR = datetime.now().year

def get_mock_dates():
    dates = []
    year_range = 3 # range of previous years to generate dates
    year = CURRENT_YEAR - 1 * year_range
    
    for i in range(12 * year_range + 1):
        month = CURRENT_MONTH + i
        if month > 12: 
            month = month % 12
            if month == 0: month = 12
            if month == 1: year += 1
            
        dates.append(f'{year}-{month}-{CURRENT_DAY}')
    
    return dates

def generate_serie(financial_instituition_cnpj):
    try:
        
        tariffs = database.get_financial_instituitions_tariffs(financial_instituition_cnpj)
        historic_series = []
        # tariffs = [tariffs[0]]
        for t in tariffs:
            print("\nServiço: ", t[16])
            print("Código: ", t[17])
            print("Valor vigente: ", t[8])
            print("Data de vigência: ", t[9])
            
            mock_dates = get_mock_dates()
            service_name = t[16]
            data = {
                "service_name": service_name,
                "vigent_date": t[9],
                "service_id": t[17],
                "service_type": t[18],
                "historic_values": []
            }
            
            for tar in tariffs:
                
                if tar[16] == service_name:
                    print("Entrei...")
                    vigent_date = tar[9] 
                    date_str = str(vigent_date)[:7]
                    for md in mock_dates:
                        # caso em que o ano e mes são iguais
                        if str(md)[:7] == date_str:
                            data['historic_values'].append([md, tar[8]])
                        else:
                            val = None
                            md_year = str(md)[:4]
                            md_month = str(md)[5:7]
                            date_year = str(vigent_date)[:4]
                            date_month = str(vigent_date)[5:7]
                            
                            if md_year >= date_year and md_month > date_month:
                                 val = tar[8]
                                 
                            data['historic_values'].append([md, val])        
                    # print(data)
            historic_series.append(data)  # nivel de tarifas
        return historic_series
    except Exception as e:
        print(f'Historic Data Generate Series error: {e}')
        
        
def generate_series():
    try:
        instituitions = database.get_all_financial_instituitions()
        services = database.get_all_services()
        for instituition in instituitions:
            name, cnpj = instituition[1], instituition[2]
            
            cnpj = '60746948000112' # ! para teste
            
            for service in services:
                
                # * isso pode ser transformado em uma função
                code = service[2]
                tariffs = database.get_all_tariffs_by_cnpj_and_code(cnpj, code)
                
                
                if len(tariffs) == 0: continue
                
                # ? caso em que há mais de uma tarifa para o serviço
                elif len(tariffs) > 1:

                    result = generate_tariffs_series(tariffs)
                    return result
                
                # ? caso em que há apenas uma tarifa para o serviço
                else:
                    pass 
                
                
                    
            break # ! para não fazer tudo agora
            
    except Exception as e:
        print(f'Generate Historic Series error: {e}')

def generate_tariffs_series(tariffs: list):
    try:
        mock_dates = get_mock_dates()
        
        # * mais de uma tarifa para o serviço
        if len(tariffs) > 1:
            aux = []
            
            # * percorrendo tarifas
            for t in tariffs:
                year, month, val = t[1].year, t[1].month, t[0]
                
                # * percorrendo datas mock
                for md in mock_dates:
                    date = datetime.strptime(md, '%Y-%m-%d').date()
                    m_year, m_month = date.year, date.month
                    
                    # * ...
                    data = [None, None]
                    if m_year == year and m_month == month:
                        data = [md, val]
                    elif m_year == year:
                        if m_month >= month:
                            data = [md, val]
                        else:
                            data = [md, None]
                    elif m_year > year:
                        if not data[0]:
                            data = [md, val]
                    else:
                        data = [md, None]
                    aux.append(data)
            
            current_val = None          
            for item in aux:
                val = item[1]
                if val:
                    current_val = val
                else:
                    item[1] = current_val
                
            aux.reverse()
            aux = aux[:37]
            # print("AUX", aux)
            result = aux.reverse()
            # return aux.reverse()
            return result
        
        # * uma tarifa para o serviço
        # todo: continuar...
        else:
            pass
    except Exception as e:
        print(f'Generate Tariffs Series error: {e}')