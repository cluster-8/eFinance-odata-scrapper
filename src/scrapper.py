# -*- coding: utf-8 -*-
from .populate import *
from .score import *
from .historic_data import *

def run_update_database():
    try:
        print("Starting database update ...")
        insert_consolidated_groups()
        insert_financial_instituitions()
        insert_physical_person_services()
        insert_juridical_person_services()
        insert_all_tariffs()
        print("Database updated successfully!")
    except Exception as e:
        print(f'Run Update Database error: {e}')
    finally:
        insert_logs()
        
