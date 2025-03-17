import streamlit as st

def main():
    st.title("Project Summary & Next Steps")
    st.write(
        """
        **Key Takeaways**:
        - Wet roads significantly increase the likelihood of rear-end collisions.
        - Higher speed limits correlate with greater collision severity.
        - Traffic volume (AADT) strongly influences collision frequency.
        - Younger drivers may benefit from targeted safety interventions.

        **Future Recommendations**:
        - Implement adaptive speed limits on wet roads.
        - Consider additional driver education programs for younger motorists.
        - Evaluate infrastructure improvements to reduce congestion on high-AADT freeways.

        Thank you for exploring our Streamlit app! We hope this analysis guides
        future safety initiatives on Washington’s freeways.
        """
    )

if __name__ == "__main__":
    main()
