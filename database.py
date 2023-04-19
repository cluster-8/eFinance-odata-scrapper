# -*- coding: utf-8 -*-
import requests
import datetime
import db

# * DATABASE SOURCE       
# OK
def get_financial_instituition_id_by_cnpj(instituition_cnpj):
    '''
    Returns Financial Instituition ID
    
    :param instituition_cnpj: str
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj = %s OR cnpj_formatado = %s", [instituition_cnpj,])
        res = cur.fetchall()
        cur.close()
        return res[0][0] 
    except Exception as e:
        print(f"Get Financial Instituition Id by CNPJ error: {e}")

# OK        
def get_service_id_by_code(service_code):
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

# OK             
def get_all_financial_instituitions():
    '''
    Returns the list of financial instituitions from database source.
    '''
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get All Database Financial Instituitions error: {e}")

# OK      
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

# OK
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

def get_tariff_by_code_and_date(code, date):
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tarifas WHERE codigo = %s AND data_vigencia", [code, date])
        res = cur.fetchall()
        cur.close()
        print(res[0][0])
        return res[0][0]
    except Exception as e:
        print(f"Get Tariff by Code and Date from database source error: {e}")
        
def get_financial_instituition_by_cnpj(cnpj):
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj = %s", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Instituição error: {e}")

def get_all_apis():
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM apis")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get All APIs error: {e}")

def get_financial_instituitions_tariffs_by_id(id: str):
    '''
    Returns a list of all tariffs by Financial Instituition id
    
    :param id: str 
    '''
    try:    
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT ON (t.servico_id) t.servico_id, t.valor_maximo, s.tipo FROM (SELECT * FROM tarifas WHERE instituicao_id = %s ORDER BY data_vigencia desc) t inner join servicos s on s.id = t.servico_id", [id])
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
        if not cnpj: return
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='F'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
        
        response = requests.get(url)
        
        return response.json()['value']
    except Exception as e:
        print(f"Get Services PF error: {e}")
        
def services_pj(cnpj):
    try:
        if not cnpj: return 
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='J'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
        
        response = requests.get(url)
        
        return response.json()['value']
    except Exception as e:
        print(f"Get Services PF error: {e}")
        


