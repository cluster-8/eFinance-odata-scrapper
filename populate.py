import db
import database
import olinda
import logging
from datetime import datetime

# * POPULATE DATABASE
# refatorando
def insert_financial_instituitions():
    '''
    Insert Financial Instituitions on database if it not exists.
    '''
    try:
        olinda_instituitions = olinda.get_financial_instituitions()
        db_instituitions = database.get_all_financial_instituitions()
        
        db_instituitions = 0 if db_instituitions == None else len(db_instituitions)
        print(db_instituitions)
        if (len(olinda_instituitions) > db_instituitions):
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
                        logging.info(f"Inserting Financial Instituition {nome} {cnpj} on database", exc_info=True)
                        print(f"Inserting Financial Instituition: {nome} {cnpj}")
                    except Exception as e:
                        print(f"Insert Financial Instituition {nome} {cnpj} on database error: {e}")
        else: print("There is no new Financial Instituitions to be inserted on database.")
    except Exception as e:
        logging.error("Insert Financial Instituitions error", exc_info=True)
        print("Insert Financial Instituitions error:", e)
        
def insert_physical_person_services():
    '''
    Insert Physical Person Services on database if it not exists.
    '''
    try:
        instituitions = database.get_all_financial_instituitions()
        for i in instituitions:
            cnpj = i[3]
            # services = database.services_pf(cnpj)
            services = olinda.get_physical_person_tariffs(cnpj)
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
                    logging.info(f"Inserting Physical Person Service: {code} {name}", exc_info=True)
                    print(f"Inserting Physical Person Service: {code} {name}")
                except Exception as e:
                    print(f'Insert Physical Person Service {code} {name} error: {e}')
    except Exception as e:
        logging.error('Insert Physical Person Services error', exc_info=True)
        print(f"Insert Physical Person Services error: {e}")
        
def insert_juridical_person_services():
    '''
    Insert Legal Juridical Services on database if it not exists.
    '''
    try:
        instituitions = database.get_all_financial_instituitions()
        for i in instituitions:
            cnpj = i[3]
            # services = database.services_pf(cnpj)
            services = olinda.get_juridical_person_tariffs(cnpj)
            if not services:
                print(f'There is no Juridical Person Services found for Financial Instituition {i[2]} {cnpj}')
                continue
            inserted_services_codes = []
            for i in services:                
                code, name, service_type = i['CodigoServico'], i['Servico'], "J"
                if code in inserted_services_codes: continue
                try: 
                    conn = db.get_database_psql()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO servicos (codigo, nome, tipo) VALUES(%s, %s, %s)", (code, name, service_type))
                    conn.commit()
                    inserted_services_codes.append(code)
                    cur.close()
                    conn.close()
                    print(f"Inserting Juridical Person Service: {code} {name}")
                    logging.info(f'Inserting Juridical Person Service {code} {name}', exc_info=True)
                except Exception as e:
                    print(f'Insert Juridical Person Service {code} {name} error: {e}')
    except Exception as e:
        logging.error('Insert Juridical Person Services error', exc_info=True)
        print(f"Insert Juridical Person Services error: {e}")
        
def insert_consolidated_groups():
    '''
    Insert all consolidated groups from Olinda Source.
    '''
    try:
        database_groups = database.get_all_consolidated_groups()
        if not database_groups:
            print("No consolidated groups from Olinda Source were found!")
            return
        
        olinda_groups = olinda.get_consolidated_groups()
        if not olinda_groups:
            print("No consolidated groups from Olinda Source were found!")
            return
       
        for group in olinda_groups:
            try:
                conn = db.get_database_psql()
                cur = conn.cursor()
                cur.execute("INSERT INTO grupos (codigo, nome) VALUES(%s, %s)", (
                    group['Codigo'],
                    group['Nome']))
                conn.commit()
                logging.info(f"Insert Consolidated Group {group['Codigo']} {group['Nome']}", exc_info=True)
                print(f'Insert Consolidated Group: ', group['Codigo'], group['Nome'])
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Insert Consolidated Group: {e}")
    except Exception as e:
        logging.error('Insert Consolidated Groups error', exc_info=True)
        print(f"Insert Consolidated Groups error: {e}")

def insert_financial_instituition_groups():
    '''
    Insert Financial Instituitions Groups from Olinda Source.
    '''
    try:
        groups = database.get_all_consolidated_groups()
        for group in groups:
            group_code = group[2]
            instituitions = olinda.get_financial_instituitions_by_group(group_code)
            if not instituitions:
                print(f"No Financial Instituitions were found for consolidated group", code)
                continue
            
            for instituition in instituitions:
                inst_on_database = database.get_financial_instituition_by_cnpj8(instituition['Cnpj'])
                if not inst_on_database:
                    print(f"No Financial Instituition was found on database for CNPJ8: {i['Cnpj']}")
                    continue
                
                inst_id = inst_on_database[0][0]
                group_id = group[0]
                
                try:
                    conn = db.get_database_psql()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO instituicao_grupo (instituicao_id, grupo_id) VALUES(%s, %s)", (inst_id, group_id))
                    conn.commit()
                    logging.info(f"Insert Instituition Group {inst_on_database[0][1]} {inst_on_database[0][2]} {group[1]}", exc_info=True)
                    print(f"Insert Instituition Group {inst_on_database[0][1]} {inst_on_database[0][2]} {group[1]}")
                    cur.close()
                    conn.close()
                except Exception as e:
                    print(f"Update Financial Instituition Group error: {e}")            
    except Exception as e:
        logging.error('Update Financial Instituition Groups error', exc_info=True)
        print(f"Update Financial Instituition Groups error: {e}")

