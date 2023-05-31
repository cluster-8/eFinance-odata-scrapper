# -*- coding: utf-8 -*-
from .populate import *
from .score import *
from .historic_data import *

def run_update_database():
    print("Starting database update ...")
    insert_consolidated_groups()
    insert_financial_instituitions()
    insert_physical_person_services()
    insert_tarifas()
    populate_scores()
    generate_series()
    print("Database updated successfully!")

# if __name__ == "__main__":
#     run_update_database()
#     print("main!")
