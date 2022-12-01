import streamlit as st
import pandas as pd
#import sqlite3
import pdfplumber
#import camelot


st.config.fastReruns=True
st.set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style,unsafe_allow_html=True)

set={
    "vertical_strategy": "text", 
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],
    "explicit_horizontal_lines": [],
    "snap_tolerance": 3,
    "snap_x_tolerance": 3,
    "snap_y_tolerance": 3,
    "join_tolerance": 3,
    "join_x_tolerance": 3,
    "join_y_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 2,
    "keep_blank_chars": False,
    "text_tolerance": 1,
    "text_x_tolerance": 1,
    "text_y_tolerance": 3,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": 3,
    "intersection_y_tolerance": 3,
}

d=pdfplumber.open("380077Thu12202217201122137057952896.pdf", password = "H@thoda19")
#d= camelot.read_pdf("380077Thu12202217201122137057952896.pdf", password = "H@thoda19")
#st.write(d.pages[0].rects)
td=[]
for pp in range(len(d.pages)):
    #td=[]
    td.extend([x['text'] for x in d.pages[pp].extract_words(keep_blank_chars=True)])
    #dd.append(td)
df=pd.DataFrame(td)
df
di=df.loc[df[0].str.contains("\*\*\*")].index
dil=[]
for d in di:
    dil.extend([d-1,d])
df=df.loc[~df.index.isin(dil)].reset_index(drop=True)
ind=df.loc[df[0].str.contains("PAN : OK")].index
ine=df.loc[df[0].str.contains("NAV on")].index
ind
ine
df1=pd.DataFrame()
for ii in zip(ind,ine):
    df1=df1.append(df[ii[0]+1:ii[1]-1].reset_index(drop=True))
    df1=df1.append(["","",""])
ff,tt=pd.DataFrame(),pd.DataFrame()
for i in range(int(len(df1)/6)):
    df2=df1.iloc[i*6:6*i+6,:].reset_index(drop=True).T
    df3=df.iloc[i*6:6*i+6,:].reset_index(drop=True).T
    ff=pd.concat([ff,df2])
    tt=pd.concat([tt,df3])
ff
tt
#print(d.pages[0].extract_words())
#df=pd.read_json(dd)
#df=pd.DataFrame(d.pages[0].extract_tables(set))
df
