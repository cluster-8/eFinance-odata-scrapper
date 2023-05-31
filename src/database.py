# -*- coding: utf-8 -*-
from .db import *
import logging

# * DATABASE SOURCE
def get_financial_instituition_id_by_cnpj(instituition_cnpj: str):
    '''
    Returns Financial Instituition ID
    
    :param instituition_cnpj: str
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM instituicoes WHERE cnpj = '{instituition_cnpj}' OR cnpj_formatado = '{instituition_cnpj}'")
        res = cur.fetchall()
        cur.close()
        return res[0][0] 
    except Exception as e:
        logging.error('Get Financial Instituition Id by CNPJ error', exc_info=True)
        print(f"Get Financial Instituition Id by CNPJ error: {e}")

def get_service_id_by_code(service_code: str, service_tipo: str = None):
    query = f"SELECT * FROM servicos WHERE codigo = '{service_code}'"

    if (service_tipo):
        query = query + f" AND tipo = '{service_tipo}'"

    '''
    Returns Service ID from database
    
    :param service_code: str
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return res[0]
    except Exception as e:
        logging.error('Get Service ID by Code error', exc_info=True)
        print(f"Get Service ID by Code error: {e}")

def get_all_financial_instituitions():
    '''
    Returns the list of financial instituitions from database source.
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes")
        # cur.execute("SELECT * FROM instituicoes i INNER JOIN instituicao_grupo ig  ON ig.instituicao_id =i.id INNER JOIN grupos g ON g.id =ig.grupo_id ")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get All Database Financial Instituitions error', exc_info=True)
        print(f"Get All Database Financial Instituitions error: {e}")

def get_all_tariffs():
    '''
    Returns the list of all tariffs from database source.
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tarifas")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get All Tariffs from database source error', exc_info=True)
        print(f"Get All Tariffs from database source error: {e}")

def get_all_services():
    '''
    Returns the list of all services from database source.
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicos")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get All Services from database source error', exc_info=True)
        print(f"Get All Services from database source error: {e}")

def get_financial_instituition_by_cnpj(cnpj: str):
    '''
    Returns financial instituition by cnpj.
    
    :param cnpj: str
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj = %s", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get Financial Instituition by CNPJ', exc_info=True)
        print(f"Get Financial Instituition by CNPJ {e}")

def get_financial_instituition_by_cnpj8(cnpj8: str):
    '''
    Returns financial instituition by cnpj8.
    
    :param cnpj8: str
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj_formatado = %s", [cnpj8,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get Financial Instituition by CNPJ8', exc_info=True)
        print(f"Get Financial Instituition by CNPJ8 {e}")

def get_financial_instituitions_physical_person_tariffs(cnpj: str):
    '''
    Returns a list of all physical person services tariffs by Financial Instituition CNPJ
    
    :param cnpj: str 
    '''
    try:    
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes i INNER JOIN tarifas t ON t.instituicao_id =i.id INNER JOIN servicos s ON s.id =t.servico_id WHERE i.cnpj = %s AND s.tipo = 'F'", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get Financial Instituition Tariffs error', exc_info=True)
        print(f"Get Financial Instituition Tariffs error: {e}")

def get_financial_instituitions_legal_person_tariffs(cnpj: str):
    '''
    Returns a list of all legal person services tariffs by Financial Instituition CNPJ
    
    :param cnpj: str 
    '''
    try:    
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes i INNER JOIN tarifas t ON t.instituicao_id =i.id INNER JOIN servicos s ON s.id =t.servico_id WHERE i.cnpj = %s AND s.tipo = 'J'", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get Financial Instituition Tariffs error', exc_info=True)
        print(f"Get Financial Instituition Tariffs error: {e}")

def get_financial_instituitions_tariffs(cnpj: str):
    '''
    Returns a list of all tariffs by Financial Instituition CNPJ
    
    :param cnpj: str 
    '''
    try:    
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes i INNER JOIN tarifas t ON t.instituicao_id =i.id INNER JOIN servicos s ON s.id =t.servico_id WHERE i.cnpj = %s", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get Financial Instituition Tariffs error', exc_info=True)
        print(f"Get Financial Instituition Tariffs error: {e}")

def get_financial_instituition_groups(id: str):
    '''
    Returns all Consolidated groups of a given Financial Instituition by id.
    
    :param cnpj: str
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT g.codigo, g.nome FROM instituicoes i \
                    INNER JOIN instituicao_grupo ig  ON ig.instituicao_id = i.id \
                    INNER JOIN grupos g ON g.id = ig.grupo_id \
                    WHERE ig.instituicao_id = %s", [id,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get Financial Instituition Groups from database source error', exc_info=True)
        print(f"Get Financial Instituition Groups from database source error: {e}")

def get_all_consolidated_groups():
    '''
    Returns the list of all consolidated groups from database source.
    '''
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM grupos")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get All Consolidated Groups from database source error', exc_info=True)
        print(f"Get All Consolidated Groups from database source error: {e}")

def get_financial_instituitions_tariffs_by_id(id: str):
    '''
    Returns a list of all tariffs by Financial Instituition id
    
    :param id: str 
    '''
    try:    
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT ON (t.servico_id) t.servico_id, t.valor_maximo, s.tipo, s.nome, t.data_vigencia FROM (SELECT * FROM tarifas WHERE instituicao_id = %s ORDER BY data_vigencia desc) t inner join servicos s on s.id = t.servico_id", [id])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get Financial Instituition Tariffs error', exc_info=True)
        print(f"Get Financial Instituition Tariffs error: {e}")

def get_financial_instituitions_physical_person_services(cnpj: str):
    pass

def get_financial_instituitions_legal_person_services(cnpj: str):
    pass

def get_all_tariffs_by_cnpj_and_code(instituition_cnpj: str, service_code: str):
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT t.valor_maximo, t.data_vigencia, t.unidade, t.periodicidade, t.moeda, s.nome, s.codigo, s.tipo FROM tarifas t INNER JOIN servicos s ON s.id = t.servico_id INNER JOIN instituicoes i ON i.id = t.instituicao_id WHERE i.cnpj = %s AND s.codigo = %s ORDER BY t.data_vigencia ASC", [instituition_cnpj, service_code])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        logging.error('Get All Tariffs by CNPJ and Service Code error', exc_info=True)
        print(f'Get All Tariffs by CNPJ and Service Code error: {e}')
        
def get_all_tariffs_by_instituition_and_service(service_id: str, instituition_id: str):
    try:
        conn = get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT i.nome, s.nome, t.unidade, t.periodicidade, t.moeda, s.codigo, s.tipo, t.valor_maximo, t.created_at FROM tarifas t INNER JOIN servicos s ON s.id = t.servico_id INNER JOIN instituicoes i ON i.id = t.instituicao_id WHERE i.id = %s AND s.id = %s ORDER BY t.created_at ASC", [instituition_id, service_id])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f'Get All Tariffs by Instituition ID and Service ID error: {e}')