from pymongo import MongoClient
from dotenv import dotenv_values

envs = dotenv_values('.env')

def get_database():

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(envs['DB_URL'])
   
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['eAlgumaCoisa']
