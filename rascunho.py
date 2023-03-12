# -*- coding: utf-8 -*-
import requests
import db
import json
import datetime
import generate_json
import populate
import get_data

# * run test
def run_test():
    # populate.insert_servicos_pf()
    
    # populate.insert_instituicoes()
    
    # populate.insert_servicos_pj()
    
    
    # generate_json.servicos_pj()
    
    # generate_json.instituicoes()
    
    # cnpj = '03183937000138'
    # get_data.get_instituicao_by_cnpj(cnpj)
    
    # get_data.get_all_instituicoes()
    
    generate_json.tarifas_pf()
        
if __name__ == "__main__":
    run_test()