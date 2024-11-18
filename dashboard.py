import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

st.title("My Dashboard")
st.sidebar.header("Settings")
st.header("Data Overview")

# File uploader to upload CSV
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"], key="file_uploader_1")

if uploaded_file:
    # Load the uploaded CSV into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # Column selection
    option = st.sidebar.selectbox("Choose a Column", df.columns)
    st.write(f"You selected: {option}")

    # Filter numerical columns using a slider
    if option in df.select_dtypes(include=[np.number]).columns:
        min_value, max_value = int(df[option].min()), int(df[option].max())
        selected_range = st.slider(
            "Select Range", min_value=min_value, max_value=max_value, value=(min_value, max_value)
        )
        df = df[(df[option] >= selected_range[0]) & (df[option] <= selected_range[1])]

    # Display statistics for the selected column
    st.write("Statistics for the selected column:")
    st.write(df[option].describe())

    # Visualization
    chart_type = st.radio("Select Chart Type", ['Bar Chart', 'Pie Chart', 'Histogram'])

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

    # Search functionality
    search_term = st.text_input("Search for a value in the selected column")
    if search_term:
        filtered_df = df[df[option].astype(str).str.contains(search_term, case=False, na=False)]
        st.write(filtered_df)

    # Download filtered data
    st.download_button(
        label="Download filtered data",
        data=df.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )

    # Email Customization
    st.header("Email Customization")
    prompt_template = st.text_area(
        "Enter your email template with placeholders (e.g., 'Hi {Name}, welcome to {Location}!')"
    )

    if prompt_template and st.button("Generate Emails"):
        emails = []
        for _, row in df.iterrows():
            payload = {"prompt": prompt_template, "row": row.to_dict()}
            response = requests.post("http://127.0.0.1:5000/generate-email", json=payload)
            if response.status_code == 200:
                emails.append(response.json()["email"])
            else:
                st.error(f"Failed to generate email for {row['Email']}")

        if emails:
            df["Generated Email"] = emails
            st.write("Generated Emails:")
            st.write(df[["Email", "Generated Email"]])

    # Email Sending
    st.header("Email Sending")
    if st.button("Send Emails"):
        if "Generated Email" in df.columns:
            for _, row in df.iterrows():
                payload = {
                    "recipient": row["Email"],
                    "subject": "Your Custom Subject",
                    "body": row["Generated Email"]
                }
                response = requests.post("http://127.0.0.1:5000/send-email", json=payload)
                if response.status_code == 200:
                    st.success(f"Email sent to {row['Email']}")
                else:
                    st.error(f"Failed to send email to {row['Email']}")
        else:
            st.error("No 'Generated Email' column found. Generate emails first.")

else:
    st.write("Please upload a CSV file to get started.")

# Custom CSS for styling
st.markdown("""
    <style>
        .reportview-container .main .block-container {
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Info message for the sidebar
st.sidebar.info("Upload a CSV file to start analysis and email generation.")
