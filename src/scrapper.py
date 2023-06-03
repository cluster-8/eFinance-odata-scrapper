# -*- coding: utf-8 -*-
from .populate import *
from .score import *
from .historic_data import *

def run_update_database():
    print("Starting database update ...")
    insert_consolidated_groups()
    insert_financial_instituitions()
    insert_physical_person_services()
    insert_all_tariffs()
    # insert_logs()
    
    print("Database updated successfully!")
