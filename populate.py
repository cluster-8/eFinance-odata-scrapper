import db
import json
import get_data
import olinda

# * POPULATE DATABASE      
def insert_servicos_pf():
    try:
        instituicoes = get_data.get_all_instituicoes()
        for i in instituicoes:
            cnpj = i[3]
            servicos = get_data.services_pf(cnpj)
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
        instituicoes = get_data.get_all_instituicoes()
        for i in instituicoes:
            cnpj = i[3]
            servicos = get_data.services_pj(cnpj)
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
        instituicoes = get_data.instituicoes()
        
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
            # existe_no_banco = get_data.get_instituicao_by_cnpj(cnpj)
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
                tarifas_pf = get_data.tarifas_pf(formatado)
                tarifas_pj = get_data.tarifas_pj(formatado)
            
            formatado = cnpj[:8]
            tarifas_pf = get_data.tarifas_pf(formatado)
            tarifas_pj = get_data.tarifas_pj(formatado)
            
            ##################################################################################### !
            # tarifas_pf = get_data.tarifas_pf(cnpj)
            # tarifas_pj = get_data.tarifas_pj(cnpj)
            
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
        instituicoes = get_data.get_all_instituicoes()
        # all_tarifas = get_data.get_all_tarifas()
        c = 0
        for i in instituicoes:
            c+=1
            print(f'#{c}/{len(instituicoes)} - Buscando tarifas para a instituição de CNPJ {i[2]}')
            instituicao_id = i[0]
            cnpj = i[3]
            tarifas_f = get_data.tarifas_pf(cnpj) 
            tarifas_j = get_data.tarifas_pj(cnpj)
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
                s = get_data.get_servico_id_by_codigo(codigo)
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
        db_apis = get_data.get_all_apis()
        for i in instituitions_apis:
            if i['Api'] != 'taxas_cartoes' and i['Recurso'] != '/': continue
            cnpj = i['CnpjInstituicao']
            instituition = get_data.get_financial_instituition_id_by_cnpj(cnpj)
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
         