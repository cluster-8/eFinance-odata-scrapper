import db
import json
import database
import olinda

# * POPULATE DATABASE      
def insert_servicos_pf():
    try:
        instituicoes = database.get_all_instituicoes()
        for i in instituicoes:
            cnpj = i[3]
            servicos = database.services_pf(cnpj)
            if not servicos:
                print(f'Nenhum serviço foi encontradao para a instituição de CNPJ {cnpj}')
                continue
            cods = []
            for i in servicos:
                codigo, nome, tipo = i['CodigoServico'], i['Servico'], "F"
                if codigo in cods: continue
                try: 
                    conn = db.get_database_psql()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO servicos (codigo, nome, tipo) VALUES(%s, %s, %s)", (codigo, nome, tipo))
                    conn.commit()
                    cods.append(codigo)
                    cur.close()
                    conn.close()
                    print(f"Inserindo serviço de pessoa física: {codigo} {nome}")
                except Exception as e:
                    print(f'Erro ao inserir serviço de pessoa física {codigo} {nome}: {e}')
    except Exception as e:
        print(e)

def insert_servicos_pj():
    try:
        instituicoes = database.get_all_instituicoes()
        for i in instituicoes:
            cnpj = i[3]
            servicos = database.services_pj(cnpj)
            if not servicos:
                print(f'Nenhum serviço foi encontradao para a instituição de CNPJ {cnpj}')
                continue
            cods = []
            for i in servicos:
                codigo, nome, tipo = i['CodigoServico'], i['Servico'], "J"
                if codigo in cods: continue
                try:
                    conn = db.get_database_psql()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO servicos (codigo, nome, tipo) VALUES(%s, %s, %s)", (codigo, nome, tipo))
                    conn.commit()
                    cods.append(codigo)
                    cur.close()
                    conn.close()
                    print(f"Inserindo serviço de pessoa jurídica: {codigo} {nome}")
                except Exception as e:
                    print(f'Erro ao inserir serviço de pessoa jurídica {codigo} {nome}: {e}')
    except Exception as e:
        print(e)
        
def insert_instituicoes():
    try:
        c = 1
        instituicoes = database.instituicoes()
        
        # data =  json_data = open('instituicoes-4.json')
        # instituicoes = json.load(data)
        
        if not instituicoes:
            print("Nenhuma instituição foi encontrada!")
            return 
        cnpjs = []
        aux = []
        for i in instituicoes:
        # for i in reversed(instituicoes):
            print(c)
            c+=1
            print(f'Instituição #{len(cnpjs)+1}/{len(instituicoes)-len(cnpjs)}')
            nome, cnpj = i['NomeInstituicao'], str(i['CnpjInstituicao'])
            
            # print(f'Instituição #{len(cnpjs)+1}/{len(instituicoes)-len(cnpjs)}')
            # nome, cnpj = i['nome'], str(i['cnpj'])
            
            
            if cnpj in cnpjs: continue
            cnpjs.append(cnpj)
            
            ##################################################################################### !
            # existe_no_banco = databaseget_instituicao_by_cnpj(cnpj)
            # if existe_no_banco: 
            #     print(f"Instituição já registrada no banco: CNPJ {cnpj}")
            #     continue
            ##################################################################################### ?
            ultimo_caractere = len(cnpj) - 1
            formatado = cnpj
            tarifas_pf = tarifas_pj = [0,0]
            print(formatado)
            while ultimo_caractere > 0 and (not tarifas_pf or not tarifas_pj):
                formatado = cnpj[:ultimo_caractere]
                ultimo_caractere = ultimo_caractere - 1
                tarifas_pf = database.tarifas_pf(formatado)
                tarifas_pj = database.tarifas_pj(formatado)
            
            formatado = cnpj[:8]
            tarifas_pf = database.tarifas_pf(formatado)
            tarifas_pj = database.tarifas_pj(formatado)
            
            ##################################################################################### !
            # tarifas_pf = databasetarifas_pf(cnpj)
            # tarifas_pj = databasetarifas_pj(cnpj)
            
            if not tarifas_pf or not tarifas_pj: continue
            
            # if cnpj in cnpjs: continue
           
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
        instituicoes = database.get_all_instituicoes()
        # all_tarifas = databaseget_all_tarifas()
        c = 0
        for i in instituicoes:
            c+=1
            print(f'#{c}/{len(instituicoes)} - Buscando tarifas para a instituição de CNPJ {i[2]}')
            instituicao_id = i[0]
            cnpj = i[3]
            tarifas_f = database.tarifas_pf(cnpj) 
            tarifas_j = database.tarifas_pj(cnpj)
            if not tarifas_j: tarifas_j = []
            if not tarifas_f: tarifas_f = []
            tarifas = [*tarifas_f, *tarifas_j]
            print(tarifas)
            if not tarifas: 
                print(f"There is no services for instituition CNPJ: {cnpj}")
                continue
            tarifas_inseridas = []
            for t in tarifas:
                
                codigo = t['CodigoServico']
                s = database.get_servico_id_by_codigo(codigo)
                service_id = s[0]
                service_type = s[3]
                                
                tarifa = {
                    "servico_id" : service_id,
                    "instituicao_id" : instituicao_id,
                    "valor_maximo" : t['ValorMaximo'],
                    "data_vigencia" : t['DataVigencia'],
                    "unidade" : t['Unidade'],
                    "periodicidade": t['Periodicidade'],
                    "moeda": t['TipoValor']
                }
                
                try:
                    conn = db.get_database_psql()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO tarifas (servico_id, instituicao_id, valor_maximo, data_vigencia, unidade, periodicidade, moeda) VALUES(%s, %s, %s, %s, %s, %s, %s)", (
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
                    # print(f'Erro ao inserir tarifa {service_type} {tarifa["servico_id"]} {tarifa["instituicao_id"]} {tarifa["valor_maximo"]} {tarifa["data_vigencia"]} {tarifa["unidade"]} {tarifa["periodicidade"]} {tarifa["moeda"]}: {e}')
                    print(e)
    except Exception as e:
        print(e)
        
