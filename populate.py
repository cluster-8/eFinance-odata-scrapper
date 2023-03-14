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
        instituicoes = get_data.get_all_instituicoes()
        for i in instituicoes:
            cnpj = i[4]
            servicos = get_data.servicos_pf(cnpj)
            cods = []
            for i in servicos:
                codigo, nome, tipo = i['CodigoServico'], i['Servico'], "F"
                
                if codigo in cods: continue
                
                conn = db.get_database_psql()
                cur = conn.cursor()
                cur.execute("INSERT INTO servicos (codigo, nome, tipo) VALUES(%s, %s, %s)", (codigo, nome, tipo))
                conn.commit()
                cods.append(codigo)
                cur.close()
                conn.close()
                print(f"Inserindo serviço de pessoa física: {codigo} {nome}")
    except Exception as e:
        print(e)

def insert_servicos_pj():
    try:
        instituicoes = get_data.get_all_instituicoes()
        for i in instituicoes:
            cnpj = i[4]
            servicos = get_data.servicos_pj(cnpj)
            cods = []
            for i in servicos:
                codigo, nome, tipo = i['CodigoServico'], i['Servico'], "F"
                
                if codigo in cods: continue
                
                conn = db.get_database_psql()
                cur = conn.cursor()
                cur.execute("INSERT INTO servicos (codigo, nome, tipo) VALUES(%s, %s, %s)", (codigo, nome, tipo))
                conn.commit()
                cods.append(codigo)
                cur.close()
                conn.close()
                print(f"Inserindo serviço de pessoa física: {codigo} {nome}")
    except Exception as e:
        print(e)
        
def insert_instituicoes():
    try:
        instituicoes = get_data.instituicoes()
        cnpjs = []
        for i in instituicoes:
            nome, cnpj = i['NomeInstituicao'], str(i['CnpjInstituicao'])
            existe_no_banco = get_data.get_instituicao_by_cnpj(cnpj)
            if existe_no_banco: 
                print(f"Instituição já registrada no banco: CNPJ {cnpj}")
                continue
            ultimo_caractere = len(cnpj) - 1
            formatado = cnpj
            tarifas_pf = tarifas_pj = None
            print(formatado)
            while ultimo_caractere > 0 and (not tarifas_pf or not tarifas_pj):
                formatado = cnpj[:ultimo_caractere]
                ultimo_caractere = ultimo_caractere - 1
                tarifas_pf = get_data.tarifas_pf(formatado)
                tarifas_pj = get_data.tarifas_pj(formatado)
            
            if cnpj in cnpjs: continue
           
            try:
                if len(formatado) == 1: formatado = None
                conn = db.get_database_psql()
                cur = conn.cursor()
                cur.execute("INSERT INTO instituicoes (nome, cnpj, cnpj_formatado) VALUES(%s, %s, %s)", (nome, cnpj, formatado))

                conn.commit()
                cur.close()
                conn.close()
                cnpjs.append(cnpj)
                print(f"Inserindo Insituição: {nome} {cnpj}")
            except Exception as e:
                    print(e)
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