# -*- coding: utf-8 -*-
import populate
import database
import score
import historic_data

def run_update_database():
    print("Starting database update ...")
    # populate.insert_consolidated_groups()
    # populate.insert_financial_instituitions()
    # populate.insert_physical_person_services()
    # populate.insert_tarifas()
    # score.populate_scores()
    # historic_data.generate_series()
    print("Database updated successfully!")

if __name__ == "__main__":
    run_update_database()
    print("main!")
