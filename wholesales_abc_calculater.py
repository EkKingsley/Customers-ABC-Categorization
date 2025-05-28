import pandas as pd
import streamlit as st


st.set_page_config(page_title="WHOLESALES ABC CALCULATOR",
                   layout="centered",
                   page_icon="📊")
with st.container(border=True):
    file = st.file_uploader("Upload File", type=["csv", "xlsx"])

if file is not None:
    # get name of file
    filename = file.name
    n = 3 # number of characters to extract from filename
    length = len(filename) # length of filename
    file_type = filename[length - n:] # get last 3 characters
    st.write(file_type)

    if file_type in ["csv", "txt"]:
        df = pd.read_csv(file)
        with st.container(border=True):
            st.subheader("INITIAL DATA")
            st.dataframe(df)
    elif file_type == "xlsx":
        df = pd.read_excel(file)
        with st.container(border=True):
            st.subheader("INITIAL DATA")
            st.dataframe(df)
    elif file_type == "xls":
        df = pd.read_excel(file)
        with st.container(border=True):
            st.subheader("INITIAL DATA")
            st.dataframe(df)
    else:
        with st.container(border=True):
            st.warning("Enter a specified file type")

    st.sidebar.subheader("Choose the appropriate Columns")
    branch = st.sidebar.selectbox("CHOOSE BRANCH", df.Branch.unique())

    with st.container(border=True):
        if branch is not None:
            filtered_df = df[df["Branch"] == branch]
            st.subheader("FILTERED DATA")
            st.dataframe(filtered_df)

    def classify(row):
        if row['Cumulative Percentage'] <= 80:
            return 'A'
        elif row['Cumulative Percentage'] <= 95:
            return 'B'
        else:
            return 'C'

    generate_abc = st.button("Generate ABC")

    with st.container(border=True):
        if generate_abc:
            # Sort by Value in descending order
            df = filtered_df.sort_values(by='TOTAL REVENUE', ascending=False).reset_index(drop=True).drop(columns='Branch',
                                                                                                  axis=1)

            # Calculate cumulative percentage
            df['Cumulative Value'] = df['TOTAL REVENUE'].cumsum()
            df['Cumulative Percentage'] = 100 * df['Cumulative Value'] / df['TOTAL REVENUE'].sum()

            # Classify items into A, B, C
            df['Category'] = df.apply(classify, axis=1)

            # Format cumulative percentage as a percentage with 4 decimal places
            df['Cumulative Percentage'] = df['Cumulative Percentage'].map(lambda x: f"{x:.4f}%")

            # Display the results
            st.subheader("ABC DATA")
            st.dataframe(df)

        with st.expander("Download Data"):
            export = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=export, file_name = f"{branch}_data.csv", mime='text/csv',
                           help='Click here to download the data as a CSV file')
else:
    st.info("Please upload a CSV file with customers and sales value to get started")