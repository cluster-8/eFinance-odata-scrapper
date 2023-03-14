# -*- coding: utf-8 -*-
import json
import datetime
import requests

import get_data

# * GENERATE JSON FILES
def servicos_pf():
    '''
        Gera uma massa de dados em json com todos os servicos para pessoa física na plataforma odata
    '''
    print(f'{datetime.datetime.now()} - criando servicos.json.')
    try:
        ifs = get_data.instituicoes()        
        all_services = []
        
        json_data = open('bkp-services.json')
        j_data = json.load(json_data)
        
        idx = len(ifs) - 1
        print(idx)
        # for i in ifs:
        while idx >=  0:
            # if_name = i['NomeInstituicao']
            if_name = ifs[idx]['NomeInstituicao']
            print(f'{datetime.datetime.now()} - buscando serviços de {if_name} ------------------------')
            # cnpj = i['CnpjInstituicao']
            cnpj = ifs[idx]['CnpjInstituicao']
            services = get_data.servicos_pf(cnpj)
            
            if len(services) > 0: 
                for i in services:
                    obj = {
                        "codigo": i['CodigoServico'],
                        "nome": i['Servico'],
                        "tipo": "Pessoa Física",
                        "unidade": i["Unidade"],
                        "moeda": i['TipoValor'],
                        "periodicidade": i['Periodicidade']
                    }
                    if obj not in all_services:
                    # if obj not in j_data:
                        all_services.append(obj)
                        print(datetime.datetime.now(), ' - Inserindo: ', obj['codigo'], obj['nome'])
                        json_string = [ob for ob in all_services]
                        with open('./json/services-2.json', 'w', encoding='utf-8') as f:
                            json.dump(json_string, f, ensure_ascii=False)
                        f.close()
                    else:
                        cod = i['CodigoServico']
                        print(f'{datetime.datetime.now()} - serviço {cod} já existe.')
                        continue
            idx -= 1
    except Exception as e:
        print(f'{datetime.datetime.now()} - Erro: {e}')
        
def servicos_pj():
    '''
        Gera uma massa de dados em json com todos os servicos para pessoa jurídica na plataforma odata
    '''
    print(f'{datetime.datetime.now()} - criando servicos.json.')
    try:
        ifs = get_data.instituicoes()        
        all_services = []
        
        # json_data = open('./json/services-pj-2.json')
        # j_data = json.load(json_data)
        
        idx = len(ifs) - 1
        while idx >=  0:
            if_name = ifs[idx]['NomeInstituicao']
            print(f'{datetime.datetime.now()} - buscando serviços de {if_name} ------------------------')
            cnpj = ifs[idx]['CnpjInstituicao']
            services = get_data.servicos_pj(cnpj)
            
            if len(services) > 0: 
                for i in services:
                    obj = {
                        "codigo": i['CodigoServico'],
                        "nome": i['Servico'],
                        "tipo": "Pessoa Jurídica",
                        "unidade": i["Unidade"],
                        "moeda": i['TipoValor'],
                        "periodicidade": i['Periodicidade']
                    }
                    if obj not in all_services:
                    # if obj not in j_data:
                        all_services.append(obj)
                        print(datetime.datetime.now(), ' - Inserindo: ', obj['codigo'], obj['nome'])
                        json_string = [ob for ob in all_services]
                        with open('services-pj-3.json', 'w', encoding='utf-8') as f:
                            json.dump(json_string, f, ensure_ascii=False)
                        f.close()
                    else:
                        cod = i['CodigoServico']
                        print(f'{datetime.datetime.now()} - serviço {cod} já existe.')
                        continue
            idx -= 1
    except Exception as e:
        print(f'{datetime.datetime.now()} - Erro: {e}')

def instituicoes():
    '''
        Gera uma massa de dados em json com todas as instituições financeiras na plataforma odata
    '''
    print(f'{datetime.datetime.now()}- gerando instituições.json')
    try:
        data = get_data.instituicoes()
        aux = []
        for i in data:
            cnpj_formatado = get_cnpj_formatado(i['CnpjInstituicao'])
            obj = {
                "grupo_consolidado": None,
                "nome": i['NomeInstituicao'],
                "cnpj": i['CnpjInstituicao'],
                "cnpj_formatado": cnpj_formatado
            }
            if obj not in aux: aux.append(obj)
            # aux.append(obj)
            json_string = [ob for ob in aux]
            with open('./json/instituicoes-4.json', 'w', encoding='utf-8') as f:
                json.dump(json_string, f, ensure_ascii=False)
            f.close()
        # json_string = [ob for ob in aux]
        # with open('instituicoes-3.json', 'w', encoding='utf-8') as f:
        #     json.dump(json_string, f, ensure_ascii=False)
        # f.close()
        return
    except Exception as e:
        print(f'{datetime.datetime.now()} - Erro: {e}')

