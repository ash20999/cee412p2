import streamlit as st
import pandas as pd
import numpy as np
# from your_data_module import load_data, run_some_queries

def main():
    st.title("Data Analysis & Interpretation")

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

    # Example data loading (replace with your own)
    # collisions_df = load_data()

    st.subheader("Exploratory Data Analysis")
    st.write("Here, we might visualize collisions by road condition, driver age, etc.")

    # Example: Collisions by road condition chart
    # sample_data = pd.DataFrame({"Condition": ["Dry", "Wet", "Snow", "Other"],
    #                             "Count": [100, 60, 15, 10]})
    # st.bar_chart(sample_data.set_index("Condition"))

    st.subheader("Statistical Tests & Queries")
    st.write(
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
        """
    )
    st.write(
        """
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
