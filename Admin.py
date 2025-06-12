import streamlit as st
import bcrypt
import json


USER_DATA_FILE = "users.json"


# Load existing user data
def load_users():
   try:
       with open(USER_DATA_FILE, "r") as file:
           data = file.read().strip()
           return json.loads(data) if data else {}
   except (FileNotFoundError, json.JSONDecodeError):
       return {}


# Save users to the file
def save_users(users):
   with open(USER_DATA_FILE, "w") as file:
       json.dump(users, file)


# Hash password
def hash_password(password):
   salt = bcrypt.gensalt()
   return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


# Create new user
def create_user(username, password, role="User"):
   users = load_users()
   if username in users:
       return False  # Username already exists


   users[username] = {
       "password": hash_password(password),
       "role": role
   }
   save_users(users)
   return True


def display_Admin_panel():
   st.image("https://i.imgur.com/5XKaNKK.jpeg", use_container_width=True)
   st.markdown("---")


   st.subheader("Admin Panel: Create New Users and Manage Roles")


   new_user = st.text_input("New Username", key="new_user")
   new_password = st.text_input("New Password", type="password", key="new_password")
  
   role_options = ["Admin", "User"]
   selected_role = st.selectbox("Select Role", role_options)


   if st.button("Create User"):
       if new_user and new_password:
           success = create_user(new_user, new_password, selected_role)
           if success:
               st.success(f"✅ User `{new_user}` created with role `{selected_role}`!")
           else:
               st.error(f"❌ Username `{new_user}` already exists. Choose a different username.")
       else:
           st.error("Username and password cannot be empty.")





