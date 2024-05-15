import streamlit as st

# Function to display the tracker for one participant
def participant_tracker(participant_name):
    st.subheader(f"Tracker for {participant_name}")
    for day in range(1, 76):
        st.write(f"Day {day}:")
        st.checkbox(f"Rule 1: Follow a diet (No cheat meals, No alcohol)", key=f"{participant_name}_rule1_{day}")
        st.checkbox(f"Rule 2: Drink 1 gallon (3.7 liters) of water", key=f"{participant_name}_rule2_{day}")
        st.checkbox(f"Rule 3: Exercise twice a day, at least 45 minutes each time", key=f"{participant_name}_rule3_{day}")
        st.checkbox(f"Rule 4: Read 10 pages of non-fiction/self-help book", key=f"{participant_name}_rule4_{day}")
        st.checkbox(f"Rule 5: Take a progress picture", key=f"{participant_name}_rule5_{day}")
        st.write("---")

# Main function to display the tracker for both participants
def main():
    st.title("75 Hard Challenge Tracker")
    participant1 = st.text_input("Participant 1 Name:")
    participant2 = st.text_input("Participant 2 Name:")
    
    if participant1 and participant2:
        participant_tracker(participant1)
        participant_tracker(participant2)

if __name__ == "__main__":
    main()