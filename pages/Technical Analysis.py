
import talib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
import time
from talib import MA_Type
from talib import abstract
from pages.lib import PatternRecognition
from pages.lib import DataFetch
st.set_page_config(
    page_title = '技術分析',
    page_icon = '📈',
    initial_sidebar_state = 'expanded',
)



period = 7
stock_id = '0050'
PR = pd.DataFrame(dtype=int)
PR_property = pd.DataFrame(index=['info','EN_name','CN_name'])
df = pd.DataFrame()
PR_name = pd.DataFrame(columns = ['names','w_names'])

selected=''
def tab_display():
    row4.write('報錯不要理他，重新搜尋即可')
    #重疊指標
    overlap, momentum, volume, volatility, statistics = row4.tabs(['重疊指標','動量指標','價量指標','波動性指標','統計分析'])
    ov = pd.DataFrame(columns=['CN','EN','Info'])
    ov.CN = ['布林通道','雙移動平均線 DEMA','指數平均線 EMA','希爾伯特瞬時變換 HT','考夫曼自適應 KAMA', '移動平均線 MA','簡單移動平均 SMA','加權移動平均 WMA']
    ov.EN = ['BBANDS','DEMA','EMA','HT_TRENDLINE','KAMA','MA','SMA','WMA']
    ov.Info = ['展現股票的波動範圍及未來走勢','利用長短線關係確認趨勢與時機','對收盤價算術平均，適合判斷價格未來走勢','對收盤價算術平均，適合判斷價格未來走勢','趨勢明顯看短線（靈敏）、橫盤整理看長線（雜訊少）','幾個週期內收盤價的算術平均','幾個週期內收盤價的算術平均','加權平均']
    ov_dict = dict(zip(ov.CN,ov.EN))
    with overlap:
        sel_over = st.form(key='sel_over',border=False)
        sel_over.dataframe(ov.values, use_container_width=True, hide_index=True)
        sel_over.selectbox(key='selection_ov', label='請選擇要查看的重疊指標', placeholder='下拉選擇', options=ov.CN)
        col1, col2 = sel_over.columns(2)
        col1.form_submit_button(label='確認', on_click=draw_ov, args=(ov,ov_dict))
        col2.number_input('請輸入週期（天）',min_value=5,value=5, key='period_ov')
    #動量指標
    mom = pd.DataFrame(columns=['CN','EN','Info'])
    mom.CN = ['平均趨向指數 ADX','ADX趨向指數 ADXR','順勢指標 CCI','動向指標 DMI', '平滑移動平均線 MACD','資金流量指標 MFI','相對強弱指數 RSI','隨機指標 K/D','威廉指標 W%R']
    mom.EN = ['ADX','ADXR','CCI','DX','MACD','MFI','RSI','STOCH','WILLR']
    mom.Info = ['判斷盤整、震盪和單邊趨勢','用來判斷ADX的趨勢','判斷股價是否超出常態分布','分析多空平衡點變化，以分析股價趨勢','分析長短線關係以判斷趨勢','反映市場流動趨勢','統計收盤價的漲數和跌數以判斷市場走勢','利用快線K與慢線D的關係來判斷市場趨勢','用以判斷市場是否超買或超賣']
    mom_dict = dict(zip(mom.CN,mom.EN))
    with momentum:
        sel_mom = st.form(key='sel_mom',border=False)
        sel_mom.dataframe(mom.values, use_container_width=True, hide_index=True)
        sel_mom.selectbox(key='selection_mom', label='請選擇要查看的動量指標', placeholder='下拉選擇', options=mom.CN)
        col1, col2, col3 = sel_mom.columns(3)
        col1.number_input('請輸入短週期（天）',min_value=5,value=9, key='fast_period_mom')
        col2.number_input('請輸入正常週期（天）',min_value=5,value=14, key='period_mom')
        col3.number_input('請輸入長週期（天）',min_value=5,value=26, key='slow_period_mom')
        sel_mom.form_submit_button(label='確認', on_click=draw_mom, args=(mom,mom_dict))
    #成交量指標
    vol = pd.DataFrame(columns=['CN','EN','Info'])
    vol.CN = ['量價指標 AD','能量潮指標 OBV']
    vol.EN = ['AD','OBV']
    vol.Info = ['利用當日搜盤價估算成交流量，用於估計一段時間內證券的累積資金量','統計成交量變動趨勢以推測股價趨勢']
    vol_dict = dict(zip(vol.CN,vol.EN))
    with volume:
        sel_vol = st.form(key='sel_vol',border=False)
        sel_vol.dataframe(vol.values, use_container_width=True, hide_index=True)
        sel_vol.selectbox(key='selection_vol', label='請選擇要查看的價量指標', placeholder='下拉選擇', options=vol.CN)
        sel_vol.form_submit_button(label='確認', on_click=draw_vol, args=(vol,vol_dict))
    #波動性指標
    vola = pd.DataFrame(columns=['CN','EN','Info'])
    vola.CN = ['真實波動幅度均值 ATR','歸一化 NATR']
    vola.EN = ['ATR','NATR']
    vola.Info = ['將昨日收盤價加入波動幅度計算的平均幅度','將ATR歸一化']
    vola_dict = dict(zip(vola.CN,vola.EN))
    with volatility:
        sel_vola = st.form(key='sel_vola',border=False)
        sel_vola.dataframe(vola.values, use_container_width=True, hide_index=True)
        sel_vola.selectbox(key='selection_vola', label='請選擇要查看的波動性指標', placeholder='下拉選擇', options=vola.CN)
        col1, col2 = sel_vola.columns(2)
        col2.number_input('請輸入週期（天）',min_value=5,value=14, key='period_vola')
        col1.form_submit_button(label='確認', on_click=draw_vola, args=(vola,vola_dict))
    #統計
    with statistics:
        stat = st.form(key='stat',border=True)
        stat.markdown('繪製 $Beta$ 及數值股票預測圖形')
        col1, col2 = stat.columns(2)
        col2.number_input('請輸入週期（天）',min_value=5,value=14, key='period_stat')
        col1.form_submit_button(label='確認', on_click=draw_stat)

