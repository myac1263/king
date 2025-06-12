import streamlit as st
import pandas as pd
import io


def display_Test_Date_panel():
   st.image("https://i.postimg.cc/4dT1D9X9/b309757a-7f9d-4052-a70f-9497b952fc8b-1.jpg", use_container_width=True)
   st.markdown("---")
   st.title("Test Date Filtering")


   # Ensure data exists in session state
   if "raw_file" not in st.session_state or st.session_state["raw_file"] is None:
       st.error("No master data found. Please upload data on the Master Data Upload page.")
       return


   try:
       # Load CSV data
       master_df = pd.read_csv(io.BytesIO(st.session_state["raw_file"]))


       # RegistrationID has no commas
       if "RegistrationID" in master_df.columns:
           master_df["RegistrationID"] = master_df["RegistrationID"].astype(str).str.replace(",", "")


       st.write("CSV loaded successfully! Here is a preview:")
       st.dataframe(master_df.head())


       if "RegistrationTestDate" not in master_df.columns:
           st.error("No 'RegistrationTestDate' column found. Available columns:")
           st.write(master_df.columns)
           return


       # Date filter
       date_input = st.date_input("Select Date to Filter:")
       if date_input:
           filtered_df = process_data(master_df.copy(), "RegistrationTestDate", date_input)


           if filtered_df is not None:
               st.write(f"There are {len(filtered_df)} students registered to do their test on this selected date!")
               st.dataframe(filtered_df)
              
                # Creating Groups
               if not filtered_df.empty:
                   num_groups = st.number_input("Enter number of groups:", min_value=1, max_value=500, value=5)
                   grouped_df = assign_groups(filtered_df.copy(), num_groups)


                   if grouped_df is not None:
                       st.write("Grouped Data:")
                       st.dataframe(grouped_df)
                      
                       # Filter Teachers
                       teachers_rooms = st.text_area("Enter teachers and rooms (format: Teacher - Room, one per line):")


                       if teachers_rooms:
                           assigned_df = assign_teachers(grouped_df.copy(), teachers_rooms)


                           if assigned_df is not None:
                               st.write("Final Group Assignments:")
                               st.dataframe(assigned_df)


                               csv_data = assigned_df.to_csv(index=False)
                               st.download_button("Download Final Assignments", data=csv_data, file_name="final_assignments.csv", mime="text/csv")


                               teacher_filter = st.text_input("Filter by Teacher Name:")
                               if teacher_filter:
                                   filtered_by_teacher = assigned_df[assigned_df["Teacher"].str.contains(teacher_filter, case=False, na=False)]
                                   st.write(f"Filtered Data for {teacher_filter}:")
                                   st.dataframe(filtered_by_teacher)


                                   csv_filtered = filtered_by_teacher.to_csv(index=False)
                                   st.download_button(f"Download Data for {teacher_filter}", data=csv_filtered, file_name=f"filtered_{teacher_filter}.csv", mime="text/csv")


   except Exception as e:
       st.error(f"Error processing the data: {e}")


# Function to process data
def process_data(df, date_column, date_input):
   try:
       df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
       filtered_df = df[df[date_column].dt.date == date_input]


       # RegistrationID has no commas
       if "RegistrationID" in df.columns:
           df["RegistrationID"] = df["RegistrationID"].astype(str).str.replace(",", "")


       return filtered_df[['StudentFirstName', 'StudentMiddleName', 'StudentLastName',
                           'StudentPreferredName', 'RegistrationID', date_column]]
   except Exception as e:
       st.error(f"Error processing data: {e}")
       return None


# Assign groups
def assign_groups(df, num_groups):
   try:
       df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # randomlize
       df['Group'] = [f"Group {i % num_groups + 1}" for i in range(len(df))]
       return df
   except Exception as e:
       st.error(f"Error assigning groups: {e}")
       return None


# Function to assign teachers and rooms
def assign_teachers(df, teachers_rooms):
   try:
       groups = df['Group'].unique()
       assignments = {group: {"Teacher": "King", "Room": "N/A"} for group in groups}


       teacher_room_pairs = [line.split(" - ") for line in teachers_rooms.split("\n") if " - " in line]
       for group, (teacher, room) in zip(groups, teacher_room_pairs):
           assignments[group] = {"Teacher": teacher, "Room": room}


       df["Teacher"] = [assignments[g]["Teacher"] for g in df["Group"]]
       df["Room"] = [assignments[g]["Room"] for g in df["Group"]]
       return df
   except Exception as e:
       st.error(f"Error assigning teachers and rooms: {e}")
       return None



