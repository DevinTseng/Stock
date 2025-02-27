

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
import time

from pages.lib import PatternRecognition
from pages.lib import DataFetch
import optuna
st.set_page_config(
    page_title = '買賣點分析',
    page_icon = '🦬',
    initial_sidebar_state = 'expanded',
)



n_trials = 10
period = 7
counts = 0
stock_id = '0050'
PR = pd.DataFrame(dtype=int)
PR_property = pd.DataFrame(index=['info','EN_name','CN_name'])
df = pd.DataFrame()
PR_name = pd.DataFrame(columns = ['names','w_names'])

#計算多日平均盈餘（作為評估賺錢能力的指標）
def AverageEarning(close, BB, period):
    #AverageEarningRate
    AER = pd.Series(index = close.index, dtype = float)
    for i,close_price in enumerate(close):
        sum = 0
        for y in range(1,period+1):
            sum += close[i+y] - close_price
            if((i+y+1) > (len(close)-1)):
               AER[i] = sum * BB[i]/y/close_price
               AER[[j for j in range(i+1,i+period+1)]] = 0
               return AER
        AER[i] = sum *BB [i] / period / close_price
    return AER

def CalculateBB(weights,PR):
    BB = pd.Series(index=PR.index, dtype=float)
    for i,date in enumerate(BB.index):
        sum=0
        for w_name in weights.keys():
            name = w_name.replace('w_','')
            sum += PR.loc[i,name] * weights[w_name]
        BB[i] = sum
    return BB

def objective(trial, period, df, PR, PR_name):
    #添加要試驗的權重變量
    weights = {}
    global counts
    n_trials = st.session_state.n_trials_trial
    statusholder.progress(counts/n_trials,f'需要一些時間，去喝杯茶吧 🍵  \n{counts}/{n_trials}')
    for w in PR_name.w_names:
        weights[w] = trial.suggest_float(w,0,1)

    #先以日期遍歷PR表，在每個日期中遍歷PR_name取得各變量名並計算sum(權重*值)，儲存於PB.BearBull中
    PR.BearBull = CalculateBB(weights,PR)
    #Normalize
    PR['BBSTD'] = (PR.BearBull / PR.BearBull.std())
    #Calculate Average Earning Rate for assigned period
    df[f'AER{period}'] = AverageEarning(df.close, PR.BearBull, period)
    counts+=1
    return df[f'AER{period}'].mean()

def find_weights():
    study = optuna.create_study(direction='maximize')
    global n_trials, period, df, PR, PR_name, PR_property, counts
    counts=0
    n_trials = st.session_state.n_trials_trial
    period = st.session_state.period_trial
    statusholder.progress(0,text='開始尋找權值，請耐心等待 ⌛️')
    with statusholder:
        with st.spinner(text='尋找最佳權值中 🔍'):
            study.optimize(lambda trial: objective(trial, period=period, df=df, PR=PR, PR_name=PR_name), n_trials = n_trials)
    statusholder.success('已找到最佳權值！')
    best_trial = study.best_trial
    for name in PR_name.names:
        PR_property.loc[f'weight{period}',name] = best_trial.params[f'w_{name}']
    BB = CalculateBB(best_trial.params,PR)
    df[f'BB{period}'] = BB.values / BB.std()
    df[f'AER{period}'] = AverageEarning(period=period,BB=df[f'BB{period}'],close=df.close)
    
    fig_AER = make_subplots(rows=2, cols=1, shared_xaxes = True, vertical_spacing=0.02)
    #x日平均盈餘
    fig_AER.add_trace(go.Scatter(x=df.ds, y=df[f'AER{period}'], name=f'{period}日平均盈餘率(AER{period})', marker_color=['purple' if val > 0 else 'blue' for val in df[f'AER{period}']]), row=2, col=1)
    fig_AER.add_trace(go.Bar(x=df.ds, y=df[f'BB{period}']*df.close.mean()/100, base=df.close, name=f'{period}日買賣指標 {period}BearBull', marker_color=['red' if val > 0 else 'green' for val in df[f'BB{period}']]), row=1, col=1)
    fig_AER.add_trace(go.Scatter(x=df.ds, y=df.close, name='股價', marker_color='black'), row=1, col=1)
    fig_AER.update_layout(height=800, width=1200, title_text=f"{period}日平均盈餘與購買指標")
    weights, figure = row3.tabs(['型態分析','購買指標'])
    #PR_property_display.sort_values(axis='index', ascending=False, by=f'weight{period}')
    with figure:
        st.write('綜合一堆型態指標加權計算出的購買指標，紅線越長越適合買；綠線越長越應該賣\n（可將圖表放大較易看到買賣指標）')
        st.plotly_chart(fig_AER)
    with weights:
        st.write('計算出的權值代表不同型態指標的重要程度，此權值根據能獲得最高 Average Earning Rate 求出\n(點擊info單元格查看線型說明)')
        st.write(PR_property)
    
    row3.write(f'本次試驗測試出最佳平均盈餘率AER{period}為：' + str(best_trial.value*100)+'%')
    trial_info()

