import db
import json

# inserindo serviços
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
        
        
def insert_servicos_pf():
    try:
        file = open('services-2.json')
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
        file = open('services-pj-2.json')
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
        file = open('instituicoes-2.json')
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