def insert_financial_instituitions_apis():
    try:
        instituitions_apis = olinda.get_financial_instituitions_endpoints()
        db_apis = database.get_all_apis()
        for i in instituitions_apis:
            if i['Api'] != 'taxas_cartoes' and i['Recurso'] != '/': continue
            cnpj = i['CnpjInstituicao']
            instituition = database.get_financial_instituition_id_by_cnpj(cnpj)
            if not instituition: continue
            
            data = {
                "apiTipo": i["Api"],
                "versao": i["Versao"],
                "recurso": i["Recurso"],
                "argumento": i["Argumento"],
                "situacao": i["Situacao"],
                "url_dados": i["URLDados"],
                "instituicao_id": instituition
            }
            
            try:
                print(data)
                # conn = db.get_database_psql()
                # cur = conn.cursor()
                # cur.execute("INSERT INTO apis (api_tipo, versao, recurso, argumento, situacao, url_dados, instituicao_id) VALUES(%s, %s, %s, %s, %s, %s, %s)", (
                #     i['Api'],
                #     i['Versao'], 
                #     i['Recurso'], 
                #     i['Argumento'], 
                #     i['Situacao'], 
                #     i['URLDados'], 
                #     instituition))
                # conn.commit()
                # # tarifas_inseridas.append(tarifa)
                # print(f'Financial Instituition API endpoint inserted successfully')
                # cur.close()
                # conn.close()
                
            except Exception as e:
                print(f"Insert Financial Instituitions APIs endpoints error: {e}")
            print(cnpj)
            print(instituition)
            print(data)
            return 
    except Exception as e:
        print(e)

# refatorando
def insert_financial_instituitions():
    '''
    Insert Financial Instituitions on database if it not exists.
    '''
    try:
        olinda_instituitions = olinda.get_financial_instituitions()
        db_instituitions = database.get_all_financial_instituitions()
        
        if len(olinda_instituitions) > len(db_instituitions):
            for i in olinda_instituitions:
                if i['CnpjInstituicao'] not in str(db_instituitions):
                    try:
                        nome, cnpj, cnpj8 = i['NomeInstituicao'], i['CnpjInstituicao'], i['CnpjInstituicao'][:8]
                        conn = db.get_database_psql()
                        cur = conn.cursor()
                        cur.execute("INSERT INTO instituicoes (nome, cnpj, cnpj_formatado) VALUES(%s, %s, %s)", (nome, cnpj, cnpj8))
                        conn.commit()
                        cur.close()
                        conn.close()
                        print(f"Inserting Financial Instituition: {nome} {cnpj}")
                    except Exception as e:
                        print(f"Insert Financial Instituition {nome} {cnpj} on database error: {e}")
        else: print("There is no new Financial Instituitions to be inserted on database.")
    except Exception as e:
        print("Insert Financial Instituitions error:", e)
        
def insert_physical_person_services():
    '''
    Insert Physical Person Services on database if it not exists.
    '''
    try:
        instituitions = database.get_all_financial_instituitions()
        unidades = []
        periodicidades = []
        for i in instituitions:
            cnpj = i[3]
            services = database.services_pf(cnpj)
            if not services:
                print(f'There is no Physical Person Services found for Financial Instituition {i[2]} {cnpj}')
                continue
            inserted_services_codes = []
            for i in services:                
                code, name, service_type = i['CodigoServico'], i['Servico'], "F"
                if code in inserted_services_codes: continue
                try: 
                    conn = db.get_database_psql()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO servicos (codigo, nome, tipo) VALUES(%s, %s, %s)", (code, name, service_type))
                    conn.commit()
                    inserted_services_codes.append(code)
                    cur.close()
                    conn.close()
                    print(f"Inserting Physical Person Service: {code} {name}")
                except Exception as e:
                    print(f'Erro ao inserir serviço de pessoa física {code} {name}: {e}')
    except Exception as e:
        print(e)