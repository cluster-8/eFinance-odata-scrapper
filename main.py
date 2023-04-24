# -*- coding: utf-8 -*-
import populate
import database
import score

def run_update_database():
    print("Starting database update ...")
    # populate.insert_consolidated_groups()
    populate.insert_financial_instituitions()
    populate.insert_physical_person_services()
    populate.insert_tarifas()
    score.populate_scores()
    
    # * inserting financial instituitions tariffs
    # instituitions = database.get_all_financial_instituitions()
    # for i in instituitions:
    #     groups = database.get_financial_instituition_groups(i[0])
    #     populate.insert_financial_instituition_tariffs(i, groups)
    
    print("Database updated successfully!")

if __name__ == "__main__":
    # run_update_database()
    print("main!")
