import streamlit as st
import pandas as pd
import pymssql

###############################################################################
# 1. Utility Functions
###############################################################################
@st.cache_resource
def init_connection(server, user, password, database):
    """Initialize and return a pymssql connection."""
    return pymssql.connect(server, user, password, database)

def run_query(conn, query):
    """Execute a SQL query; return the result as a DataFrame."""
    with conn.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(data, columns=columns)

def compare_two_tables(conn,
                       table1, table2,
                       group_col,         # e.g. 'rdsurf', 'CrashRate'
                       colname1, colname2):
    """
    Query table1 and table2, grouping by group_col, then join side-by-side 
    for a grouped bar chart. 
    """
    q1 = f"SELECT {group_col}, COUNT(*) AS {colname1} FROM {table1} GROUP BY {group_col}"
    q2 = f"SELECT {group_col}, COUNT(*) AS {colname2} FROM {table2} GROUP BY {group_col}"

    df1 = run_query(conn, q1).set_index(group_col)
    df2 = run_query(conn, q2).set_index(group_col)

    # Merge the two dataframes on the group_col index
    df_merged = df1.join(df2, how="outer")  # outer join in case some categories don't overlap
    return df_merged

###############################################################################
# 2. Main Streamlit App
###############################################################################
def main():
    st.title("Rear-End Collision Analysis (Best Practice Visualizations)")

    # -------------------------------------------------------------------------
    # A) Database Credentials
    # -------------------------------------------------------------------------
    st.subheader("Enter Database Credentials")
    username = st.text_input("Username:", value="WI25_ash209")
    password = st.text_input("Password:", type="password", value="Aarshpatel0101")
    database = st.text_input("Database:", value="WI25_T10")
    server   = "128.95.29.66"

    if st.button("Connect to DB"):
        if username and password and database:
            try:
                st.session_state["conn"] = init_connection(server, username, password, database)
                st.success(f"Connected to {database} on {server}!")
            except Exception as e:
                st.error(f"Failed to connect: {e}")
        else:
            st.warning("Please fill in username, password, and database name.")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # B) Compare WetRoad vs DryRoad by rdsurf
    # -------------------------------------------------------------------------
    st.subheader("Compare WetRoad vs DryRoad (Grouped Bar Chart by `rdsurf`)")
    st.write(
        "This shows how collisions in **WetRoad** vs. **DryRoad** differ across each `rdsurf` value."
    )

    if st.button("Show Wet vs Dry Bar Chart"):
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                # Use the helper to get side-by-side data
                df_wet_dry = compare_two_tables(
                    conn,
                    table1="WetRoad",
                    table2="DryRoad",
                    group_col="rdsurf",
                    colname1="Collisions_Wet",
                    colname2="Collisions_Dry"
                )
                st.write("Grouped Bar Chart (x-axis is `rdsurf` categories)")
                st.bar_chart(df_wet_dry)
            except Exception as e:
                st.error(f"Error comparing WetRoad vs DryRoad: {e}")
        else:
            st.warning("Connect to the database first.")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # C) Compare AndYounger vs AndOlder by CrashRate
    # -------------------------------------------------------------------------
    st.subheader("Compare AndYounger vs AndOlder (Grouped Bar Chart by `CrashRate`)")
    st.write(
        "This shows how collisions in **AndYounger** vs. **AndOlder** differ across each `CrashRate` value."
    )

    if st.button("Show Younger vs Older Bar Chart"):
        if "conn" in st.session_state:
            conn = st.session_state["conn"]
            try:
                df_young_old = compare_two_tables(
                    conn,
                    table1="AndYounger",
                    table2="AndOlder",
                    group_col="CrashRate",
                    colname1="Collisions_Younger",
                    colname2="Collisions_Older"
                )
                st.write("Grouped Bar Chart (x-axis is `CrashRate` categories)")
                st.bar_chart(df_young_old)
            except Exception as e:
                st.error(f"Error comparing AndYounger vs AndOlder: {e}")
        else:
            st.warning("Connect to the database first.")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # D) Hypotheses & Additional Analysis Info
    # -------------------------------------------------------------------------
    st.subheader("Hypotheses")
    st.markdown(
        """
        1. **Wet road surfaces lead to more rear-end collisions**  
        2. **Higher speed limits correlate with increased accident severity**  
        3. **Younger drivers (under 25) are more likely to be involved**
        """
    )

    st.subheader("Interpretation of Results")
    st.write(
        """
        Using grouped bar charts, we can easily compare the distribution of collisions
        in each category. For example, if you see that 'WET' is higher in WetRoad vs. DryRoad,
        that aligns with our hypothesis that wet road surfaces increase collision frequency.
        
        Similarly, if certain CrashRate categories are more prominent among Younger vs. Older drivers,
        it informs us about which demographic might require more targeted safety measures.
        """
    )

if __name__ == "__main__":
    main()
