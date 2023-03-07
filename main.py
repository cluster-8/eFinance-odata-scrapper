import requests
import db

database = db.get_database()

def get_IFs():
    
    url = "https://olinda.bcb.gov.br/olinda/servico/DASFN/versao/v1/odata/Recursos?$top=10000&$format=json&$select=Api,Versao,CnpjInstituicao,NomeInstituicao,NomeContato,EmailContato,Recurso,Argumento,Situacao,URLDados,URLConsulta"
    
    try:
        result = requests.get(url, verify=False)

        for data in result.json()['value']:
            bank = database.banks.find_one({'CnpjInstituicao': data['CnpjInstituicao']})

            print("bank (data): ", data['NomeInstituicao'])

            if bank: 
                print("bank encontrado: ", bank['NomeInstituicao'])

                recursoAlreadyExist = next(item for item in bank['apis'] if item['Recurso'] == data['Recurso'])

                if recursoAlreadyExist: 
                    print("recurso já existe: ", recursoAlreadyExist['Recurso'])
                    break

                database.banks.update_one(bank, {'$push': {'apis':  {
                    'Api': data['Api'], 'Versao': data['Versao'], 'Recurso': data['Recurso'], 'Argumento': data['Argumento'], 'Situacao': data['Situacao'], 'URLDados': data['URLDados'], 'URLConsulta': data['URLConsulta']
                }}})
            else:
                print("bank sendo criado: ", bank['NomeInstituicao'])

                database.banks.insert_one({'CnpjInstituicao': data['CnpjInstituicao'], 'NomeInstituicao': data['NomeInstituicao'], 'apis': []})

            # return
    except Exception as e:
        print(e)

# def get_tariffs_by_if(if_cnpj, tipo_pessoa):
    
#     pessoa = 'F' if tipo_pessoa == 'pf' else 'J'
#     # cnpj = if_cnpj[:9]
#     cnpj = if_cnpj[:8]
    
#     url = f"https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='{pessoa}'&@CNPJ='{cnpj}'&$top=10000&$format=json&$select=CodigoServico,Servico,Unidade,DataVigencia,ValorMaximo,TipoValor,Periodicidade"
    
#     try:
#         result = requests.get(url)
        
#         if len(result.json()['value']) > 0:
#             print()
#             # print(cnpj, result.status_code, result.json()['value'])
        
#     except Exception as e:
#         print(e)
        
def run_test():
    
    ifs = get_IFs()
    
#     ifs_nomes = []
    
#     for i in range(len(ifs)):
#         cnpj = ifs[i]['CnpjInstituicao']
#         res = get_tariffs_by_if(cnpj, 'pf')
#         # print(res)
#         break
#         # print(ifs[])
#         # if ifs[i]['NomeInstituicao'] not in ifs_nomes:
#         #     ifs_nomes.append(ifs[i]['NomeInstituicao'])
      
#     # print(len(ifs_nomes))  
    
#     # for i in range(len(ifs_nomes)):
#         # print(ifs_nomes[i])
        
        
if __name__ == "__main__":
    run_test()

