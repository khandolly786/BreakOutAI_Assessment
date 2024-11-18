import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("My Dashboard")
st.sidebar.header("Settings")
st.header("Data Overview")

# File uploader to upload CSV
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"], key="file_uploader_1")

# If file is uploaded, process it
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # Column selection after file upload
    option = st.sidebar.selectbox("Choose a Column", df.columns)
    st.write("You selected:", option)

    # Example: Slider for filtering numerical columns
    if option in df.select_dtypes(include=[np.number]).columns:
        min_value, max_value = int(df[option].min()), int(df[option].max())
        selected_range = st.slider(
            "Select Range", min_value=min_value, max_value=max_value, value=(min_value, max_value)
        )
        df = df[(df[option] >= selected_range[0]) & (df[option] <= selected_range[1])]

    # Displaying Statistics for the selected column
    st.write("Statistics for the selected column:")
    st.write(df[option].describe())

    # Choose chart type for visualization
    chart_type = st.radio("Select Chart Type", ['Bar Chart', 'Pie Chart', 'Histogram'])

    # Generate the appropriate chart
    if chart_type == 'Bar Chart':
        fig, ax = plt.subplots()
        df[option].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)
    elif chart_type == 'Pie Chart':
        fig, ax = plt.subplots()
        df[option].value_counts().plot(kind="pie", ax=ax, autopct='%1.1f%%')
        st.pyplot(fig)
    elif chart_type == 'Histogram':
        fig, ax = plt.subplots()
        df[option].plot(kind='hist', ax=ax, bins=30)
        st.pyplot(fig)

    # Search functionality for column values
    search_term = st.text_input("Search for a value in the selected column")
    if search_term:
        filtered_df = df[df[option].astype(str).str.contains(search_term, case=False, na=False)]
        st.write(filtered_df)

    # Button to download filtered data as CSV
    st.download_button(
        label="Download filtered data",
        data=df.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:
    st.write("Please upload a CSV file to get started.")

# Custom CSS to style the page
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Info message
st.sidebar.info("Upload a CSV file to get started with the analysis.")
