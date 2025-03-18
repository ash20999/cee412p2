import streamlit as st
import pandas as pd
import numpy as np
import pymssql

# Optional: for type hints
# from typing import Optional

# -- Caching the DB connection with Streamlit's cache_resource:
@st.cache_resource
def init_connection(server, user, password, database):
    """
    Initialize and return a pymssql connection.
    Caches the connection to avoid re-connecting every run.
    """
    conn = pymssql.connect(server, user, password, database)
    return conn

def run_query(conn, query):
    """
    Given an open connection and a SQL query,
    execute and return results in a DataFrame.
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]  # extract col names
    return pd.DataFrame(data, columns=column_names)

def main():
    st.title("Data Analysis & Interpretation")

    # ------------------------------------------------------------
    # 1. Database credentials
    # ------------------------------------------------------------
    st.subheader("Enter Database Credentials")
    username = st.text_input("Enter username:", placeholder="CEE412_admin")
    password = st.text_input("Enter a password:", type="password", placeholder="Password")
    database = st.text_input("Enter your SQL Server database:", placeholder="Database name", value="WI25_T10")
    server = "128.95.29.66"  # Change if needed

    # Button to initialize the connection
    if st.button("Connect to DB"):
        if username and password and database:
            try:
                st.session_state["conn"] = init_connection(server, username, password, database)
                st.success("Successfully connected to the database!")
            except Exception as e:
                st.error(f"Failed to connect: {e}")
        else:
            st.warning("Please fill in username, password, and database name.")

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
        2. **Higher speed limits correlate with increased accident severity**  
        3. **Freeways with higher AADT experience more frequent rear-end collisions**  
        4. **Younger drivers (under 25) are more likely to be involved**  
        5. **Newer vehicles (under 10 years old) are less likely to crash**
        """
    )

    st.subheader("Exploratory Data Analysis")
    st.write("Here, we might visualize collisions by road condition, driver age, etc.")

    # Example of simple bar chart:
    # sample_data = pd.DataFrame({"Condition": ["Dry", "Wet", "Snow", "Other"],
    #                            "Count": [100, 60, 15, 10]})
    # st.bar_chart(sample_data.set_index("Condition"))

    st.subheader("Statistical Tests & Queries")
    st.markdown(
        """
        We used SQL queries and statistical testing (e.g., chi-square, t-tests, or logistic regression)
        to assess our hypotheses. Example approach:
        
        ```sql
        SELECT Road_Condition, COUNT(*) AS Collision_Count
        FROM Accident
        WHERE ACCTYPE IN ('06','16','13','14','73','74','83','84')
        GROUP BY Road_Condition
        ORDER BY Collision_Count DESC;
        ```
        Based on these queries, we observed that **wet conditions** indeed show a higher
        proportion of rear-end collisions than dry conditions, supporting Hypothesis 1.
        """
    )

    st.subheader("Interpretation of Results")
    st.write(
        """
        Our results suggest speed limits and traffic volume (AADT) are significant factors
        influencing both the frequency and severity of rear-end collisions. Younger drivers,
        while a smaller population, appeared overrepresented in these collisions, highlighting
        the need for targeted driver education.
        """
    )

if __name__ == "__main__":
    main()

