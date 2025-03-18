import streamlit as st
import pandas as pd
import pymssql

# Cache the DB connection to avoid reconnecting on every widget update
@st.cache_resource
def init_connection(server, user, password, database):
    """
    Initialize and return a pymssql connection.
    """
    conn = pymssql.connect(server, user, password, database)
    return conn

def run_query(conn, query):
    """
    Executes a query using an existing pymssql connection,
    and returns the result in a pandas DataFrame.
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    return pd.DataFrame(data, columns=columns)

def main():
    st.title("Data Analysis & Interpretation")

    # ------------------------------------------------------------
    # 1. Database credentials
    # ------------------------------------------------------------
    st.subheader("Enter Database Credentials")

    # Default values set to your credentials
    username = st.text_input("Enter username:", value="WI25_ash209")
    password = st.text_input("Enter a password:", type="password", value="Aarshpatel0101")
    database = st.text_input("Enter your SQL Server database:", value="WI25_T10")
    server = "128.95.29.66"  # Hard-coded

    # Button to initialize the connection
    if st.button("Connect to DB"):
        if username and password and database:
            try:
                st.session_state["conn"] = init_connection(server, username, password, database)
                st.success(f"Successfully connected to {database} on {server}!")
            except Exception as e:
                st.error(f"Failed to connect: {e}")
        else:
            st.warning("Please enter username, password, and database name.")

    # ------------------------------------------------------------
    # 2. Table Selection + Sample Query
    # ------------------------------------------------------------
    st.subheader("Choose a Table to Query")
    table = st.selectbox(
        "Which table would you like to connect to?",
        ("wa17acc", "wa17rdsurf", "wa17rdsurf_ur", "wa17county")
    )

    if st.button("Preview Table (First 10 Rows)"):
        # Check if a connection is in st.session_state
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                query = f"SELECT TOP 10 * FROM {table}"
                df = run_query(conn, query)
                st.dataframe(df)
            except Exception as e:
                st.error(f"Query failed: {e}")
        else:
            st.warning("You need to connect to the database first.")

    # ------------------------------------------------------------
    # 3. Hypotheses & Data Analysis Text
    # ------------------------------------------------------------
    st.subheader("Hypotheses")
    st.markdown(
        """
        1. **Wet road surfaces lead to more rear-end collisions** 
