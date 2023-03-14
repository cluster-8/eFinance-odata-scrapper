import db
import json
import get_data

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
        
def insert_tarifas():
    try:
        instituicoes = get_data.get_all_instituicoes()
        for i in instituicoes:
            instituicao_id = i[0]
            cnpj = i[4]
            tarifas_f = get_data.tarifas_pf(cnpj) 
            tarifas_j = get_data.tarifas_pj(cnpj)
            print('passei')
            if not tarifas_j: tarifas_j = []
            if not tarifas_f: tarifas_f = []
            tarifas = [*tarifas_f, *tarifas_j]
            if not tarifas: 
                print(f"There is no services for instituition CNPJ: {cnpj}")
                continue
            tarifas_inseridas = []
            for t in tarifas:
                codigo = t['CodigoServico']
                s = get_data.get_servico_id_by_codigo(codigo)
                service_id = s[0]
                
                tarifa = {
                    "servico_id" : service_id,
                    "instituicao_id" : instituicao_id,
                    "valor_maximo" : t['ValorMaximo'],
                    "data_vigencia" : t['DataVigencia'],
                    "unidade" : t['Unidade'],
                    "periodicidade": t['Periodicidade'],
                    "moeda": t['TipoValor']
                }
                
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
                print(f'Tarifa inserida:',tarifa['instituicao_id'],tarifa['servico_id'],tarifa['data_vigencia'])
                cur.close()
                conn.close()
                
    except Exception as e:
        print(e)