# -*- coding: utf-8 -*-
import db

# * DATABASE SOURCE
def get_financial_instituition_id_by_cnpj(instituition_cnpj: str):
    '''
    Returns Financial Instituition ID
    
    :param instituition_cnpj: str
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj = %s", [instituition_cnpj,])
        res = cur.fetchall()
        cur.close()
        return res[0][0] 
    except Exception as e:
        print(f"Get Financial Instituition Id by CNPJ error: {e}")

def get_service_id_by_code(service_code: str):
    '''
    Returns Service ID from database
    
    :param service_code: str
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicos WHERE codigo = %s", [service_code,])
        res = cur.fetchall()
        cur.close()
        return res[0]
    except Exception as e:
        print(f"Get Service ID by Code error: {e}")
             
def get_all_financial_instituitions():
    '''
    Returns the list of financial instituitions from database source.
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes")
        # cur.execute("SELECT * FROM instituicoes i INNER JOIN instituicao_grupo ig  ON ig.instituicao_id =i.id INNER JOIN grupos g ON g.id =ig.grupo_id ")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get All Database Financial Instituitions error: {e}")

def get_all_tariffs():
    '''
    Returns the list of all tariffs from database source.
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tarifas")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get All Tariffs from database source error: {e}")

def get_all_services():
    '''
    Returns the list of all services from database source.
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicos")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get All Services from database source error: {e}")

def get_financial_instituition_by_cnpj(cnpj: str):
    '''
    Returns financial instituition by cnpj.
    
    :param cnpj: str
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj = %s", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Financial Instituition by CNPJ {e}")

def get_financial_instituition_by_cnpj8(cnpj8: str):
    '''
    Returns financial instituition by cnpj8.
    
    :param cnpj8: str
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj_formatado = %s", [cnpj8,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Financial Instituition by CNPJ8 {e}")

def get_financial_instituitions_physical_person_tariffs(cnpj: str):
    '''
    Returns a list of all physical person services tariffs by Financial Instituition CNPJ
    
    :param cnpj: str 
    '''
    try:    
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes i INNER JOIN tarifas t ON t.instituicao_id =i.id INNER JOIN servicos s ON s.id =t.servico_id WHERE i.cnpj = %s AND s.tipo = 'F'", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Financial Instituition Tariffs error: {e}")

def get_financial_instituitions_legal_person_tariffs(cnpj: str):
    '''
    Returns a list of all legal person services tariffs by Financial Instituition CNPJ
    
    :param cnpj: str 
    '''
    try:    
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes i INNER JOIN tarifas t ON t.instituicao_id =i.id INNER JOIN servicos s ON s.id =t.servico_id WHERE i.cnpj = %s AND s.tipo = 'J'", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Financial Instituition Tariffs error: {e}")

def get_financial_instituitions_tariffs(cnpj: str):
    '''
    Returns a list of all tariffs by Financial Instituition CNPJ
    
    :param cnpj: str 
    '''
    try:    
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes i INNER JOIN tarifas t ON t.instituicao_id =i.id INNER JOIN servicos s ON s.id =t.servico_id WHERE i.cnpj = %s", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Financial Instituition Tariffs error: {e}")

def get_all_consolidated_groups():
    '''
    Returns the list of all consolidated groups from database source.
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM grupos")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get All Consolidated Groups from database source error: {e}")

def get_financial_instituition_groups(id: str):
    '''
    Returns all Consolidated groups of a given Financial Instituition by id.
    
    :param cnpj: str
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT g.codigo, g.nome FROM instituicoes i \
                    INNER JOIN instituicao_grupo ig  ON ig.instituicao_id = i.id \
                    INNER JOIN grupos g ON g.id = ig.grupo_id \
                    WHERE ig.instituicao_id = %s", [id,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Financial Instituition Groups from database source error: {e}")

def get_financial_instituitions_physical_person_services(cnpj: str):
    pass

def get_financial_instituitions_legal_person_services(cnpj: str):
    pass