import streamlit as st
import sqlite3
from datetime import datetime, date, time

# Initialize database connection
conn = sqlite3.connect('bookings.db')
c = conn.cursor()

# Create bookings table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        court TEXT,
        booking_date TEXT,
        start_time TEXT,
        end_time TEXT,
        booked_by TEXT
    )
''')
conn.commit()

# List of courts
COURTS = ['Court 1', 'Court 2', 'Court 3', 'Court 4']

def get_available_slots(selected_court, selected_date):
    """
    Return list of available time slots for a given court and date.
    """
    # Define full day slots: 8am-9pm hourly
    slots = [(time(h, 0), time(h+1, 0)) for h in range(8, 21)]
    c.execute(
        "SELECT start_time, end_time FROM bookings WHERE court = ? AND booking_date = ?",
        (selected_court, selected_date)
    )
    taken = c.fetchall()
    # Filter out taken slots
    available = []
    for s, e in slots:
        s_str, e_str = s.strftime('%H:%M'), e.strftime('%H:%M')
        if not any(s_str == t0 and e_str == t1 for t0, t1 in taken):
            available.append((s_str, e_str))
    return available

def book_slot(court, booking_date, start_time, end_time, user):
    """
    Insert a new booking into the database.
    """
    c.execute(
        "INSERT INTO bookings (court, booking_date, start_time, end_time, booked_by) VALUES (?, ?, ?, ?, ?)",
        (court, booking_date, start_time, end_time, user)
    )
    conn.commit()

# Streamlit UI
st.title("🏸 Badminton Court Booking App")

# User input
user_name = st.text_input("Your Name")
selected_court = st.selectbox("Select Court", COURTS)
selected_date = st.date_input("Select Date", min_value=date.today())

# Show available slots
available = get_available_slots(selected_court, selected_date.strftime('%Y-%m-%d'))
if available:
    slot_choice = st.selectbox("Choose Time Slot", [f"{s} - {e}" for s, e in available])
    if st.button("Book Now"):
        start, end = slot_choice.split(' - ')
        if user_name:
            book_slot(selected_court, selected_date.strftime('%Y-%m-%d'), start, end, user_name)
            st.success(f"Booked {selected_court} on {selected_date} from {start} to {end} for {user_name}.")
        else:
            st.error("Please enter your name before booking.")
else:
    st.info("No available slots for this court on the selected date.")

# Display existing bookings for admin overview
if st.checkbox("Show All Bookings"):
    c.execute("SELECT court, booking_date, start_time, end_time, booked_by FROM bookings ORDER BY booking_date, start_time")
    rows = c.fetchall()
    st.table(rows)
