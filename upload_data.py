
from pymongo import MongoClient 
from pymongo.server_api import ServerApi
import pandas as pd 
import json 



#url 
url  = "mongodb+srv://mrinalMl:pwmachine221@cluster0.p7thjcz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# new client  
client = MongoClient(url)

# Create DB Name and Collection Name 
db_name = "Maxter_Ml"
collection_name = "Wafer_fault"

df = pd.read_csv('notebooks/wafer_23012020_041211.csv')


df = df.drop('Unnamed: 0', axis=1)

json_record = list(json.loads(df.T.to_json()).values())

type(json_record)

client[db_name][collection_name].insert_many(json_record)

