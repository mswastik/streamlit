import streamlit as st
import pandas as pd
#import sqlite3
from pathlib import Path
import altair as alt



st.config.fastReruns=True

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style,unsafe_allow_html=True)

@st.cache
def data():
    #con = sqlite3.connect("C:\\Users\\smishra14\\Downloads\\data\\consolidated\\data.db")
    p = Path(__file__)
    df=pd.read_excel(str(p.parent) +"/consolidated statement.xlsx" ,sheet_name="MF")
    df['Date']=pd.to_datetime(df['Date'])
    return df

df=data()

df1=df.groupby(['Name of the Fund']).agg({'Net Units':'sum','Current Nav':'mean','Invested':'sum','Withdrawal Amt.':'sum','Invested Amt.':'sum'})

df1['Gain']=df1['Withdrawal Amt.']-df1['Invested Amt.']

df1['Current Value']=df1['Net Units']*df1['Current Nav']

gg=df1[df1['Net Units']<.009]['Gain']
ii=df1[df1['Net Units']>.009]['Invested Amt.'].sum()
c1,c2,c3=st.columns(3)

#c1.subheader(f"Current Value") 
c1.metric(label="Current Value", value=format(df1['Current Value'].sum(),'.0f'),delta=format(((
df1['Current Value'].sum()-ii)/ii)*100,".1f")+"%")

c2.metric("Invested Value",format(ii,'.0f'))

c3.metric("Realised Gain", format(gg.sum(),'.0f'))
st._legacy_dataframe(df1[df1["Current Value"]>0][["Invested Amt.", "Current Value"]])

#dd

#dft=df.groupby('Date')['Cum Amt.'].sum().reset_index()

#dft['Date1']=pd.to_datetime(dft['Date'])+ pd.offsets.MonthEnd()

dft=df.copy()
dft['nu']=dft.groupby("Name of the Fund")['Net Units'].cumsum()
dft['Amt']=dft['nu']*dft['NAV']

#dft=dft.set_index('Date').resample('M').sum('Amt').reset_index()

dfg=dft.groupby("Date").sum(). reset_index() 
dfg["camt"]=dfg["Amt"].cumsum() 
dfg['Date']=pd.to_datetime(dfg['Date'])
st.altair_chart(alt.Chart(dfg).mark_line(point=alt.OverlayMarkDef(size=75,opacity=.5)).encode(y=alt.Y("sum(camt):Q"), x=alt.X("yearmonth(Date):T"),tooltip=['camt', 'Date']).interactive(),use_container_width=True)