def draw_ov(ov,ov_dict):
    global df
    st.session_state.selection_ov = st.session_state.selection_ov
    selected = st.session_state.selection_ov
    period = st.session_state.period_ov
    
    if ov_dict[selected] in ['DEMA', 'EMA', 'KAMA', 'MA', 'SMA', 'WMA']:
        df[f'{ov_dict[selected]}{period}'] = eval(f'abstract.{ov_dict[selected]}(df,period)')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.ds, y=df[f'{ov_dict[selected]}{period}'], name= f'{selected}{period}'))
        fig.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'))
        fig.update_layout(height=800, width=1200, title_text= f'{selected}{period}指標')
        row3.plotly_chart(fig)
    elif ov_dict[selected] == 'BBANDS':
        upper, middle, lower = talib.BBANDS(df.close,period,matype=MA_Type.T3)
        fig_BB = go.Figure()
        fig_BB.add_trace(go.Scatter(x=df.ds, y=upper, name='上', marker_color='red'))
        fig_BB.add_trace(go.Scatter(x=df.ds, y=middle, name='中', marker_color='blue'))
        fig_BB.add_trace(go.Scatter(x=df.ds, y=lower, name='下', marker_color='green'))
        fig_BB.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'))
        row3.plotly_chart(fig_BB)
    elif ov_dict[selected] == 'HT_TRENDLINE':
        HT = talib.HT_TRENDLINE(df.close)
        fig_HT = go.Figure()
        fig_HT.add_trace(go.Scatter(x=df.ds, y=HT, name='希爾伯特瞬時變換', marker_color='purple'))
        fig_HT.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'))
        row3.plotly_chart(fig_HT)
    index = list(ov_dict.keys()).index(selected)
    row3.write(selected + '：' + ov.Info[index])
    tab_display()
    

def draw_mom(mom,mom_dict):
    global df
    selected = st.session_state.selection_mom
    period = st.session_state.period_mom
    fast_period = st.session_state.fast_period_mom
    slow_period = st.session_state.slow_period_mom
    
    if mom_dict[selected] in ['ADX', 'ADXR', 'CCI', 'DX', 'MFI', 'RSI','WILLR']:
        df[f'{mom_dict[selected]}{period}'] = eval(f'abstract.{mom_dict[selected]}(df,period)')
        fig = make_subplots(rows=2, cols=1, shared_xaxes = True, vertical_spacing=0.02)
        fig.add_trace(go.Scatter(x=df.ds, y=df[f'{mom_dict[selected]}{period}'], name= f'{selected}{period}'),row=2,col=1)
        fig.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'),row=1,col=1)
        fig.update_layout(height=800, width=1200, title_text= f'{selected}{period}指標')
        row3.plotly_chart(fig)
    elif mom_dict[selected] == 'MACD':
        macd, macd_signal, macd_hist = talib.MACD(df.close, period, slow_period, fast_period)
        fig_MACD = make_subplots(rows=2, cols=1, shared_xaxes = True, vertical_spacing=0.02)
        fig_MACD.add_trace(go.Scatter(x=df.ds, y=macd, name='MACD', marker_color='brown'),row=2,col=1)
        fig_MACD.add_trace(go.Scatter(x=df.ds, y=macd_signal, name='MACD信號', marker_color='orange'),row=2,col=1)
        fig_MACD.add_trace(go.Scatter(x=df.ds, y=macd_hist, name='MACD歷史', marker_color='purple'),row=2,col=1)
        fig_MACD.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'),row=1,col=1)
        fig_MACD.update_layout(height=800, width=1200, title_text=f"MACD指標")
        row3.plotly_chart(fig_MACD)
    elif mom_dict[selected] == 'STOCH':
        slowk, slowd = talib.STOCH(df.high, df.low, df.close)
        fig_KD = make_subplots(rows=2, cols=1, shared_xaxes = True, vertical_spacing=0.02)
        fig_KD.add_trace(go.Scatter(x=df.ds, y=slowk, name='K', marker_color='blue'),row=2,col=1)
        fig_KD.add_trace(go.Scatter(x=df.ds, y=slowd, name='D', marker_color='orange'),row=2,col=1)
        fig_KD.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'),row=1,col=1)
        fig_KD.update_layout(height=800, width=1200, title_text=f"K/D指標")
        row3.plotly_chart(fig_KD)
    index = list(mom_dict.keys()).index(selected)
    row3.write(selected + '：' + mom.Info[index])
    tab_display()
    

