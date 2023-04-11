# -*- coding: utf-8 -*-
import populate
import database
# import score
# import schedule
# import time

def run_update_database():
    print("Starting database update ...")
    # populate.insert_consolidated_groups()
    # populate.insert_financial_instituitions()
    # populate.insert_financial_instituition_groups()
    
    # populate.insert_physical_person_services()
    # populate.insert_juridical_person_services()
    
    # * inserting financial instituitions tariffs
    # instituitions = database.get_all_financial_instituitions()

    # for i in instituitions:
        # groups = database.get_financial_instituition_groups(i[0])
        # populate.insert_financial_instituition_tariffs(i, groups)
    
    print("Database updated successfully!")
        
if __name__ == "__main__":
    print('Main started')
    
    run_update_database()

    # schedule.every(interval=).day.at("03:00").do(run_update_database)
    # schedule.every(2).minutes.do(run_update_database)

    # while True:
    #     print('true?')
    #     schedule.run_pending()
    #     time.sleep(30)
