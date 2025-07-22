import streamlit as st
import sqlite3

# Connect to database
conn = sqlite3.connect('dating_app.db')
c = conn.cursor()

# Create user table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        looking_for TEXT,
        bio TEXT
    )
''')
conn.commit()

# Title
st.title("💘 Simple Dating App")

menu = ["Register", "Browse"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create Your Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    looking_for = st.selectbox("Looking for", ["Male", "Female", "Other"])
    bio = st.text_area("Short Bio")

    if st.button("Submit"):
        if name and bio:
            c.execute("INSERT INTO users (name, age, gender, looking_for, bio) VALUES (?, ?, ?, ?, ?)",
                      (name, age, gender, looking_for, bio))
            conn.commit()
            st.success("Profile created!")
        else:
            st.error("Name and Bio are required.")

elif choice == "Browse":
    st.subheader("Browse Matches")
    selected_gender = st.selectbox("Show users looking for:", ["Male", "Female", "Other"])
    c.execute("SELECT name, age, gender, bio FROM users WHERE looking_for = ?", (selected_gender,))
    matches = c.fetchall()

    if matches:
        for name, age, gender, bio in matches:
            st.markdown(f"**Name:** {name}")
            st.markdown(f"**Age:** {age}")
            st.markdown(f"**Gender:** {gender}")
            st.markdown(f"**Bio:** {bio}")
            st.markdown("---")
    else:
        st.info("No matches found.")
