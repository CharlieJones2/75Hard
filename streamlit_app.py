import streamlit as st
from datetime import datetime
import sqlite3

def create_table_if_not_exists():
    conn = sqlite3.connect("75hard.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY,
                    participant TEXT,
                    rule_num INTEGER,
                    day DATE,
                    checked INTEGER
                )''')
    conn.commit()
    conn.close()
    
def save_checkbox_status(participant, rule_num, day, checked):
    conn = sqlite3.connect("75hard.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM progress WHERE participant=? AND rule_num=? AND day=?''', (participant, rule_num, day))
    result = c.fetchone()
    if result:
        c.execute('''UPDATE progress SET checked=? WHERE participant=? AND rule_num=? AND day=?''', (checked, participant, rule_num, day))
    else:
        c.execute('''INSERT INTO progress (participant, rule_num, day, checked) VALUES (?, ?, ?, ?)''', (participant, rule_num, day, checked))
    conn.commit()
    conn.close()
    
def get_checkbox_status(participant, rule_num, day):
    conn = sqlite3.connect("75hard.db")
    c = conn.cursor()
    c.execute('''SELECT checked FROM progress WHERE participant=? AND rule_num=? AND day=?''', (participant, rule_num, day))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return 0

def participant_tracker(participant_name):
    st.subheader(f"Tracker for {participant_name}")
    day_date = datetime.now().strftime('%Y-%m-%d')
    st.write(f"Day {day_date}:")
    rule1_checked = st.checkbox(f"Rule 1: Follow a diet (No cheat meals, No alcohol)", value=get_checkbox_status(participant_name, 1, day_date))
    save_checkbox_status(participant_name, 1, day_date, 1 if rule1_checked else 0)
    
    rule2_checked = st.checkbox(f"Rule 2: Drink 1 gallon (3.7 liters) of water", value=get_checkbox_status(participant_name, 2, day_date))
    save_checkbox_status(participant_name, 2, day_date, 1 if rule2_checked else 0)
    
    rule3_checked = st.checkbox(f"Rule 3: Exercise twice a day, at least 45 minutes each time", value=get_checkbox_status(participant_name, 3, day_date))
    save_checkbox_status(participant_name, 3, day_date, 1 if rule3_checked else 0)
    
    rule4_checked = st.checkbox(f"Rule 4: Read 10 pages of non-fiction/self-help book", value=get_checkbox_status(participant_name, 4, day_date))
    save_checkbox_status(participant_name, 4, day_date, 1 if rule4_checked else 0)
    
    rule5_checked = st.checkbox(f"Rule 5: Take a progress picture", value=get_checkbox_status(participant_name, 5, day_date))
    save_checkbox_status(participant_name, 5, day_date, 1 if rule5_checked else 0)

    st.write("---")
        
def display_progress_graph(participant_name):
    conn = sqlite3.connect("75hard.db")
    c = conn.cursor()
    c.execute('''SELECT day, SUM(checked) FROM progress WHERE participant=? GROUP BY day''', (participant_name,))
    result = c.fetchall()
    conn.close()
    
    dates = [r[0] for r in result]
    progress = [r[1] for r in result]
    
    st.subheader(f"Progress Graph for {participant_name}")
    st.line_chart(y=progress, x=dates, use_container_width=True)

# Main function to display the tracker for both participants
def main():
    create_table_if_not_exists()
    st.title("75 Hard Challenge Tracker")
    participant1 = "Charlie"
    participant2 = "Oliwia"
    participant = st.radio("Hey :)",[participant1,participant2])
    
    participant_tracker(participant)
    display_progress_graph(participant1)
    display_progress_graph(participant2)

if __name__ == "__main__":
    main()