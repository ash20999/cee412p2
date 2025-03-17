import streamlit as st
from PIL import Image

def main():
    st.title("Dataset & Data Management Plan")

    st.subheader("Dataset Overview")
    st.write(
        """
        We used the HSIS dataset for major Washington State freeways (I-5, I-90, I-405, and SR-520).
        It includes accident characteristics (location, date/time, etc.), roadway features (speed limits,
        AADT, surface conditions), and vehicle/driver details.
        """
    )

    st.subheader("Limitations")
    st.write(
        """
        - Potential missing or erroneous records (e.g., unknown driver ages).
        - Differences in data dictionary between 2002 and 2013-2017, requiring standardization.
        - Not all freeways or collision types are equally represented.
        """
    )

    st.subheader("E/R Diagram")
    st.write("Below is our conceptual E/R diagram illustrating the relationships:")
    # Example: If you have an image of the E/R diagram
    # E/R diagram should have entities: Accident, Road, Vehicle, Driver
    # Make sure "pages/2_Dataset.py" is referencing your actual diagram file path.
    # diagram = Image.open("data/er_diagram.png")
    # st.image(diagram, caption='E/R Diagram for Rear-End Collision Database')

    st.write(
        """
        **Accident**: CASENO, Date, Weather, Road_Condition  
        **Road**: GPSX, GPSY, Route, Surface_Type, Speed_Limit, AADT  
        **Vehicle**: VEHICLE_ID, ACCIDENT_ID, Vehicle_Type, Vehicle_Condition  
        **Driver**: LICENSENUMBER, Age, Impaired, Sex  
        
        We designed the database to meet BCNF by ensuring each table references primary keys
        (e.g., CASENO for accidents). This reduces redundancy and supports efficient queries.
        """
    )

    st.subheader("Data Management Plan")
    st.markdown(
        """
        - Data stored in a SQL database (Microsoft SQL Server).
        - Regular backups and versioning.
        - Anomalies (duplicates, missing data) are identified and resolved before analysis.
        - Road updates are added as new entries rather than overwriting historical data.
        """
    )

if __name__ == "__main__":
    main()
