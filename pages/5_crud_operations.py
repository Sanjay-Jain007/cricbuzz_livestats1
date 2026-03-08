import streamlit as st
import sqlite3
import pandas as pd

st.title("🛠 Player CRUD Operations")

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# -----------------------
# MODE SELECTOR
# -----------------------

mode = st.selectbox(
    "Select Operation",
    ["View","Create","Update","Delete"]
)

# -----------------------
# VIEW PLAYERS
# -----------------------

if mode == "View":

    st.subheader("All Players")

    df = pd.read_sql_query("SELECT * FROM players", conn)

    st.dataframe(df)

# -----------------------
# CREATE PLAYER
# -----------------------

elif mode == "Create":

    st.subheader("Add New Player")

    player_id = st.number_input("Player ID", step=1)

    name = st.text_input("Player Name")
    country = st.text_input("Country")
    role = st.text_input("Role")
    bat = st.text_input("Batting Style")
    bowl = st.text_input("Bowling Style")

    if st.button("Add Player"):

        cursor.execute("""
        INSERT INTO players
        (player_id,name,country,role,batting_style,bowling_style)
        VALUES (?,?,?,?,?,?)
        """,(player_id,name,country,role,bat,bowl))

        conn.commit()

        st.success("Player added successfully")

# -----------------------
# UPDATE PLAYER
# -----------------------

elif mode == "Update":

    st.subheader("Update Player")

    player_id = st.number_input("Player ID to Update", step=1)

    new_country = st.text_input("New Country")
    new_role = st.text_input("New Role")

    if st.button("Update Player"):

        cursor.execute("""
        UPDATE players
        SET country=?, role=?
        WHERE player_id=?
        """,(new_country,new_role,player_id))

        conn.commit()

        st.success("Player updated")

# -----------------------
# DELETE PLAYER
# -----------------------

elif mode == "Delete":

    st.subheader("Delete Player")

    player_id = st.number_input("Player ID to Delete", step=1)

    if st.button("Delete Player"):

        cursor.execute("""
        DELETE FROM players
        WHERE player_id=?
        """,(player_id,))

        conn.commit()

        st.warning("Player deleted")

conn.close()