def draw_vol(vol,vol_dict):
    global df
    
    selected = st.session_state.selection_vol
    df[f'{vol_dict[selected]}'] = eval(f'abstract.{vol_dict[selected]}(df)')
    fig = make_subplots(rows=2, cols=1, shared_xaxes = True, vertical_spacing=0.02)
    fig.add_trace(go.Scatter(x=df.ds, y=df[f'{vol_dict[selected]}'], name= f'{selected}'),row=2,col=1)
    fig.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'),row=1,col=1)
    fig.update_layout(height=800, width=1200, title_text= selected)
    row3.plotly_chart(fig)
    index = list(vol_dict.keys()).index(selected)
    row3.write(selected + '：' + vol.Info[index])
    tab_display()
    

def draw_vola(vola,vola_dict):
    global df
    
    selected = st.session_state.selection_vola
    period = st.session_state.period_vola
    df[f'{vola_dict[selected]}'] = eval(f'abstract.{vola_dict[selected]}(df,period)')
    fig = make_subplots(rows=2, cols=1, shared_xaxes = True, vertical_spacing=0.02)
    fig.add_trace(go.Scatter(x=df.ds, y=df[f'{vola_dict[selected]}'], name= f'{selected}'),row=2,col=1)
    fig.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'),row=1,col=1)
    fig.update_layout(height=800, width=1200, title_text= selected)
    row3.plotly_chart(fig)
    index = list(vola_dict.keys()).index(selected)
    row3.write(selected + '：' + vola.Info[index])
    tab_display()

def draw_stat():
    
    period = st.session_state.period_stat
    TSF = abstract.TSF(df,period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.ds, y=TSF, name= '預測股價', marker_color='red'))
    fig.add_trace(go.Scatter(x=df.ds, y=df.close, name='原始股價', marker_color='black'))
    fig.update_layout(height=800, width=1200, title_text= '基於數值模型預測的股價')
    row3.plotly_chart(fig)
    row3.write('---')
    beta = abstract.BETA(df,period)
    fig2 = make_subplots(rows=2, cols=1, shared_xaxes = True, vertical_spacing=0.02)
    fig2.add_trace(go.Scatter(x=df.ds, y=beta, name= f'{selected}'),row=2,col=1)
    fig2.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'),row=1,col=1)
    fig2.update_layout(height=800, width=1200, title_text= '各時間點的Beta值')
    row3.plotly_chart(fig2)
    row3.write('用來衡量股價相對於業績評價基準的波動性，beta>1 波動性較高')
    tab_display()


def On_Click():
    global start_date, end_date, stock_id, period, df, selected
    start_date = st.session_state.startdate
    end_date = st.session_state.enddate
    stock_id = st.session_state.stock
    with statusholder:
        with st.spinner(text='下載資料中...'):
            time.sleep(1)
            df = DataFetch.FetchPrice(stock_id,start_date,end_date)
            PatternRecognition.pattern_recognition(df,PR,PR_property,PR_name)
        statusholder.success('下載完成 ✅')
    fig = go.Figure(
        data=[go.Candlestick(x=df.ds, open=df.open, high=df.high, low=df.low, close=df.close)]
    )
    with row2:
        fig.update_layout(title= f'{stock_id} K線圖')
        st.plotly_chart(fig,x_label='日期',y_label='收盤價')
    tab_display()


headerholder = st.sidebar.container()

with st.sidebar:
    headerholder.header('技術分析')
    headerholder.info('蒐集了很多常用指標')
    statusholder = st.sidebar.empty()
    Get_Info = st.form(key='Get_Info', border = True, enter_to_submit=False, clear_on_submit=False)
    Get_Info.date_input(key = 'startdate',label='請選擇起始日期',value='2019-12-31')
    Get_Info.date_input(key='enddate',label='請選擇結束日期')
    Get_Info.text_input(key='stock',label='請輸入股票代號')
    Get_Info.form_submit_button(label='Search',icon=':material/search:', on_click = On_Click)

row1 = st.container(border=False)
row2 = st.container(border=True)
row3 = st.container(border=True)
row4 = st.container(border=True)

row1.header('Technical Analysis 技術分析 📈')
row1.write('---')
row1.markdown('##### 👈 輸入日期、股票代號查看常用技術分析指標')

    