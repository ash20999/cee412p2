import streamlit as st
import pandas as pd
import pymssql

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
    # Added four new table entries: AndYounger, AndOlder, Wetroad, DryRoad
    table = st.selectbox(
        "Which table would you like to connect to?",
        (
            "wa17acc",
            "wa17rdsurf",
            "wa17rdsurf_ur",
            "wa17county",
            "AndYounger",
            "AndOlder",
            "Wetroad",
            "DryRoad"
        )
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
        Below, we run a query to group collisions by `rdsurf` and 
        display them in a bar chart. The underlying data is retrieved in the background 
        and **not** displayed as a DataFrame.
        
        NOTE: The table must have a column called `rdsurf` for this to work.
        """
    )

    if st.button("Show Bar Chart"):
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                # Query grouping by rdsurf
                query = f"""
                SELECT rdsurf, COUNT(*) AS Collisions
                FROM {table}
                GROUP BY rdsurf
                """
                df_chart = run_query(conn, query)

                # Setting the index to rdsurf
                df_chart = df_chart.set_index("rdsurf")
                st.bar_chart(df_chart["Collisions"])

            except Exception as e:
                st.error(
                    "Could not display bar chart for the selected table. "
                    f"Check if 'rdsurf' exists in {table}.\n\nError: {e}"
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
        SELECT rdsurf, COUNT(*) AS Collision_Count
        FROM wa17rdsurf
        GROUP BY rdsurf
        ORDER BY Collision_Count DESC;
        ```
        Based on these queries, we observed that **wet conditions** (rdsurf='WET') indeed show a higher
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
