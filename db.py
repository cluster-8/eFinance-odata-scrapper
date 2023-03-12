from pymongo import MongoClient
from dotenv import dotenv_values
import psycopg2

envs = dotenv_values('.env')

def get_database():

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(envs['DB_URL'])
   
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['eAlgumaCoisa']

def get_database_psql():
   try:
      conn = psycopg2.connect(
         host="localhost",
         database=envs['DB_NAME'],
         user=envs['DB_USER'],
         password=envs['DB_PASS'])
      # print(conn)
      return conn
   except Exception as e:
      print(e)