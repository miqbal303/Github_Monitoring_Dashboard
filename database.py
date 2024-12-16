import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

#load environment varibles
load_dotenv()

#MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = "Github_Commits"
COLLECTION_NAME = "Commits"


def get_mongo_client():
    try:
        if not MONGO_URI or not DATABASE_NAME or not COLLECTION_NAME:
            raise ValueError("Missing required environment variable: MONGO_URI,DATABASE_NAME, or COLLECTION_NAME")
        
        client = MongoClient(MONGO_URI)

        client.admin.command("ping") # ping mongodb to check connection

        print("Successfully connection to MongoDB")

        return client[DATABASE_NAME][COLLECTION_NAME]
    except errors.ServerSelectionTimeOutError as e:
        print(f"Mongodb connection error: {e}")
    except ValueError as e:
        print(f"Missing required environment variable: {e}")
    except Exception as e:
              print(f"An error occurred: {e}")
    return None


if __name__ == "__main__":
     collection = get_mongo_client()
     if collection is not None:
          print("Connected to MongoDB")
     else:
          print("Failed to connect to MongoDB")