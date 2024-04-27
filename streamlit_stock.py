import requests
from io import StringIO
import pandas as pd
import numpy as np
import json
import time
import streamlit as st
from datetime import datetime

st.set_page_config(page_title='台灣股票搜索小工具',initial_sidebar_state='expanded',page_icon='🔍')
st.sidebar.title('股票搜尋小工具')
High = f'{st.sidebar.number_input('請輸入最高價'):.2f}'
Low = f'{st.sidebar.number_input('請輸入最低價'):.2f}'
Open = f'{st.sidebar.number_input('請輸入開盤價'):.2f}'
date=st.sidebar.date_input('請選擇查詢日期')
datestr=date.strftime('%Y%m%d')
left_column, right_column=st.columns(2)
TpexURL='https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d='+str(int(datestr[0:4])-1911)+'/'+datestr[4:6]+'/'+datestr[6:8]
URL='https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL'

@st.cache_data
def getTpex(TpexURL):
    r = requests.get(TpexURL)
    return r
def SearchTpex(TpexURL):#上櫃搜索
    r = getTpex(TpexURL)
    df0 = pd.json_normalize(json.loads(r.text),record_path=['aaData'])
    df0=df0[[0,1,4,5,6,2]]
    df0.columns=['代號','名稱','開盤','最高','最低','收盤']
    df0.set_index(['名稱'],inplace=True)
    df1 = df0[df0['開盤']==Open]
    df1.index.name=''
    
    if len(df1)==0:
        st.text('【上市】【上櫃】')
        st.write('查無此股票')
    elif len(df1)==1:
        st.text('【上櫃】')
        st.write(df1)
    else:
        st.text('【上櫃】')
        df1=df1[np.logical_or(df1['最高']==High, df1['最低']==Low)]
        st.write(df1)
    
@st.cache_data
def postStock(URL):
    r = requests.post(URL)
    return r
def Search(URL):#上市搜索
    r = postStock(URL)
    name_attribute = ['證券代號','證券名稱','開盤價','最高價','最低價','收盤價']
    df0 = pd.read_csv(StringIO(r.text.replace("=", "")), 
                header=["證券代號" in l for l in r.text.split("\n")].index(True)-1,usecols=name_attribute)#將證券代號第一次出現那行作爲標頭
    df0.columns=['代號','證券名稱','開盤','最高','最低','收盤']
    df0.set_index(['證券名稱'],inplace=True)
    df0.index.name=''
    df1 = df0[df0['開盤']==Open]
    
    if len(df1)==1:
        st.text('【上市】')
        st.write(df1)
    elif len(df1)==0:
        SearchTpex(TpexURL)
        return
    else:
        df1=df1[np.logical_or(df1['最高']==High, df1['最低']==Low)]
        st.text('【上市】')
        st.write(df1)
    SearchTpex(TpexURL)

if st.sidebar.button('搜尋'):
        Search(URL)
    


