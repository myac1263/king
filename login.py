import bcrypt
import json


USER_DATA_FILE = "users.json"


# Hashing passwords
def hash_password(password):
   salt = bcrypt.gensalt()
   return bcrypt.hashpw(password.encode('utf-8'), salt)


# Load existing user data from the file (if it exists)
def load_users():
   try:
       with open(USER_DATA_FILE, "r") as file:
           data = file.read().strip()
           return json.loads(data) if data else {}
   except (FileNotFoundError, json.JSONDecodeError):
       return {}


# Save the updated user data
def save_users(users):
   with open(USER_DATA_FILE, "w") as file:
       json.dump(users, file)


# Setting default admin account
def initialize_users():
   users = load_users()
   if "admin" not in users:
       users["admin"] = {
           "password": hash_password("password").decode('utf-8'),
           "role": "Admin"
       }
       save_users(users)


# Login function to verify user credentials
def login(username, password):
   users = load_users()
   if username in users:
       stored_hash = users[username]["password"].encode('utf-8')
       return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
   return False



