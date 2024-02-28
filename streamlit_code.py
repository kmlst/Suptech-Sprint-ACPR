import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

NOM_CHAMP_MECA = '20. Résumé du mécanisme'
COL_INDEX = "1. le code ISIN du produit"
NAME_COL = "2. Le nom du produit"

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("../Exemples + résumés méca.xlsx").set_index(COL_INDEX)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def new_tab(data):
    st.title("Bienvenue sur Very'DIC ! .")
    # Open data record
    st.sidebar.header("Open Data record")
    selected_index = st.sidebar.multiselect("Select ISIN", list(data.index))
    if st.sidebar.button("Open Data Record"):
        get_record(data, selected_index)


def get_record(data, selected_index):
    st.subheader(f'Résumé pour {selected_index}, {data.loc[selected_index, NAME_COL]}')
    # with st.expander('Resume'):
    st.text(data.loc[selected_index, NOM_CHAMP_MECA][0])


def dashboard(data):
    st.title("Synthèse DIC")

    # Sidebar for selecting fields
    st.sidebar.header("Select Fields and Apply Filters")
    
    numerical_fields = st.sidebar.multiselect("Select Numerical Fields", data.select_dtypes(include=['float64', 'int64']).columns, key='col_select')
    categorical_fields = st.sidebar.multiselect("Select Categorical Fields", data.select_dtypes(include=['object']).columns, key = 'col_cat_select')
    # Remove resume that is a special field
    # categorical_fields.remove(NOM_CHAMP_MECA)
    filter_values = {}
    for field in numerical_fields:
        filter_type = st.sidebar.radio(f"Filter type for {field}", ["Greater than", "Smaller than", "Equal to"])
        filter_values[field] = {}
        if filter_type == "Greater than":
            filter_values[field]['sign'] = 'Greater than'
            filter_values[field]['value'] = st.sidebar.number_input(f"Filter {field}", step=0.1)
        elif filter_type == "Smaller than":
            filter_values[field]['sign'] = 'Smaller than'
            filter_values[field]['value'] = st.sidebar.number_input(f"Filter {field}", step=0.1)
        else:
            filter_values[field]['sign'] = 'Equal'
            filter_values[field]['value'] = st.sidebar.number_input(f"Filter {field}", step=0.1)

    for field in categorical_fields:
        filter_values[field] = st.sidebar.multiselect(f"Filter {field}", data[field].unique(), key='categories')

    # Apply filters
    filtered_data = data.copy()
    for field, value in filter_values.items():
        if value:
            if field in numerical_fields:
                if "Greater than" in filter_values[field]['sign']:
                    filtered_data = filtered_data[filtered_data[field] > value['value']]
                elif "Smaller than" in filter_values[field]['sign']:
                    filtered_data = filtered_data[filtered_data[field] < value['value']]
                else:
                    filtered_data = filtered_data[filtered_data[field] == value['value']]
            else:
                filtered_data = filtered_data[filtered_data[field].isin(value)]


    # Display selected fields
    # Download filtered CSV
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download filtered data CSV file", data=csv, file_name="filtered_data.csv", mime="text/csv")
    # Display IDs of filtered rows
    if len(filtered_data) < len(data):
        st.subheader("Filtered Rows IDs")
        st.write(filtered_data.index.tolist())

    if numerical_fields or categorical_fields:
        selected_columns = numerical_fields + categorical_fields
       
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
                    fig = px.histogram(filtered_data, x=field, title=f"{field} Distribution")
                    cols[j].plotly_chart(fig)

        # Plot categorical fields using Plotly
        if categorical_fields:
            num_cols = 2
            for i in range(0, len(categorical_fields), num_cols):
                cols = st.columns(num_cols)
                for j, field in enumerate(categorical_fields[i:i+num_cols]):
                    fig = px.histogram(filtered_data, x=field, title=f"{field} Count")
                    fig.update_xaxes(categoryorder="total descending")
                    cols[j].plotly_chart(fig)

            # Hide unused axes
            for j in range(num_plots, len(axes)):
                axes[j].axis('off')

            plt.tight_layout()
            # st.pyplot(fig)


def switch_to_tab(tab_name):
    # Update URL query parameters to switch tabs
    st.query_params["tab"] = tab_name


if __name__ == "__main__":
    
    data = load_data()
    # Get current tab from URL query parameters
    # current_tab = st.query_params().get("tab", ["Summary"])[0]

    # Create tabs for navigation
    # tab1, tab2 = st.tabs(["📈 Summary", "🗃 Data"])
    # with tab1:
    #     dashboard(data)
    # with tab2:
    #     new_tab(data)

    # Create a layout with two columns for the buttons
    col1, col2 = st.columns(2)

    # Create buttons to switch tabs
    with col1:
        if st.button("Go to Summary"):
            switch_to_tab("Summary")
    with col2:
        if st.button("Go to Data"):
            switch_to_tab("Data")

    current_tab = st.query_params["tab"]

    # Display content based on current tab
    if current_tab == "Summary":
        dashboard(data)
    elif current_tab == "Data":
        new_tab(data)



