import streamlit as st
import pandas as pd
import pymssql

# Cache the DB connection so it doesn't reconnect on every widget update
@st.cache_resource
def init_connection(server, user, password, database):
    """Initialize and return a pymssql connection."""
    return pymssql.connect(server, user, password, database)

def run_query(conn, query):
    """Execute a query on an existing pymssql connection, return a DataFrame."""
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

    # Provide defaults or placeholders
    username = st.text_input("Enter username:", value="WI25_ash209")
    password = st.text_input("Enter a password:", type="password", value="Aarshpatel0101")
    database = st.text_input("Enter your SQL Server database:", value="WI25_T10")
    server = "128.95.29.66"  # Hard-coded; change if needed

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
    # 2. Table Selection
    # ------------------------------------------------------------
    st.subheader("Choose a Table to Query")
    table = st.selectbox(
        "Which table would you like to connect to?",
        ("wa17acc", "wa17rdsurf", "wa17rdsurf_ur", "wa17county")
    )

    # ------------------------------------------------------------
    # 2A. Optional: Preview the table
    # ------------------------------------------------------------
    if st.button("Preview Table (First 10 Rows)"):
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                query = f"SELECT TOP 10 * FROM {table}"
                df = run_query(conn, query)
                st.write(f"Showing first 10 rows from **{table}**:")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Query failed: {e}")
        else:
            st.warning("You need to connect to the database first.")

    # ------------------------------------------------------------
    # 2B. Display a Bar Chart (Pull data in the background)
    # ------------------------------------------------------------
    st.markdown("---")
    st.subheader("Bar Chart Example")

    st.write(
        """
        Below, we run a query to group collisions by `Road_Condition` and 
        display them in a bar chart. The underlying data is retrieved in the background 
        and **not** displayed as a DataFrame.
        """
    )

    if st.button("Show Bar Chart"):
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                # Example query that groups by a "Road_Condition" column
                query = f"""
                SELECT Road_Condition, COUNT(*) AS Collisions
                FROM {table}
                GROUP BY Road_Condition
                """
                df_chart = run_query(conn, query)

                # If the table doesn't have "Road_Condition", this will fail.
                # Adjust the column name(s) if needed.
                df_chart = df_chart.set_index("Road_Condition")
                st.bar_chart(df_chart["Collisions"])

            except Exception as e:
                st.error(
                    "Could not display bar chart for the selected table. "
                    f"Check if 'Road_Condition' exists in {table}.\n\nError: {e}"
                )
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
        3. **Younger drivers (under 25) are more likely to be involved**
        """
    )

    st.subheader("Exploratory Data Analysis")
    st.write("Here, we might visualize collisions by road condition, driver age, etc.")

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
