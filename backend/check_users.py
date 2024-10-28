from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(f"Connecting to: {MONGO_URI}")  # Be careful not to log this in production

client = MongoClient(MONGO_URI)
db = client.get_database()
print(f"Connected to database: {db.name}")

users_collection = db['users']
print(f"Users collection: {users_collection.name}")

def display_all_users():
    count = users_collection.count_documents({})
    print(f"Total number of users in the database: {count}")
    if count == 0:
        print("No users found in the database.")
    else:
        print("All users in the database:")
        for user in users_collection.find({}):
            pprint(user)
            print("---")

def find_user_by_username(username):
    user = users_collection.find_one({"username": username})
    if user:
        print(f"User found with username '{username}':")
        pprint(user)
    else:
        print(f"No user found with username '{username}'")

def list_collections():
    print("Collections in the database:")
    for collection in db.list_collection_names():
        print(f"- {collection}")

if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("1. Display all users")
        print("2. Find a user by username")
        print("3. List all collections")
        print("4. Exit")
        
        choice = input("Enter your choice (1, 2, 3, or 4): ")
        
        if choice == '1':
            display_all_users()
        elif choice == '2':
            username = input("Enter the username to search for: ")
            find_user_by_username(username)
        elif choice == '3':
            list_collections()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
