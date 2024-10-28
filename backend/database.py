from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_database():
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable is not set")
    
    client = MongoClient(MONGO_URI)
    return client['fencer_lunge']  # replace 'fencer_lunge' with your actual database name
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_database():
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable is not set")
    
    client = MongoClient(MONGO_URI)
    return client['fencer_lunge']  # replace 'fencer_lunge' with your actual database name

# Get a reference to the database
db = get_database()

# Get a reference to the users collection
users_collection = db['users']

def test_connection():
    try:
        db.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB. Error: {e}")

if __name__ == "__main__":
    test_connection()

# You can add a test connection function
def test_connection():
    try:
        db = get_database()
        db.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB. Error: {e}")

if __name__ == "__main__":
    test_connection()
