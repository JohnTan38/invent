import streamlit as st
import pandas as pd

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

title_main('INVENTORY')

dataUpload = st.file_uploader("Upload your xlsx file", type="xlsx")
if dataUpload is None:
        st.text("Please upload a file")
elif dataUpload is not None:
        data = pd.read_excel(dataUpload, skiprows=[0], engine='openpyxl')
        data = data.dropna(axis=1, how='all')
        data_new = add_used_2(data)
        if st.button('Lets get started'):
                
            st.dataframe(data_new)
            success_df('Data generated successfully!')