def trial_info():
    Trial_Info = row4.form(key='Trial_Info', enter_to_submit=False, clear_on_submit=False, border=False)
    Trial_Info.text('通過試驗算法找出使盈餘率最大的型態權值')
    n_trials = Trial_Info.number_input(key='n_trials_trial',label='請輸入試驗次數',min_value=5,value=10,help='試驗次數越多，試出來的參數越準，但所需時間也越久',label_visibility='visible')
    period = Trial_Info.number_input(key='period_trial',label='請輸入檢視週期（天）',min_value=7,value=14)
    Trial_Info.form_submit_button('開始試驗',icon=':material/play_arrow:', on_click = find_weights)

def On_Click():
    global start_date, end_date, stock_id, n_trials, period, df
    start_date = st.session_state.startdate
    end_date = st.session_state.enddate
    stock_id = st.session_state.stock
    with st.sidebar:
        with st.spinner(text='下載資料中...'):
            time.sleep(1)
            df = DataFetch.FetchPrice(stock_id,start_date,end_date)
            PatternRecognition.pattern_recognition(df,PR,PR_property,PR_name)
        statusholder.success('下載完成 ✅')
    fig = go.Figure(
        data=[go.Candlestick(x=df.ds, open=df.open, high=df.high, low=df.low, close=df.close)]
    )
    row1.subheader('⬇️ ⬇️ ⬇️ ⬇️')
    with row2:
        
        fig.update_layout(title= f'{stock_id} K線圖')
        st.plotly_chart(fig,x_label='日期',y_label='收盤價')
    trial_info()
    
    

    
with st.sidebar:
    headerholder = st.container()
    statusholder = st.empty()
    Get_Info = st.form(key='Get_Info', border = True, enter_to_submit=False, clear_on_submit=False)
    Get_Info.date_input(key = 'startdate',label='請選擇起始日期',value='2019-12-31')
    Get_Info.date_input(key='enddate',label='請選擇結束日期')
    Get_Info.text_input(key='stock',label='請輸入股票代號')
    Get_Info.form_submit_button(label='Search',icon=':material/search:', on_click = On_Click)
headerholder.header('牛市熊市一測便知 🦬')
headerholder.info('Powered by 電腦煉丹術！')
row1 = st.container()
row2 = st.container(border=True)
row3 = st.container(border=True)
row4 = st.container(border=True)

row1.header('Bear Bull Index 買賣點分析 🏹')
row1.write('---')
row1.markdown('''
                此功能是用於評估某支股票在特定日期應該買或賣多少，當 Bear Bull 數值愈高且大於0，表示此時買股票更容易獲利；反之，若數值為負且愈小表示此時越應該出脫股票。
              
                計算方式簡單來說就是把眾多股票指標在某一日期的分析給出的結果作加權平均，得到BearBull值：

                :red[$BearBull = \sum{W_iX_i}$]，其中 W 與 X 分別為各個型態指標給出的多空分數及其對應的權重值，為了求得能使我們盈餘儘量大的最佳權值，於是我利用機器優化算法遍歷每個日期，最終求得一組當前最佳的權值。
              

              ''')
row1.write('---')
row1.write('詳細推導過程可以看這邊：')
row1.page_link(page='https://github.com/DevinTseng/Stock/blob/main/README.md#開發思路',label='**BearBull開發思路**',icon = '✏️')
row1.write('')
row1.markdown(''':red-background[⚠️ 注意：  所求出的權重組合僅代表在 $x$ 次試驗後機器找到的最優解，並不代表終極答案]''')



    