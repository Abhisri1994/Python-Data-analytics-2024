# streamlit run dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# global variables
years = list (map(str, range(1998, 2014)))

@st.cache_data
def load_data():
        df = pd.read_excel("Canada.xlsx", sheet_name=1, skiprows=20, skipfooter=2)
        cols_to_rename ={
        'OdName': 'Country',
        'AreaName': 'Continent',
        'RegName': 'Region',
        'DevName': 'Status',
        }
        df = df.rename(columns=cols_to_rename)
        cols_to_drop = ['AREA', 'REG', 'DEV', 'Type', 'Coverage']
        df = df.drop(columns=cols_to_drop)
        df = df.set_index('Country')
        df.columns = [str(name).lower() for name in df.columns.tolist()]
        df['total'] = df[years].sum(axis=1)
        df
        return df

# configure the layout.
st.set_page_config(
    layout="wide",
    page_title="immigration Data Analysis",
    page_icon="📊",
)

#loading the data
with st.spinner("loading Data..."):
    df = load_data()
    st.sidebar.success("data loaded successfully! ")

# creating the ui interface
c1, c2,c3 = st.columns(2)
c1.title("iimigration Data Analysis")
c2.header("Summary of data")
total_rows = df.shape[0]
total_cols = df.shape[1]
total_immig = df.total.sum()
max_immig = df.total.max()
max_immig_country = df.total.idxmax()
c2.metric("Total Countries", total_rows)
c2.metric("Total Years", len(years))
c2.metric("Total immigration",f'{total_immig/1000000: .2f}M')
c2.metric("Maxmium immigration",f'{max_immig/1000000: .2f}M',
          f"{max_immig_country}")
c3.header("Top Countries") # type: ignore
top_10 = df.head(10)['total']
c3.dataframe(top_10,use_container_width=True)
fig2=px.bar(top_10,x=top_10.index,y='total')
c3.plotly_chart(fig,use_container_width=True)

# Country wise visualtion
countries= df.index.to_list()
country=c1.selectbox("Select a country", countries)
immig=df.loc[country, years]
fig=px.area(immig,x=immig.index,y= immig.values,title="immigration trend")

c1.plotly_chart(fig,use_container_width=True)
fig2=px.histogram(immig, x=immig.values,nbins=)
           



