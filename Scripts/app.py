import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime

st.set_page_config('Inventory', page_icon="🏛️", layout='wide')
def title(url):
     st.markdown(f'<p style="color:#2f0d86;font-size:22px;border-radius:2%;"><br><br><br>{url}</p>', unsafe_allow_html=True)
def title_main(url):
     st.markdown(f'<h1 style="color:#230c6e;font-size:42px;border-radius:2%;"><br>{url}</h1>', unsafe_allow_html=True)

def success_df(html_str):
    html_str = f"""
        <p style='background-color:#baffc9;
        color: #313131;
        font-size: 15px;
        border-radius:5px;
        padding-left: 12px;
        padding-top: 10px;
        padding-bottom: 12px;
        line-height: 18px;
        border-color: #03396c;
        text-align: left;'>
        {html_str}</style>
        <br></p>"""
    st.markdown(html_str, unsafe_allow_html=True)


def process_dataframe(df_data):
    # Function to extract number after last whitespace
    def extract_number(s):
        # Check if the input is string
        if isinstance(s, str):
            try:
                
                return np.float64(re.findall(r'\b\d+\b', s)[-1])
            except (IndexError, ValueError):
                return np.float64(0)
        else:
            return np.float64(0)

    df_data['USED'] = 0

    # Check each column
    for col in df_data.columns:
        try:
            # If the column header is a datetime
            datetime.strptime(str(col), '%Y-%m-%d %H:%M:%S')
            # Apply the function to each element in the column
            df_data['USED'] += df_data[col].apply(extract_number)
        except ValueError:
            continue
            
        df_data['BAL'] = df_data['INITIAL QTY'] - df_data['USED']
        df_data['COST'] = df_data['UNIT $']* df_data['USED']
        df_data['STATUS'] = df_data['BAL'].apply(lambda x: 'REORDER' if x < 5 else 'HEALTHY')

    return df_data

def select_reorder(df):
    return df[df['STATUS'] == 'REORDER']

title_main('INVENTORY')

dataUpload = st.file_uploader("Upload your xlsx file", type="xlsx")
if dataUpload is None:
        st.text("Please upload a file")
elif dataUpload is not None:
        data = pd.read_excel(dataUpload, skiprows=[0], engine='openpyxl')
        data = data.dropna(axis=1, how='all')
        data_new = process_dataframe(data).reset_index(drop=True)
        if st.button('Lets get started'):
                
            st.dataframe(data_new)
            st.divider()
            st.dataframe(select_reorder(data_new))
            reOrder = select_reorder(data_new)['ITEM DESCRIPTION DO'].tolist()
            html_str_order = f"""
                <p style='background-color:#F0FFFF;
                color: #483D8B;
                font-size: 18px;
                font: bold;
                border-radius:5px;
                padding-left: 12px;
                padding-top: 10px;
                padding-bottom: 12px;
                line-height: 18px;
                border-color: #03396c;
                text-align: left;'>
                {reOrder}</style>
                <br></p>"""
            st.markdown('''
                **REORDER** '''+html_str_order, unsafe_allow_html=True)

            success_df('Data generated successfully!')


st.markdown('''
            **REORDER** :orange[ITEM] :blue-background[blue highlight] :cherry_blossom:''')
