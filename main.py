# -*- coding: utf-8 -*-
import populate
import database

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


from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()