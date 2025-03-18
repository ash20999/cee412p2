import streamlit as st
import pandas as pd
import pymssql

@st.cache_resource
def init_connection(server, user, password, database):
    """Initialize and return a pymssql connection."""
    return pymssql.connect(server, user, password, database)

def run_query(conn, query):
    """Execute a query on an existing pymssql connection; return a DataFrame."""
    with conn.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(data, columns=columns)

def compare_two_tables(conn,
                       table1, table2,
                       group_col,         # e.g. 'rdsurf' or 'ACCTYPE'
                       colname1, colname2):
    """
    Runs a simple group-by query on table1 and table2 using `group_col`,
    merges them side-by-side in one DataFrame, then returns that DataFrame.

    Example usage:
    compare_two_tables(conn,
                       "WetRoad", "DryRoad",
                       group_col="rdsurf",
                       colname1="Collisions_Wet", colname2="Collisions_Dry")
    """
    q1 = f"SELECT {group_col}, COUNT(*) AS {colname1} FROM {table1} GROUP BY {group_col}"
    q2 = f"SELECT {group_col}, COUNT(*) AS {colname2} FROM {table2} GROUP BY {group_col}"

    df1 = run_query(conn, q1).set_index(group_col)
    df2 = run_query(conn, q2).set_index(group_col)

    # Join on the index = the grouping column (e.g., rdsurf or ACCTYPE)
    df_combined = df1.join(df2, how="outer")
    return df_combined

def main():
    st.title("Compare WetRoad/DryRoad and Younger/Older")

    # --------------------------------------
    # 1. Database credentials
    # --------------------------------------
    st.subheader("Enter Database Credentials")
    username = st.text_input("Enter username:", value="WI25_ash209")
    password = st.text_input("Enter a password:", type="password", value="Aarshpatel0101")
    database = st.text_input("Enter your SQL Server database:", value="WI25_T10")
    server = "128.95.29.66"  # Hard-coded; adjust if needed

    if st.button("Connect to DB"):
        if username and password and database:
            try:
                st.session_state["conn"] = init_connection(server, username, password, database)
                st.success(f"Successfully connected to {database} on {server}!")
            except Exception as e:
                st.error(f"Failed to connect: {e}")
        else:
            st.warning("Please enter username, password, and database name.")

    # --------------------------------------
    # 2. Compare Wet vs Dry (by rdsurf)
    # --------------------------------------
    st.subheader("Compare WetRoad vs DryRoad by `rdsurf`")
    st.write(
        "This button retrieves data from **WetRoad** and **DryRoad**, groups by `rdsurf`, "
        "and displays side-by-side bar charts."
    )
    if st.button("Show Wet vs Dry Comparison"):
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                df_wet_dry = compare_two_tables(
                    conn,
                    table1="WetRoad",
                    table2="DryRoad",
                    group_col="rdsurf",            # Group by rdsurf
                    colname1="Collisions_Wet", 
                    colname2="Collisions_Dry"
                )

                # st.dataframe(df_wet_dry)  # Uncomment to see raw numbers
                st.bar_chart(df_wet_dry)
            except Exception as e:
                st.error(f"Error comparing WetRoad vs DryRoad: {e}")
        else:
            st.warning("Connect to the database first.")

    st.markdown("---")

    # --------------------------------------
    # 3. Compare AndYounger vs AndOlder (by ACCTYPE)
    # --------------------------------------
    st.subheader("Compare AndYounger vs AndOlder by `ACCTYPE`")
    st.write(
        "This button retrieves data from **AndYounger** and **AndOlder**, groups by `ACCTYPE`, "
        "and displays side-by-side bar charts."
    )
    if st.button("Show Younger vs Older Comparison"):
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                df_young_old = compare_two_tables(
                    conn,
                    table1="AndYounger",
                    table2="AndOlder",
                    group_col="ACCTYPE",        # Group by ACCTYPE
                    colname1="Collisions_Younger",
                    colname2="Collisions_Older"
                )

                # st.dataframe(df_young_old)  # Uncomment to see raw numbers
                st.bar_chart(df_young_old)
            except Exception as e:
                st.error(f"Error comparing AndYounger vs AndOlder: {e}")
        else:
            st.warning("Connect to the database first.")

    st.markdown("---")

    # --------------------------------------
    # 4. Additional context or content
    # --------------------------------------
    st.subheader("Hypotheses")
    st.markdown(
        """
        1. **Wet road surfaces lead to more rear-end collisions**  
        2. **Higher speed limits correlate with increased accident severity**  
        3. **Younger drivers (under 25) are more likely to be involved**
        """
    )

    st.subheader("Exploratory Data Analysis")
    st.write(
        "We might visualize collisions by road condition, driver age, etc. "
        "Here, we specifically show how rdsurf differs between Wet/Dry tables and how ACCTYPE differs between Younger/Older."
    )

if __name__ == "__main__":
    main()
