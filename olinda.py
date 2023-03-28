import requests

def get_financial_instituitions():
    '''
    Returns the list of financial instituitions from Olinda Source.
    '''
    
    url = "https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$top=10000&$format=json&$select=CnpjInstituicao,NomeInstituicao"
    try:
        result = requests.get(url)
        
        data = []
        for i in result.json()['value']:
            if i not in data: data.append(i)
        
        return data
    except Exception as e:
        print("Get Olinda Financial Instituitions error:", e)

def get_physical_person_tariffs(instituition_cnpj: str):
    '''
    Returns the list of all physical person services tariffs of a instituition from Olinda Source.
    
    :param instituition_cnpj: str
    '''
    try:
        cnpj = instituition_cnpj[:8]
    
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira (PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='F'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
        
        result = requests.get(url)
        
        if len(result.json()['value']) > 0: 
            return result.json()['value']
        
    except Exception as e:
        print("Get Olinda Physical Person Services Tariffs error:", e)

def get_juridical_person_tariffs(instituition_cnpj: str):
    '''
    Returns the list of all juridical person services tariffs of a instituition from Olinda Source.
    
    :param instituition_cnpj: str
    '''
    try:
        cnpj = instituition_cnpj[:8]
    
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira (PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='J'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
        
        result = requests.get(url)
        
        if len(result.json()['value']) > 0: 
            return result.json()['value']
        
    except Exception as e:
        print("Get Olinda Juridical Person Services Tariffs error:", e)

        
def get_tariffs_by_cnpj(cnpj: str, instituition_name: str):
    '''
    Returns the list of all tariffs of a instituition from Olinda Source.
    
    :param instituition_cnpj: str
    '''
    try:
        parsed_cnpj = cnpj[:8]
        service_type = 'F'
        
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{service_type}'&@CNPJ='{parsed_cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
        
        
        pf_tariffs = requests.get(url).json()['value']
        if not pf_tariffs: 
            pf_tariffs = []
        else:    
            for i in pf_tariffs:
                i['TipoServico'] = service_type
                i['CnpjInstituicao'] = cnpj
                i['NomeInstituicao'] = instituition_name
                
        service_type = 'J'
        pj_tariffs = requests.get(url).json()['value']
        if not pj_tariffs:
            pj_tariffs = []
        else:
            for i in pj_tariffs:
                i['TipoServico'] = service_type
                i['CnpjInstituicao'] = cnpj
                i['NomeInstituicao'] = instituition_name
        
        tariffs = [*pf_tariffs, *pj_tariffs]
        if len(tariffs) == 0: return
        
        return tariffs
    except Exception as e:
        print(f"Get tariffs by cnpj error: {e}")
        
def get_financial_instituitions_endpoints():
    try:
        url = "https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$top=10000&&$filter=Api%20eq%20'taxas_cartoes'&$format=json&$select=Api,Versao,CnpjInstituicao,NomeInstituicao,Recurso,Argumento,Situacao,URLDados"
        
        response = requests.get(url)
        
        return response.json()['value']
    except Exception as e:
        print(f"Get Financial Instituitions endpoints error: {e}")

# * TAXAS DE JUROS PARA OPERAÇÕES DE CRÉDITO
def get_daily_interest_rates_per_beginning_period(start_date: str):
    '''
       Function to get the credit operations rates of all financial irnstituitions by beginning period
    '''
    try:
        if not start_date:
            print('Start date not specified!')
            return
            
        url = f"https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/TaxasJurosDiariaPorInicioPeriodo?$top=100&$filter=InicioPeriodo%20eq%20'{start_date}'&$format=json&$select=InicioPeriodo,FimPeriodo,Segmento,Modalidade,Posicao,InstituicaoFinanceira,TaxaJurosAoMes,TaxaJurosAoAno,cnpj8"
        
        response = requests.get(url)
        
        return response.json()['value']
    except Exception as e:
        print(f"Get Rates on Credits Operations error: {e}")
        
def get_daily_interest_rates_per_instituition(cnpj8: str):
    '''
    '''
    try:
        if not cnpj8:
            print('Start date not specified!')
            return
            
        url = f"https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/TaxasJurosDiariaPorInicioPeriodo?$filter=cnpj8%20eq%20'{cnpj8}'&$format=json&$select=InicioPeriodo,FimPeriodo,Segmento,Modalidade,Posicao,InstituicaoFinanceira,TaxaJurosAoMes,TaxaJurosAoAno,cnpj8"
        
        response = requests.get(url)
        
        return response.json()['value']
    except Exception as e:
        print(f"Get Rates on Credits Operations error: {e}")
        
def get_query_dates():
    '''
    '''
    try:
        url = "https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/ConsultaDatas?$top=10000&$format=json&$select=inicioPeriodo,fimPeriodo,tipoModalidade"
        
        response = requests.get(url)
        
        return response.json()['value']
    except Exception as e:
        print(f"Get Rates on Credits Operations error: {e}")