from dotenv import dotenv_values
import psycopg2

envs = dotenv_values('.env')

def get_database_psql():
   try:
      conn = psycopg2.connect(
         host="localhost",
         database=envs['DB_NAME'],
         user=envs['DB_USER'],
         password=envs['DB_PASS'])
      return conn
   except Exception as e:
      print(e)