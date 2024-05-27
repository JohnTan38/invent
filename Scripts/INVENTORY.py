import streamlit as st
import pandas as pd

def add_used_2(df):
    # Create a new column 'USED_2' initialized with zeros
    df['USED_2'] = 0

    # Iterate over each column
    for col in df.columns:
        # Check if the column header is a datetime
        if pd.to_datetime(col, errors='coerce') is not pd.NaT:
            # Count the occurrences of '2' in the column and add to 'USED_2'
            df['USED_2'] += df[col].apply(lambda x: str(x).count('2'))
            df['USED'] = df['USED_2'] * 2
            df['BAL'] = df['INITIAL QTY'] - df['USED']
            df['COST'] = df['UNIT $']* df['USED']
            df['STATUS'] = df['BAL'].apply(lambda x: 'REORDER' if x < 5 else 'HEALTHY')

    return df

dataUpload = st.file_uploader("Upload your xlsx file", type="xlsx")
if dataUpload is None:
        st.text("Please upload a file")
elif dataUpload is not None:
        data = pd.read_excel(dataUpload, skiprows=[0], engine='openpyxl')
        data = data.dropna(axis=1, how='all')
        data_new = add_used_2(data)
        if st.button('Lets get started'):
        #dataUpload = st.file_uploader("Upload your xlsx file", type="xlsx")
    
    

        #data = pd.read_excel(dataUpload, skiprows=[0], engine='openpyxl')
        #data = data.dropna(axis=1, how='all')
        #data_new = add_used_2(data)
            st.dataframe(data_new)

#data_new = add_used_2(data)