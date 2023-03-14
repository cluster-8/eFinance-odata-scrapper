# -*- coding: utf-8 -*-
import generate_json
import populate

# * run test
def run_test():
    
    # * generate json files (from olinda source)
    # generate_json.servicos_pj()
    # generate_json.instituicoes()
    # generate_json.tarifas_pf()
    # generate_json.tarifas_pj()
    
    # * populate database
    # populate.insert_servicos_pf()
    # populate.insert_instituicoes()
    # populate.insert_servicos_pj()
    # populate.insert_tarifas_pj()
    
    
    populate.insert_instituicoes()
    # populate.insert_servicos_pf()
    # populate.insert_servicos_pj()
    # populate.insert_tarifas()
        
if __name__ == "__main__":
    run_test()
