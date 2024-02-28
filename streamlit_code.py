import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

NOM_CHAMP_MECA = 'resume_mecanisme'
COL_INDEX = "code_ISIN"
NAME_COL = "nom_du_produit"

from column_mapping import map_name

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("output/bdd_DIC.csv").set_index(COL_INDEX)

# @st.cache_data
def new_tab(data, selected_index):
    st.title("Détail du produit")
    # Open data record
    get_record(data, selected_index)

# @st.cache_data
def get_record(data, selected_index):
    st.header('Mécanisme du produit')
    st.subheader(f'Résumé pour {selected_index}, {data.loc[selected_index, NAME_COL]}')
    st.markdown(data.loc[selected_index, NOM_CHAMP_MECA])


def apply_filters(data, filter_values):
    numerical_fields = data.select_dtypes(include=['float64', 'int64']).columns
    filtered_data = data.copy()

    for old_field, value in filter_values.items():
        field = old_field
        if value:
            if field in numerical_fields:
                if "Greater than" in filter_values[field]['sign']:
                    filtered_data = filtered_data[filtered_data[field] >= value['value']]
                elif "Smaller than" in filter_values[field]['sign']:
                    filtered_data = filtered_data[filtered_data[field] <= value['value']]
                else:
                    filtered_data = filtered_data[filtered_data[field] == value['value']]
            else:
                filtered_data = filtered_data[filtered_data[field].isin(value)]

    return filtered_data

def dashboard(data):
    st.title("Synthèse DIC")

    # Sidebar for selecting fields
    st.sidebar.header("Select Fields and Apply Filters")
    
    numerical_fields = data.select_dtypes(include=['float64', 'int64']).columns
    categorical_fields = data.select_dtypes(include=['object']).columns

    # Apply filters
    filtered_data = filtered_data = apply_filters(data, filter_values)


    # Display selected fields
    # Download filtered CSV
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download filtered data CSV file", data=csv, file_name="filtered_data.csv", mime="text/csv")
    # Display IDs of filtered rows
    # if len(filtered_data) < len(data):
    #     st.subheader("Filtered Rows IDs")
    #     st.write(filtered_data.index.tolist())

    if all_fields:
        # selected_columns = numerical_fields + categorical_fields
       
        st.subheader("Data Visualizations")

        # Display plots side by side in two columns
        num_plots = len(all_fields)
        num_cols = 2
        num_rows = -(-num_plots // num_cols)  # Ceiling division to calculate number of rows needed

        with st.container():
            fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
            axes = axes.flatten()
            # num_cols = 2
            for i in range(0, len(all_fields), num_cols):
                cols = st.columns(spec=[0.5, 0.5])
                for j, old_field in enumerate(all_fields[i:i+num_cols]):
                    field = list(map_name.keys())[list(map_name.values()).index(old_field)]   
                    if field in numerical_fields:
                        fig = px.histogram(filtered_data, x=field, title=f"{map_name[field]}")
                        cols[j].plotly_chart(fig)
                    else:
                        fig = px.histogram(filtered_data, x=field, title=f"{map_name[field]}")
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
    current_tab = "Summary"

    # Create a layout with two columns for the buttons
    # st.query_params["tab"] = "Summary"    
    col1, col2 = st.columns(2)

    # Create buttons to switch tabs
    with col1:
        if st.button("Tableau de bord"):
            current_tab = "Summary"
            # switch_to_tab("Summary")
    with col2:
        if st.button("Détail produit"):
            current_tab = "Data"

    # Sidebar for selecting fields and applying filters
    st.sidebar.header("Select Fields and Apply Filters")
    numerical_fields = data.select_dtypes(include=['float64', 'int64']).columns
    categorical_fields = data.select_dtypes(include=['object']).columns

    all_fields = st.sidebar.multiselect("Champ à explorer", map_name.values(), key='col_cat_select')
    filter_values = {}
    for original_field in all_fields:
        field = list(map_name.keys())[list(map_name.values()).index(original_field)]
        if field in numerical_fields:
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
        else:
            filter_values[field] = st.sidebar.multiselect(f"Filter {field}", data[field].unique())

    selected_isin = st.sidebar.selectbox("Select ISIN", list(data.index))

    if st.sidebar.button("Ouvrir le détail"):
        new_tab(data, selected_isin)
    else:
        dashboard(data)



