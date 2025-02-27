import requests
from io import StringIO
import pandas as pd
import numpy as np
import json
import streamlit as st

st.set_page_config(
    page_title='價搜台股',
    initial_sidebar_state='expanded',
    page_icon='🔍')
headerholder = st.sidebar.container()

High=Low=Open=0.0
left_column, right_column=st.columns(2)


@st.cache_data
def getTpex(TpexURL):
    r = requests.get(TpexURL)
    return r
def SearchTpex(TpexURL):#上櫃搜索
    r = getTpex(TpexURL)
    df0 = pd.json_normalize(json.loads(r.text),record_path=['aaData'])
    df0=df0[[0,1,4,5,6,2]]
    df0.columns=['代號','名稱','開盤','最高','最低','收盤']
    df0 = df0[df0['開盤']==Open]
    df0.set_index(['名稱'],inplace=True)
    df0.index.name='證券名稱'
    df1 = df0
    df1['代號'] = 'https://tw.stock.yahoo.com/quote/'+ df0['代號'] +'.TWO/technical-analysis'

    if len(df1)==0:
        st.text('【上櫃】')
        statusholder.error('查無此股票')
    elif len(df1)==1:
        statusholder.success('找到一支上櫃股票 ✅')
        st.text('【上櫃】')
        st.dataframe(df1,column_config={'代號':st.column_config.LinkColumn(help='跳轉至Yahoo股市頁面',disabled=True,display_text='https://tw\.stock\.yahoo\.com/quote/(.*?)\.TWO/technical-analysis')}, use_container_width=True)
    else:
        statusholder.success('找到多支上櫃股票 ✅')
        st.text('【上櫃】')
        df1=df1[np.logical_or(df1['最高']==High, df1['最低']==Low)]
        st.dataframe(df1,column_config={'代號':st.column_config.LinkColumn(help='跳轉至Yahoo股市頁面',disabled=True,display_text='https://tw\.stock\.yahoo\.com/quote/(.*?)\.TWO/technical-analysis')},use_container_width=True)
        
@st.cache_data
def postStock(URL):
    r = requests.post(URL)
    return r
def Search(URL):#上市搜索
    with statusholder:
        with st.spinner('正在搜索上市股票 🔍'):
            r = postStock(URL)
    name_attribute = ['證券代號','證券名稱','開盤價','最高價','最低價','收盤價']
    df0 = pd.read_csv(StringIO(r.text.replace("=", "")), 
                header=["證券代號" in l for l in r.text.split("\n")].index(True)-1,usecols=name_attribute)#將證券代號第一次出現那行作爲標頭
    df0.columns=['代號','證券名稱','開盤','最高','最低','收盤']
    df0.set_index(['證券名稱'],inplace=True)
    df0 = df0[df0['開盤']==Open]
    df1 = df0
    df1['代號'] = 'https://tw.stock.yahoo.com/quote/'+ df0['代號'] +'.TW/technical-analysis'

    if len(df1)==1:
        statusholder.success('找到一支上市股票 ✅')
        st.text('【上市】')
        st.dataframe(df1,column_config={'代號':st.column_config.LinkColumn(help='跳轉至Yahoo股市頁面',disabled=True,display_text='https://tw\.stock\.yahoo\.com/quote/(.*?)\.TW/technical-analysis')},use_container_width=True)
    elif len(df1)==0:
        st.text('【上市】')
        statusholder.error('查無此股票')
    else:
        df1=df1[np.logical_or(df1['最高']==High, df1['最低']==Low)]
        st.text('【上市】')
        st.dataframe(df1,column_config={'代號':st.column_config.LinkColumn(help='跳轉至Yahoo股市頁面',disabled=True,display_text='https://tw\.stock\.yahoo\.com/quote/(.*?)\.TW/technical-analysis')},use_container_width=True)
        statusholder.success('找到多支上市股票 ✅')
    with statusholder:
        with st.spinner('正在搜索上櫃股票 🔍'):
            SearchTpex(TpexURL)
with st.sidebar:
    headerholder.header('價格搜股')
    headerholder.info('股市分析老師不跟你說股票代號？來這搜！')
    statusholder = st.empty()
    Input_Info = st.form(key='Input_Info',border=True, enter_to_submit=False, clear_on_submit=False)
    high = Input_Info.number_input('請輸入最高價',min_value=0.0,value=None)
    low = Input_Info.number_input('請輸入最低價',min_value=0.0,value=None)
    open = Input_Info.number_input('請輸入開盤價',min_value=0.0,value=None)
    date = Input_Info.date_input('請選擇查詢日期')
    datestr = date.strftime('%Y%m%d')
    TpexURL='https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d='+str(int(datestr[0:4])-1911)+'/'+datestr[4:6]+'/'+datestr[6:8]
    URL='https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL'
    Search_Button = Input_Info.form_submit_button(label='Search',icon=':material/search:')

if Search_Button:
        if high is not None: 
            High=f'{high:.2f}' 
        else: 
            High=0
        if low is not None: 
            Low=f'{low:.2f}' 
        else: 
            Low=0
        if open is not None:
            Open=f'{open:.2f}'
        else:
            Open=0
        Search(URL)

row1 = st.empty()
row2 = st.empty()
row3 = st.empty()
row4 = st.empty()

row1.header('Search by Price 價搜台股 🔍')
row1.write('---')
row1.markdown('''
              
              ##### 👈 輸入最高、最低、開盤價搜台股代號
              :red-background[當日價格可能因為尚未發布資料而搜不到股票]''')