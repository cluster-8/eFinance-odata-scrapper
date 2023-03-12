# -*- coding: utf-8 -*-
import requests
import datetime
import db

# * OLINDA SOURCE
def instituicoes():
    
    url = "https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$top=10000&$format=json&$select=Api,Versao,CnpjInstituicao,NomeInstituicao,NomeContato,EmailContato,Recurso,Argumento,Situacao,URLDados,URLConsulta"
    
    try:
        result = requests.get(url)
        return result.json()['value']
    except Exception as e:
        print("Erro na busca por Instituições Financeiras:", e)
 
def tarifas_pf(if_cnpj):
    
    pessoa = 'F'
    # cnpj = if_cnpj[:9]
    cnpj = str(if_cnpj)[:8]
    # cnpj = str(if_cnpj)
    
    url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{pessoa}'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
    
    try:

        result = requests.get(url)
        if len(result.json()['value']) > 0: 
            # print(result.json())
            return result.json()['value']
        
    except Exception as e:
        print("Erro ao buscar tarifas por id:", e)

def grupos():
    try:
        url = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/GruposConsolidados?%24format=json"
        response = requests.get(url)
        return response.json()['value']
    except Exception as e:
        print(f'Get Grupos Consolidados error: {e}')

def servicos_pf(if_cnpj):
    try:
        last = len(str(if_cnpj))
        response_status = None
        value = []
        if not value: 
            print(f'{datetime.datetime.now()} - "value" inválido.')
            # return
        while len(value) == 0 and last > 0:
            pessoa = "F"
            cnpj = str(if_cnpj)[:last]
            # print(cnpj)
            url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{pessoa}'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
            response = requests.get(url)
            response_status = response.status_code
            if response_status == 200:
                value = response.json()['value']
                # print(len(value))
            # print(cnpj)
            last -= 1
        return response.json()['value']
    except Exception as e:
        print(f"Get IF Services error: {e}")
        
def servicos_pj(if_cnpj):
    try:
        last = len(str(if_cnpj))
        response_status = None
        value = []
        if not value: 
            print(f'{datetime.datetime.now()} - "value" inválido.')
            # return
        while len(value) == 0 and last > 0:
            pessoa = "J"
            cnpj = str(if_cnpj)[:last]
            # print(cnpj)
            url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{pessoa}'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
            response = requests.get(url)
            response_status = response.status_code
            if response_status == 200:
                value = response.json()['value']
                # print(len(value))
            # print(cnpj)
            last -= 1
        return response.json()['value']
    except Exception as e:
        print(f"Get IF Services error: {e}")

def get_instituicoes_by_grupo(grupo_codigo):
    try:
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaInstituicoesDeGrupoConsolidado(CodigoGrupoConsolidado=@CodigoGrupoConsolidado)?%40CodigoGrupoConsolidado={grupo_codigo}&%24format=json"
        response = requests.get(url)
        print(response)
        return response.json()['value']
    except Exception as e:
        print(f"Get IF Services error: {e}")
 
# * DATABASE SOURCE       
def get_instituicao_id_by_cnpj(cnpj):
    try:
        
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM if_instituicao WHERE if_cnpj = %s", [cnpj,])
        res = cur.fetchall()
        cur.close()
        print(res[0][0])
        return res[0][0]
        
    except Exception as e:
        print(f"Get Instituição error: {e}")
        
def get_servico_id_by_codigo(codigo):
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sp_servico WHERE sp_codigo = %s", [codigo,])
        res = cur.fetchall()
        cur.close()
        # print(res[0])
        return res[0]
    except Exception as e:
        print(f"Get Serviço error: {e}")
             
def get_all_instituicoes():
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute("SELECT * FROM if_instituicao")
        res = cur.fetchall()
        cur.close()
        # print(res)
        return res
    except Exception as e:
        print(f"Get Serviço error: {e}")