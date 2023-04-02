# -*- coding: utf-8 -*-
import populate

def run_update_database():
    populate.insert_financial_instituitions()
    populate.insert_physical_person_services()
    populate.insert_tarifas()
        
if __name__ == "__main__":
    run_update_database()