def grupos():
    '''
        Gera uma massa de dados em json com todos os grupos consolidados na plataforma odata
    '''
    print(f'{datetime.datetime.now()}- gerando grupos.json')
    try:
        data = get_data.grupos()
        aux = []
        for val in data:
            obj = {
                "codigo": val['Codigo'],
                "nome": val['Nome']
            }
            aux.append(obj)
        json_string = [ob for ob in aux]
        with open('./json/grupos.json', 'w', encoding='utf-8') as f:
            json.dump(json_string, f, ensure_ascii=False)
        f.close()
        return 
    except Exception as e:
        print(f'Generate Grupos Consolidados JSON error: {e}')

def tarifas_pf():
    '''
        Rertorna as tarifas para serviços pessoa física
    '''
    print(f'{datetime.datetime.now()} - criando tarifas-pf.json.')
    try:
        ifs = get_data.get_all_instituicoes()
        aux = []
        for idx in ifs:
            instituicao_id = idx[0]
            cnpj_formatado = idx[4]
            tarifas = get_data.tarifas_pf(cnpj_formatado)
            
            if not tarifas: 
                print(f'{datetime.datetime.now()} - nenhuma tarifa encontrada para instituicão de CNPJ: {cnpj_formatado}')
                continue
            else:
                for t in tarifas:
                    cod_servico = t['CodigoServico']
                    servico = get_data.get_servico_id_by_codigo(cod_servico)
                    servico_id = servico[0]
                    
                    obj = {
                        "servico_id": servico_id,
                        "instituicao_id": instituicao_id,
                        "valor_maximo": t['ValorMaximo'],
                        "data_vigencia": t['DataVigencia'],
                        "unidade": t['Unidade'],
                        "periodicidade": t['Periodicidade'],
                        "moeda": t['TipoValor']
                    }
                    
                    if obj not in aux: aux.append(obj)
                    json_string = [ob for ob in aux]
                    with open('./json/tarifas-pf.json', 'w', encoding='utf-8') as f:
                        json.dump(json_string, f, ensure_ascii=False)
                    f.close()
                    
                    # print(obj)
            
            
            # modelo = {
            #     'CodigoServico': '1607', 
            #     'Servico': 'Utilização de canais de atend. para retirada em espécie - no exterior', 
            #     'Unidade': 'por evento', 
            #     'DataVigencia': '2019-07-01', 
            #     'ValorMaximo': 8.58, 
            #     'TipoValor': 'Real', 
            #     'Periodicidade': 'Por evento'
            # }
        
    except Exception as e:
        print(f'{datetime.datetime.now()} - Erro: {e}')

def tarifas_pj():
    '''
        Rertorna as tarifas para serviços pessoa jurídica
    '''
    print(f'{datetime.datetime.now()} - criando tarifas-pj.json.')
    try:
        ifs = get_data.get_all_instituicoes()
        aux = []
        for idx in ifs:
            instituicao_id = idx[0]
            cnpj_formatado = idx[4]
            tarifas = get_data.tarifas_pj(cnpj_formatado)
            
            if not tarifas: 
                print(f'{datetime.datetime.now()} - nenhuma tarifa encontrada para instituicão de CNPJ: {cnpj_formatado}')
                continue
            else:
                for t in tarifas:
                    cod_servico = t['CodigoServico']
                    servico = get_data.get_servico_id_by_codigo(cod_servico)
                    servico_id = servico[0]
                    
                    obj = {
                        "servico_id": servico_id,
                        "instituicao_id": instituicao_id,
                        "valor_maximo": t['ValorMaximo'],
                        "data_vigencia": t['DataVigencia'],
                        "unidade": t['Unidade'],
                        "periodicidade": t['Periodicidade'],
                        "moeda": t['TipoValor']
                    }
                    
                    if obj not in aux: aux.append(obj)
                    json_string = [ob for ob in aux]
                    with open('./json/tarifas-pj.json', 'w', encoding='utf-8') as f:
                        json.dump(json_string, f, ensure_ascii=False)
                    f.close()
        
    except Exception as e:
        print(f'{datetime.datetime.now()} - Erro: {e}')
        
def get_cnpj_formatado(cnpj):
    '''
        Recebe o cnpj e retorna o valor de cnpj válido
        para realizar consultas na plataforma odata
    '''
    try:
        last = len(str(cnpj))
        value = []
        if not value: 
            print(f'{datetime.datetime.now()} - "value" inválido.')
            # return
        while len(value) == 0 and last > 0:
            pessoa = "F"
            cnpj = str(cnpj)[:last]
            url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{pessoa}'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
            response = requests.get(url)
            response_status = response.status_code
            if response_status == 200:
                value = response.json()['value']
            last -= 1
        return cnpj
    except Exception as e:
        print(f'{datetime.datetime.now()} - Erro: {e}')
    