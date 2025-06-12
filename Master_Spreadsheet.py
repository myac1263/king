import streamlit as st
import pandas as pd
import io


def display_Master_Spreadsheet_panel():
   # Header image
   st.image("https://i.imgur.com/qh7yOt2.jpeg", use_container_width=True)
   st.markdown("---")
   st.title("Master Data Upload")


   # Initialize session state
   if "master_df" not in st.session_state:
       st.session_state["master_df"] = None
   if "raw_file" not in st.session_state:
       st.session_state["raw_file"] = None


   # File Uploader
   uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


   if uploaded_file is not None:
       file_contents = uploaded_file.getvalue() 
       st.session_state["raw_file"] = file_contents 
      
       master_df = pd.read_csv(io.BytesIO(file_contents))


       # Remove commas
       if "RegistrationID" in master_df.columns:
           master_df["RegistrationID"] = master_df["RegistrationID"].astype(str).str.replace(",", "")


       st.session_state["master_df"] = master_df 
       st.success("File uploaded successfully!")


   # Display data if uploaded
   if st.session_state["master_df"] is not None:
       master_df = st.session_state["master_df"]
       st.write("Master Spreadsheet:")
       st.dataframe(master_df) 
   else:
       st.warning("Please upload a CSV file.")