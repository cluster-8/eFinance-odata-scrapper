from dotenv import dotenv_values
import os
import psycopg2
import logging

envs = dotenv_values('./.env')

print((os.getenv('DB_HOST') if os.getenv('DB_HOST') else envs['DB_HOST']))
print((os.getenv('DB_NAME') if os.getenv('DB_NAME') else envs['DB_NAME']))
print((os.getenv('DB_USER') if os.getenv('DB_USER') else envs['DB_USER']))
print((os.getenv('DB_HOST') if os.getenv('DB_HOST') else envs['DB_HOST']))

def get_database_psql():
   try:
      conn = psycopg2.connect(
         host=(os.getenv('DB_HOST') if os.getenv('DB_HOST') else envs['DB_HOST']),
         database=(os.getenv('DB_NAME') if os.getenv('DB_NAME') else envs['DB_NAME']),
         user=(os.getenv('DB_USER') if os.getenv('DB_USER') else envs['DB_USER']),
         password=(os.getenv('DB_PASS') if os.getenv('DB_PASS') else envs['DB_PASS']))
      return conn
   except Exception as e:
      logging.error('Get Database PSQL, connection error', exc_info=True)
      print(e)
