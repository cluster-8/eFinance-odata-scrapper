import requests
import logging
import log


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
        logging.error('Get Olinda Financial Instituitions error', exc_info=True)
        print("Get Olinda Financial Instituitions error:", e)

def get_physical_person_tariffs(instituition_cnpj: str):
    '''
    Returns the list of all physical person services tariffs of a instituition from Olinda Source.
    
    :param instituition_cnpj: str
    '''
    try:
        cnpj = instituition_cnpj[:8]
        
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='F'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
        
        result = requests.get(url)
        print(cnpj, result)
        
        if len(result.json()['value']) > 0: 
            return result.json()['value']
        
    except Exception as e:
        logging.error('Get Olinda Physical Person Services Tariffs error', exc_info=True)
        print("Get Olinda Physical Person Services Tariffs error:", e)

def get_juridical_person_tariffs(instituition_cnpj: str):
    '''
    Returns the list of all juridical person services tariffs of a instituition from Olinda Source.
    
    :param instituition_cnpj: str
    '''
    try:
        cnpj = instituition_cnpj[:8]
        
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='J'&@CNPJ='{cnpj}'&$top=100&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
        
        result = requests.get(url)
        
        if len(result.json()['value']) > 0: 
            return result.json()['value']
        
    except Exception as e:
        logging.error('Get Olinda Juridical Person Services Tariffs error', exc_info=True)
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
        logging.error('Get tariffs by cnpj error', exc_info=True)
        print(f"Get tariffs by cnpj error: {e}")
        
def get_consolidated_groups():
    '''
    Returns the list of consolidated groups from Olinda Source.
    '''
    try:
        url = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/GruposConsolidados?$top=100&$format=json&$select=Codigo,Nome"
        
        groups = requests.get(url).json()['value']
        return groups
    except Exception as e:
        logging.error('Get Consolidated Groups error', exc_info=True)
        print(f"Get Consolidated Groups error: {e}")
        
def get_financial_instituitions_by_group(group_code: str):
    '''
    Returns the list of Financial Instituitions of a given group code from Olinda Source.
    '''
    try:
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaInstituicoesDeGrupoConsolidado(CodigoGrupoConsolidado=@CodigoGrupoConsolidado)?@CodigoGrupoConsolidado='{group_code}'&$top=10000&$format=json&$select=Cnpj,Nome"
        
        instituitions = requests.get(url).json()['value']
        return instituitions
    except Exception as e:
        logging.error('Get Financial Instituitions by Consolidated Group error', exc_info=True)
        print(f"Get Financial Instituitions by Consolidated Group error: {e}")
        
def get_all_services():
    '''
    Returns the list of all services from Olinda Source.
    '''
    try:
        url = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifaPorValores/versao/v1/odata/ServicosBancarios?$top=10000&$format=json&$select=Codigo,Nome"
        
        services = requests.get(url).json()['value']
        return services
    except Exception as e:
        logging.error('Get All Services from Olinda Source error', exc_info=True)
        print(f"Get All Services from Olinda Source error: {e}")
        
def get_all_services_values_by_group(service_type: str, group_code: str):
    '''
    Returns a list of max, min and mean values for all physical person services of a given group.
    
    :param group_code: str
    :param service_type: str
    '''
    try:
        if service_type not in "FJ": raise Exception(f"Inavlid service type: {service_type}")
        
        url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaValoresDeServicoBancario/versao/v1/odata/ListaValoresServicoBancario(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CodigoGrupoConsolidado=@CodigoGrupoConsolidado)?@PessoaFisicaOuJuridica='{service_type}'&@CodigoGrupoConsolidado='{group_code}'&$top=10000&$format=json&$select=NomeServico,ValorMinimo,PeriodicidadeValorMinimo,ValorMaximo,PeriodicidadeValorMaximo,ValorMedio"
        
        values = requests.get(url).json()['value']
        return values
    except Exception as e:
        logging.error('Get All Services Values by Group error', exc_info=True)
        print(f"Get All Services Values by Group error: {e}")