def insert_financial_instituition_tariffs(instituition: tuple, groups: list):
    '''
    Insert all tariffs of a given Financial Instituition by CNPJ.
    
    :param instituition: tuple
    :param groups: list
    '''
    try:
        print("Gettings Financial Instituition tariffs...")
        instituition_id = instituition[0]
        cnpj = str(instituition[2])

        # get physical person services tariffs
        physical_person_tariffs = olinda.get_physical_person_tariffs(cnpj)
        
        # insert physical person services tariffs
        print("Inserting physical person services tariffs...")
        insert_tariffs(instituition_id, physical_person_tariffs, groups, "F")
        
        # get juridical person services tariffs
        juridical_person_tariffs = olinda.get_juridical_person_tariffs(cnpj)
        
        # insert physical person services tariffs
        print("Inserting juridical person services tariffs...")
        insert_tariffs(instituition_id, juridical_person_tariffs, groups, "J")
        
    except Exception as e:
        logging.error('Insert Financial Instituition Tariffs error', exc_info=True)
        print(f"Insert Financial Instituition Tariffs error: {e}")
        
def insert_tariffs(instituition_id: str, tariffs: list, groups: list, service_type: str):
    '''
    Insert all tariffs of a given Financial Instituition.
    
    :param instituition_id: str
    :param tariffs: list
    :param groups: list
    :param service_type: str
    '''
    try:
        if not tariffs: return
        all_values = []
        for g in groups:
            group_code = g[0]
            values = olinda.get_all_services_values_by_group(service_type, group_code)
            all_values = [*all_values, *values]
        
        for tariff in tariffs:
            service_name = tariff['Servico']
            service_values = [v['ValorMinimo'] for v in all_values if v['NomeServico'] == service_name]
            code = tariff['CodigoServico']
            service_id = database.get_service_id_by_code(code)[0]
            min_value = min(service_values) if service_values else None
            
            t = {
                "servico_id" : service_id,
                "instituicao_id" : instituition_id,
                "valor_maximo" : tariff['ValorMaximo'],
                "valor_minimo": min_value,
                "data_vigencia" : tariff['DataVigencia'],
                "unidade" : tariff['Unidade'],
                "periodicidade": tariff['Periodicidade'],
                "moeda": tariff['TipoValor']
                }
            
            try:
                conn = db.get_database_psql()
                cur = conn.cursor()
                cur.execute("INSERT INTO tarifas (servico_id, instituicao_id, valor_maximo, valor_minimo, data_vigencia, unidade, periodicidade, moeda) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (
                    t['servico_id'],
                    t['instituicao_id'], 
                    t['valor_maximo'], 
                    t['valor_minimo'],
                    t['data_vigencia'], 
                    t['unidade'], 
                    t['periodicidade'], 
                    t['moeda']))
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Insert Financial Insitituition Tariff error: {e}")
    except Exception as e:
        logging.error('Insert All Tariffs error', exc_info=True)
        print(f"Insert All Tariffs error: {e}")

def insert_tariff(instituition_id: str, service_id: str, tariff, createdAt: str):
    '''
    Insert one tariff of a given Financial Instituition.
    
    :param instituition_id: str
    :param service_id: str
    :param tariffs
    :param dataVigencia: str
    '''
    try:
        t = {
            "servico_id" : service_id,
            "instituicao_id" : instituition_id,
            "valor_maximo" : float(tariff[5].replace(',', '')),
            "data_vigencia" : datetime.strptime(tariff[4], '%d/%m/%Y'),
            "unidade" : tariff[8],
            "periodicidade": tariff[9],
            "moeda": tariff[6],
            "created_at": datetime.strptime(createdAt, '%d/%m/%Y')
            }

        try:
            conn = db.get_database_psql()
            cur = conn.cursor()
            cur.execute("INSERT INTO tarifas (servico_id, instituicao_id, valor_maximo, data_vigencia, unidade, periodicidade, moeda, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (
                t['servico_id'],
                t['instituicao_id'], 
                t['valor_maximo'], 
                t['data_vigencia'], 
                t['unidade'], 
                t['periodicidade'], 
                t['moeda'],
                t['created_at']))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Insert Financial Insitituition Tariff error: {e}")
    except Exception as e:
        print(f"Insert Tariff error: {e}")
