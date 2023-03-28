# -*- coding: utf-8 -*-
import requests
import datetime
import db

# * OLINDA SOURCE
def get_financial_instituitions():
    
    url = "https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$top=10000&$format=json&$select=Api,Versao,CnpjInstituicao,NomeInstituicao,NomeContato,EmailContato,Recurso,Argumento,Situacao,URLDados,URLConsulta"
        
    try:
        result = requests.get(url)
        return result.json()['value']
    except Exception as e:
        print("Erro na busca por Instituições Financeiras:", e)
 
# ? tarifas
# def get_physical_person_tariffs(if_cnpj):
    
#     pessoa = 'F'
#     cnpj = str(if_cnpj)[:8]
    
#     url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{pessoa}'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
    
#     try:
#         result = requests.get(url)
#         if len(result.json()['value']) > 0: 
#             return result.json()['value']
#     except Exception as e:
#         print("Erro ao buscar tarifas pessoa física por id:", e)
        
def get_juridical_person_tariffs(if_cnpj):
    
    pessoa = 'J'
    cnpj = str(if_cnpj)[:8]

    
    url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{pessoa}'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
    
    try:
        result = requests.get(url)
        if len(result.json()['value']) > 0:
            return result.json()['value']
    except Exception as e:
        print("Erro ao buscar tarifas pessoa jurídica por id:", e)

# ? grupo
def get_financial_groups():
    try:
        url = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/GruposConsolidados?%24format=json"
        response = requests.get(url)
        return response.json()['value']
    except Exception as e:
        print(f'Get Grupos Consolidados error: {e}')

# ? instituições
def get_financial_instituitions_by_group(grupo_codigo):
    try:
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaInstituicoesDeGrupoConsolidado(CodigoGrupoConsolidado=@CodigoGrupoConsolidado)?%40CodigoGrupoConsolidado={grupo_codigo}&%24format=json"
        response = requests.get(url)
        return response.json()['value']
    except Exception as e:
        print(f"Get IF Services error: {e}")
 
# * DATABASE SOURCE       
def get_financial_instituition_id_by_cnpj(cnpj):
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes WHERE cnpj = %s", [cnpj,])
        res = cur.fetchall()
        cur.close()
        return res[0][0] 
    except Exception as e:
        print(f"Get Instituição error: {e}")
        
def get_service_id_by_code(codigo):
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicos WHERE codigo = %s", [codigo,])
        res = cur.fetchall()
        cur.close()
        # print(res[0])
        return res[0]
    except Exception as e:
        print(f"Get Serviço error: {e}")
             
def get_all_financial_instituitions():
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Serviço error: {e}")
        
def get_all_tariffs():
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tarifas")
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(f"Get Tarifas error: {e}")

def get_tariff_by_code_and_date(cod, date):
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tarifas WHERE codigo = %s AND data_vigencia", [cod, date])
        res = cur.fetchall()
        cur.close()
        print(res[0][0])
        return res[0][0]
    except Exception as e:
        print(f"Get Tarifa error: {e}")
        
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

def get_financial_instituitions_tariffs(instituition_name):
    try:    
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM instituicoes i INNER JOIN tarifas t ON t.instituicao_id =i.id INNER JOIN servicos s ON s.id =t.servico_id WHERE i.nome = %s", [instituition_name,])
        res = cur.fetchall()
        cur.close()
        return res
    except Exception as e:
        print(e)

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

# ! ULTIMA: 90729369000122

def services_pf(cnpj):
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
        


