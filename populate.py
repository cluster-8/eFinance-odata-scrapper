import db
import json

def execute_query(query):
    
    # query = f'''
    # select * from gc_grupo;
    # '''
    
    try:
        cur = db.get_database_psql()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        print(res)
        return res
    except Exception as e:
        print(e)

# * POPULATE DATABASE      
def insert_servicos_pf():
    try:
        file = open('./json/services-2.json')
        data = json.load(file)
        cods = []
        for i in data:
            codigo, nome, tipo = i['codigo'], i['nome'], "F"
            
            if codigo in cods: continue
            
            conn = db.get_database_psql()
            cur = conn.cursor()
            cur.execute("INSERT INTO sp_servico (sp_codigo, sp_nome, sp_tipo) VALUES(%s, %s, %s)", (codigo, nome, tipo))
            conn.commit()
            cods.append(codigo)
            cur.close()
            conn.close()
    except Exception as e:
        print(e)

def insert_servicos_pj():
    try:
        file = open('./json/services-pj-2.json')
        data = json.load(file)
        cods = []
        for i in data:
            codigo, nome, tipo = i['codigo'], i['nome'], "J"
            if codigo in cods: continue
            conn = db.get_database_psql()
            cur = conn.cursor()
            cur.execute("INSERT INTO sp_servico (sp_codigo, sp_nome, sp_tipo) VALUES(%s, %s, %s)", (codigo, nome, tipo))
            conn.commit()
            cods.append(codigo)
            cur.close()
            conn.close()
    except Exception as e:
        print(e)
        
def insert_instituicoes():
    try:
        file = open('./json/instituicoes-2.json')
        data = json.load(file)
        cnpjs = []
        for i in data:
            nome, cnpj, formatado = i['nome'], i['cnpj'], i['cnpj_formatado']
            
            if cnpj in cnpjs: continue
            
            conn = db.get_database_psql()
            cur = conn.cursor()
            cur.execute("INSERT INTO if_instituicao (if_nome, if_cnpj, if_cnpj_formatado) VALUES(%s, %s, %s)", (nome, cnpj, formatado))
            conn.commit()
            cur.close()
            conn.close()
            cnpjs.append(cnpj)
    except Exception as e:
        print(e)
        
def insert_tarifas_pf():
    try:
        file = open('./json/tarifas-pf.json')
        data = json.load(file)
        tarifas_inseridas = []
        for i in data:
            
            tarifa = {
                "servico_id" : i['servico_id'],
                "instituicao_id" : i['instituicao_id'],
                "valor_maximo" : i['valor_maximo'],
                "data_vigencia" : i['data_vigencia'],
                "unidade" : i['unidade'],
                "periodicidade" : i['periodicidade'],
                "moeda" : i['moeda']
            }
            
            
            if tarifa in tarifas_inseridas: continue
            
            # servico_id = tarifa['servico_id']
            # instituicao_id = tarifa['instituicao_id']
            # valor_maximo = tarifa['valor_maximo']
            # data_vigencia = tarifa['data_vigencia']
            # unidade = tarifa['unidade']
            # periodicidade = tarifa['periodicidade']
            # moeda = tarifa['moeda']
            
            conn = db.get_database_psql()
            cur = conn.cursor()
            cur.execute("INSERT INTO ts_tarifa (ts_servico_id, ts_instituicao_id, ts_valor_maximo, ts_data_vigencia, ts_unidade, ts_periodicidade, ts_moeda) VALUES(%s, %s, %s, %s, %s, %s, %s)", (
                tarifa['servico_id'],
                tarifa['instituicao_id'], 
                tarifa['valor_maximo'], 
                tarifa['data_vigencia'], 
                tarifa['unidade'], 
                tarifa['periodicidade'], 
                tarifa['moeda']))
            conn.commit()
            tarifas_inseridas.append(tarifa)
            cur.close()
            conn.close()
    except Exception as e:
        print(e)