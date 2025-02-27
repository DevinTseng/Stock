import streamlit as st


st.set_page_config(
    page_title = '首頁',
    page_icon = ':material/home:',
    initial_sidebar_state= 'expanded',
)

row1 = st.empty()
row2 = st.container()
row3 = st.container()
row4 = st.container()
row5 = st.container()
row2.write('---')
with st.sidebar:
    st.header('歡迎回家 🏠')
    st.success('來看看關於這個網站的介紹吧～')
    st.page_link(page='https://github.com/DevinTseng/Stock.git', label='**項目倉庫：Github**' , icon='🐈‍⬛', use_container_width = True)
row1.header('Stock Analysis 股票分析 📈')

row2.markdown('#### 功能直達')
col1, col2 = row2.columns(2)
row2.write('')
col1.page_link(page='pages/Bear Bull.py',label='**買賣指標 BearBull**',icon = '📍')
col1.page_link(page='pages/Stock Search.py',label='**價格搜股 Search by Price**',icon = '📍')
col1.page_link(page='pages/Technical Analysis.py',label='**技術分析 Search by Price**',icon = '📍')
col2.page_link(page='https://github.com/DevinTseng/Stock/tree/BearBull?tab=readme-ov-file#項目背景', label='**Story Behind 開發背景**' , icon='📖')
col2.page_link(page='https://github.com/DevinTseng/Stock/tree/BearBull?tab=readme-ov-file#未來願景', label='**Future Vision 未來展望**' , icon='🔭')
col2.page_link(page='https://github.com/DevinTseng/Stock/tree/BearBull?tab=readme-ov-file#開發思路', label='**BearBull 指標開發思路**' , icon='📒')
row2.write('---') 

row3.markdown('#### About 關於此網站')
row3.markdown('''
              這個網站是我個人的一個小小實驗項目，最早只有價格搜股功能。隨著我漸漸接觸一些技術分析的知識，同時基於神經網絡、機器學習的時序預測模型也愈發成熟，我便想能否結合兩者作股票分析。
              
              最初的想法很簡單暴力，那就是直接拿 Facebook 的 Prophet 模型預測股價，經過幾次迭代雖然已能達成不錯的估計效果，但該模型變化趨勢仍會落後股價一些，且還有相當誤差，故還談不上預測。
              
              
              雖然用模型預測股價這方面還沒達成理想效果，但在摸索訓練模型時，我學習到用Optuna框架找模型參數的方法。基於這樣的功能，我設計了一個買賣指標 \'BearBull Index\'，他能反映在一個特定時間點買入或賣出一支股票在未來一定週期的獲利能力，簡而言之他能告訴你在某一天某支股票應該買多少或賣多少。詳細的思路可以在 **這裡** 看到。除了買賣分析，我也集成了一些常用指標在 **Technical Analysis** 分頁，歡迎使用。''')
row3.markdown('''
           ```
           📌 使用過程如果彈出錯誤，這一般是因為操作太快，等一下再試一次就好

           📌 因為這個網站是部署在第三方平台上的，所以有時候載入較慢，請耐心等待

           📌 投資理財有賺有賠使用前請勿過度依賴計算結果
              ```''')
            
row3.write('---')

row4.markdown('#### Future Viosion 未來展望')
row4.markdown('''
                1. 繼續透過 NeuralProphet 訓練模型預測股價，預計加入一些提前變量如：美股波動一起訓練。
              2. 完善技術分析部分線圖繪製，開發自定義線圖合一顯示功能。
              3. BearBull 權值參數搜索加速。
              4. 加入型態分析（其實現在已經有了，只是在背景計算沒顯示出來）
              5. 修復頁面跳轉bug （這是streamlit框架的限制，有待他們解決）
              6. 結合大語言模型分析新聞語義，給出基本面及消息面評價指標
              ''')
            
row4.write('---')

row5.markdown('#### Story Behind 項目背景')
row5.markdown('''
              There has been a troublesome problem for my mom in stock investments.
              
               When watching the stock analysis live stream, the analysist usually hide the name along with the code of the stock, this posed a tough problem to my mom to find the specified stock, leading me to develop the **Search by Price** function, which gives you the TW stock code according to the given high, low, and open price.
              
              Recently, an article of using Goolgle\'s neural model to predict time siries came to my news feed, illuminating me to predict stock price by AI models. 
              
              To start up, I tried the Facebook-related Prophet model, then the Statforecast, NeuralProphet subsequently. Unforetunately, these models all return the results with predicted price laying back slightly to the real price.
               Though I still can\'t get the precisely predicted prices at present stage, but the price trends indicated is quite valuable for reference.
              
              During the process of training models, I came to know Optunas, a tool for deciding hyper-parameters automatically. This gave me the inspiration of a new mean for fabricating an investment indicator.
               With the power of Optuna, I composed an index called \'BearBull\', which simply reflects how uch you\'ll earn on a specific date in a given period of time. The larger the value, the more you\'ll earn.''')

             

