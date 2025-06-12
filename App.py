import streamlit as st
from login import login, load_users
import Home
import Admin
import Test_Date
import Master_Spreadsheet


# Initialize session state variables if not already set
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "page" not in st.session_state:
  st.session_state.page = "login"
if "role" not in st.session_state:
  st.session_state.role = None  # Default role if not logged in


# Function to show the login form
def show_login_form():
  st.title("Login Page")
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")




  if st.button("Login"):
      if login(username, password):  # Verify credentials
          st.session_state.logged_in = True
          st.session_state.username = username


          # Set the user's role in session_state
          users = load_users() 
          if username in users:
              st.session_state.role = users[username]["role"]


          st.session_state.page = "home"  # Redirect to home page
          st.rerun()  # Force rerun to reflect the new state
      else:
          st.error("Invalid username or password.")


#Logout Button
def show_logout_button():
  if st.button("Logout"):
      # Reset the session state variables to log the user out
      st.session_state.logged_in = False
      st.session_state.page = "login"  # Redirect to login page
      st.session_state.role = None  # Clear the user role
      st.rerun()


# Main app
if not st.session_state.logged_in:
  show_login_form()
else:
  # Sidebar navigation
  st.sidebar.title("Navigation")
  page_selection = st.sidebar.radio(
      "Navigate",
      [
          "🏠 Home",
          "🛠️ Admin",
          "📊 Master Spreadsheet",
          "📅 Test Date",
      ],
      key="radio1"
  )


  # Session state for navigation
  if page_selection == "🏠 Home":
      st.session_state.page = "home"
      Home.display_Home_panel()
  elif page_selection == "🛠️ Admin":
      st.session_state.page = "Admin"
      Admin.display_Admin_panel()
  elif page_selection == "📅 Test Date":
      st.session_state.page = "Test_Date"
      Test_Date.display_Test_Date_panel()
  elif page_selection == "📊 Master Spreadsheet":
      st.session_state.page = "Master_Spreadsheet"
      Master_Spreadsheet.display_Master_Spreadsheet_panel()


  show_logout_button()

