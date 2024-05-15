# import streamlit as st
# from datetime import datetime
# import sqlite3
# import pandas as pd

# def create_table_if_not_exists():
#     conn = sqlite3.connect("75hard.db")
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS progress (
#                     id INTEGER PRIMARY KEY,
#                     participant TEXT,
#                     rule_num INTEGER,
#                     day DATE,
#                     checked INTEGER
#                 )''')
#     conn.commit()
#     conn.close()
    
# def save_checkbox_status(participant, rule_num, day, checked):
#     conn = sqlite3.connect("75hard.db")
#     c = conn.cursor()
#     c.execute('''SELECT * FROM progress WHERE participant=? AND rule_num=? AND day=?''', (participant, rule_num, day))
#     result = c.fetchone()
#     if result:
#         c.execute('''UPDATE progress SET checked=? WHERE participant=? AND rule_num=? AND day=?''', (checked, participant, rule_num, day))
#     else:
#         c.execute('''INSERT INTO progress (participant, rule_num, day, checked) VALUES (?, ?, ?, ?)''', (participant, rule_num, day, checked))
#     conn.commit()
#     conn.close()
    
# def get_checkbox_status(participant, rule_num, day):
#     conn = sqlite3.connect("75hard.db")
#     c = conn.cursor()
#     c.execute('''SELECT checked FROM progress WHERE participant=? AND rule_num=? AND day=?''', (participant, rule_num, day))
#     result = c.fetchone()
#     conn.close()
#     if result:
#         return result[0]
#     else:
#         return 0

# def participant_tracker(participant_name):
#     st.subheader(f"Tracker for {participant_name}")
#     day_date = datetime.now().strftime('%Y-%m-%d')
#     st.write(f"Day {day_date}:")
#     rule1_checked = st.checkbox(f"Rule 1: Follow a diet (No cheat meals, No alcohol)", value=get_checkbox_status(participant_name, 1, day_date))
#     save_checkbox_status(participant_name, 1, day_date, 1 if rule1_checked else 0)
    
#     rule2_checked = st.checkbox(f"Rule 2: Drink 1 gallon (3.7 liters) of water", value=get_checkbox_status(participant_name, 2, day_date))
#     save_checkbox_status(participant_name, 2, day_date, 1 if rule2_checked else 0)
    
#     rule3_checked = st.checkbox(f"Rule 3: Exercise twice a day, at least 45 minutes each time", value=get_checkbox_status(participant_name, 3, day_date))
#     save_checkbox_status(participant_name, 3, day_date, 1 if rule3_checked else 0)
    
#     rule4_checked = st.checkbox(f"Rule 4: Read 10 pages of non-fiction/self-help book", value=get_checkbox_status(participant_name, 4, day_date))
#     save_checkbox_status(participant_name, 4, day_date, 1 if rule4_checked else 0)
    
#     rule5_checked = st.checkbox(f"Rule 5: Take a progress picture", value=get_checkbox_status(participant_name, 5, day_date))
#     save_checkbox_status(participant_name, 5, day_date, 1 if rule5_checked else 0)

#     st.write("---")
        
# def display_progress_graph(participant_name):
#     conn = sqlite3.connect("75hard.db")
#     c = conn.cursor()
#     c.execute('''SELECT day, SUM(checked) FROM progress WHERE participant=? GROUP BY day''', (participant_name,))
#     result = c.fetchall()
#     conn.close()
    
#     df = pd.DataFrame()
#     dates = [r[0] for r in result]
#     progress = [r[1] for r in result]
#     df['date'] = dates
#     df['progress'] = progress
#     df['participant'] = participant_name
    
#     st.subheader(f"Progress Graph for {participant_name}")
#     st.line_chart(data=df, x='date' ,y='progress', use_container_width=True)
#     st.dataframe(df)

# # Main function to display the tracker for both participants
# def main():
#     create_table_if_not_exists()
#     st.title("75 Hard Challenge Tracker")
#     participant1 = "Charlie"
#     participant2 = "Oliwia"
#     participant = st.radio("Hey :)",[participant1,participant2])
    
#     participant_tracker(participant)
#     display_progress_graph(participant1)
#     display_progress_graph(participant2)

# if __name__ == "__main__":
#     main()

import streamlit as st
import csv
from datetime import datetime
import pandas as pd

# Function to load data from CSV file
def load_data():
    try:
        with open("75hard.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            data = {row["participant"]: {row["day"]: {f"rule_{i}": int(row[f"rule_{i}"]) for i in range(1, 7)}} for row in reader}
    except FileNotFoundError:
        data = {}
    return data

# Function to save data to CSV file
def save_data(data):
    with open("75hard.csv", "w", newline="") as file:
        fieldnames = ["participant", "day", "rule_1", "rule_2", "rule_3", "rule_4", "rule_5", "rule_6"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for participant, days in data.items():
            for day, rules in days.items():
                row = {"participant": participant, "day": day}
                row.update({f"rule_{i}": rules.get(f"rule_{i}", 0) for i in range(1, 6)})
                writer.writerow(row)

# Function to update data when checkbox is clicked
def update_data(participant, day, rule_num, checked):
    data = load_data()
    if participant not in data:
        data[participant] = {}
    if day not in data[participant]:
        data[participant][day] = {}
    data[participant][day][f"rule_{rule_num}"] = int(checked)
    save_data(data)

# Function to retrieve checkbox status from data
def get_checkbox_status(participant, day, rule_num):
    data = load_data()
    if participant in data and day in data[participant]:
        return data[participant][day].get(f"rule_{rule_num}", 0)
    else:
        return 0

# Function to display the tracker for one participant
def participant_tracker(participant_name):
    st.subheader(f"Tracker for {participant_name}")
    day_date = datetime.now().strftime('%Y-%m-%d')
    st.write(f"Day {day_date}:")
    for rule_num in ['Healthy diet','1 gallon water','Exercise 1','Exercise 2','Read 10 pages of a book','Progress picture']:
        rule_checked = st.checkbox(f"Rule {rule_num}: ", key=f"{participant_name}_rule{rule_num}_{day_date}", value=get_checkbox_status(participant_name, day_date, rule_num))
        update_data(participant_name, day_date, rule_num, rule_checked)

# Function to display progress graph
def display_progress_graph(participant_name):
    data = load_data()
    if participant_name in data:
        df = pd.DataFrame(data[participant_name], orient='index')
        df.index.name = 'Date'
        st.subheader(f"Progress Graph for {participant_name}")
        st.line_chart(df.sum(axis=1), use_container_width=True)
        st.dataframe(df)

# Main function to display the tracker and progress graph for both participants
def main():
    st.title("75 Hard Challenge Tracker")
    participant1 = "Charlie"
    participant2 = "Oliwia"
    participant = st.radio("Hey :)", [participant1, participant2])
    
    participant_tracker(participant)
    display_progress_graph(participant1)
    display_progress_graph(participant2)

if __name__ == "__main__":
    main()