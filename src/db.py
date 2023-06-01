from dotenv import dotenv_values
import psycopg2
import logging

envs = dotenv_values('.env')

print(envs['DB_HOST'])
print(envs['DB_NAME'])
print(envs['DB_USER'])
print(envs['DB_PASS'])

def get_database_psql():
   try:
      conn = psycopg2.connect(
         host=envs['DB_HOST'],
         database=envs['DB_NAME'],
         user=envs['DB_USER'],
         password=envs['DB_PASS'])
      return conn
   except Exception as e:
      logging.error('Get Database PSQL, connection error', exc_info=True)
      print(e)
