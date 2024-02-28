import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("output/bdd_DIC.csv")

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    st.title("Test Dashboard")

    data = load_data()

    # Sidebar for selecting fields
    st.sidebar.header("Select Fields")
    numerical_fields = st.sidebar.multiselect("Select Numerical Fields", data.select_dtypes(include=['float64', 'int64']).columns)
    categorical_fields = st.sidebar.multiselect("Select Categorical Fields", data.select_dtypes(include=['object']).columns)

    # Display selected fields
    if numerical_fields or categorical_fields:
        st.subheader("Data Visualizations")

        # Display plots side by side in two columns
        num_plots = len(numerical_fields) + len(categorical_fields)
        num_cols = 2
        num_rows = -(-num_plots // num_cols)  # Ceiling division to calculate number of rows needed

        with st.container():
            for i, field in enumerate(numerical_fields):
                if i % num_cols == 0:
                    col1, col2 = st.columns(2)
                fig = plt.figure()
                sns.histplot(data[field], kde=True)
                col1.pyplot(fig)

            for i, field in enumerate(categorical_fields):
                if i % num_cols == 0:
                    col1, col2 = st.columns(2)
                fig = plt.figure()
                sns.countplot(data[field])
                plt.xticks(rotation=45)
                col2.pyplot(fig)

    # Open data record
    st.sidebar.header("Open Data Record")
    selected_index = st.sidebar.number_input("Enter row index to view data record", min_value=0, max_value=len(data)-1, step=1)
    if st.sidebar.button("Open Data Record"):
        st.write(data.iloc[selected_index])

if __name__ == "__main__":
    main()
