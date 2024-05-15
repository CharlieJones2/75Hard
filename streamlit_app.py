import streamlit as st
import datetime as dt

# Function to display the tracker for one participant
def participant_tracker():
    #for day in range(1, 76):
    st.write(f"Day {dt._Date.today()}:")
    st.checkbox(f"Follow a diet (Whole foods, healthy meals ONLY)", key=f"rule1_{dt._Date.today()}")
    st.checkbox(f"Drink 1 gallon (3.7 liters) of water", key=f"rule2_{dt._Date.today()}")
    st.checkbox(f"First 45 minute exercise", key=f"rule3_{dt._Date.today()}")
    st.checkbox(f"Second 45 minute exercise", key=f"rule3_{dt._Date.today()}")
    st.checkbox(f"Read 10 pages of a book", key=f"rule4_{dt._Date.today()}")
    st.checkbox(f"Take a progress picture", key=f"rule5_{dt._Date.today()}")
    st.write("---")

# Main function to display the tracker for both participants
def main():
    st.title("75 Hard Challenge Tracker")
    participant_tracker()

if __name__ == "__main__":
    main()