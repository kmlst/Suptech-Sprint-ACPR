import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("../fake_data.csv")

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    st.title("Test Dashboard")

    data = load_data()

    # Sidebar for selecting fields
    st.sidebar.header("Select Fields and Apply Filters")
    numerical_fields = st.sidebar.multiselect("Select Numerical Fields", data.select_dtypes(include=['float64', 'int64']).columns, key='col_select')
    categorical_fields = st.sidebar.multiselect("Select Categorical Fields", data.select_dtypes(include=['object']).columns, key = 'col_cat_select')
    filter_values = {}
    for field in numerical_fields:
        filter_type = st.sidebar.radio(f"Filter type for {field}", ["Greater than", "Smaller than", "Equal to"])
        if filter_type == "Greater than":
            filter_values[field] = st.sidebar.number_input(f"Filter {field}", step=0.1)
        elif filter_type == "Smaller than":
            filter_values[field] = st.sidebar.number_input(f"Filter {field}", step=0.1)
        else:
            filter_values[field] = st.sidebar.number_input(f"Filter {field}", step=0.1)
    for field in categorical_fields:
        filter_values[field] = st.sidebar.multiselect(f"Filter {field}", data[field].unique(), key='categories')

    # Apply filters
    filtered_data = data.copy()
    for field, value in filter_values.items():
        if value:
            if field in numerical_fields:
                if "Greater than" in filter_values[field]:
                    filtered_data = filtered_data[filtered_data[field] > value]
                elif "Smaller than" in filter_values[field]:
                    filtered_data = filtered_data[filtered_data[field] < value]
                else:
                    filtered_data = filtered_data[filtered_data[field] == value]
            else:
                filtered_data = filtered_data[filtered_data[field].isin(value)]


       # Display selected fields
    if numerical_fields or categorical_fields:
        selected_columns = numerical_fields + categorical_fields
        st.subheader("Selected Columns")
        st.write(selected_columns)
        
        st.subheader("Data Visualizations")

        # Display plots side by side in two columns
        num_plots = len(numerical_fields) + len(categorical_fields)
        num_cols = 2
        num_rows = -(-num_plots // num_cols)  # Ceiling division to calculate number of rows needed

        with st.container():
            fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
            axes = axes.flatten()

            # Plot numerical fields using Plotly
        if numerical_fields:
            num_cols = 2
            for i in range(0, len(numerical_fields), num_cols):
                cols = st.columns(num_cols)
                for j, field in enumerate(numerical_fields[i:i+num_cols]):
                    fig = px.histogram(data, x=field, title=f"{field} Distribution")
                    cols[j].plotly_chart(fig)

        # Plot categorical fields using Plotly
        if categorical_fields:
            num_cols = 2
            for i in range(0, len(categorical_fields), num_cols):
                cols = st.columns(num_cols)
                for j, field in enumerate(categorical_fields[i:i+num_cols]):
                    fig = px.histogram(data, x=field, title=f"{field} Count")
                    fig.update_xaxes(categoryorder="total descending")
                    cols[j].plotly_chart(fig)

            # Hide unused axes
            for j in range(num_plots, len(axes)):
                axes[j].axis('off')

            plt.tight_layout()
            # st.pyplot(fig)

    # Open data record
    st.sidebar.header("Open Data Record")
    selected_index = st.sidebar.number_input("Enter row index to view data record", min_value=0, max_value=len(data)-1, step=1)
    if st.sidebar.button("Open Data Record"):
        st.write(data.iloc[selected_index])

if __name__ == "__main__":
    main()
