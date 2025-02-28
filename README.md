
# Stock Analysis 股票分析
## Main Features 主要功能:
此項目部署於 Streamlit 平台，可直接至網址: <https://tw-stock-analysis.streamlit.app> 使用

This project is deployed on Streamlit, you can access it through the URL above.

1. Search by Price 價格搜股:
>通過比對輸入日期的最高價、最低價及開盤價，找出對應股票。
 **應用:** 分析師把股票代碼藏起來要你加入股友社才能看? 來這裡直接搜就好啦!
>
> Find the TW stock code by matching the high, low, and open price.
>
2. BearBull Index 買賣點分析:
>這是本項目的核心功能，通過自己定義的 BearBull 買賣指標，直接找到適合的買賣點!
>
> With BearBull Index, you can easily figure out how much should you invest on certain date.
>
3. Technical Analysis 技術分析:
>集成 TA-lib 的多種技術分析函數，一站式檢視股票基本概況!
>
> Various T-A Index integrated, give a quick-view of your stocks!
>


## Story Behind 項目背景
我媽看我學電子所以叫我幫我找股市分析師報的明牌，就這樣第一個功能 **價格搜股** 開發出來了。

自完成價格搜股以來，沉寂了一年多...

到了大四，開始做畢業設計才發現還是 Coding 比較好玩，加上最近看到 Google 的 [TimesFM2.0](https://github.com/google-research/timesfm) 模型推出及 Deepseek 的開源，於是就想說能不能用它們來為股票投資提供一點理性指標。畢竟股票是基於統計學和群眾心理嘛，應該是有規律可循 的，也許能通過模型訓練找到規律並預測之? 我是這樣想的。

我陸續嘗試了 Meta 的 [Prophet](http://facebook.github.io/prophet/)模型、[StatForecast](https://nixtlaverse.nixtla.io/statsforecast/docs/getting-started/getting_started_complete.html)模型，最終選擇使用 Prophet 的後繼模型 [NeuralProphet](https://neuralprophet.com)來預測股價。雖然最終訓練的模型離精準價格預測還有一段距離，但作為趨勢判斷已經相當可以了(未來應該會集成到網站中)，在訓練模型的過程中，我也學會通過 [Optuna](https://optuna.org)調優器來尋找模型的超參數。

有了這項技術，我想也許我可以換個道路，不用求出具體的預測股價，只要能估計目前時間點的賺錢效率就好了~

The preliminary function stemmed from my mom's request to find certain stock based on the given prices, cause the stock analysist usually hid the stock code, for the sake of luring you to join their membership. Thus, the 'Search by Price' function was born. Since then, I started to figure out how to make more use of the stock data with Deep-Learning and Neural models.

At first, I tried the Meta's Prophet model, which is a great model for TSF (Times Series Forecasting), actually it performed quite nice in catching and predicting the stocks' trends, but the results were still far away for making accurate investment suggestions. In spite of not getting so wel with model predicting, I came to know the great tool, Optuna in model training. Optuna is a commonly used framework for finding the best hyper-parameters in model training, with this tool, something different popped out in my head...


## How 開發思路
要求賺錢效率，我有什麼分析工具嗎? 欸，我記得期貨老師教了一堆線圖，什麼兩隻烏鴉、頂分型等等，雖然沒用過，但畢竟是前人驚艷總結，應該有點參考價值吧。
於是我上網扒了一堆 Python packages，找到了一個超棒的庫——[TA-lib](https://ta-lib.org)它囊括了 150 多種技術分析線型及統計指標，更讚的是，它提供型態分析! 也就是說你可以直接調用兩隻烏鴉函數，看看現在的線型是多是空，並給你返回一個量化的分值。
太讚了吧! 那我直接調用把分數拿出來分析不就好了，可是現實不是那麼美好，在我實驗多次以後發現對於同一個日期的股票樣本，不同型態分析常常會給出截然相反的答案，就好像 *2330* 一飛沖天，有些老師跟你說，牛市來了，快追! 有些老師說，高點要反轉了，快撤! 
到底哪個老師 (型態分析) 說得對呢? 
那好吧，我給每個型態分析給出的分數加權求和，定義一個指標叫 *BearBull*，它的本質應該表示在某一個日期該股票應該做空還是做多 (型態分析給出分值的意義) 。

Actually our mission is to make investments more accurately and efficiently, so why not just setup an index to indicate the proficiency of sole investment? 

First of all, how to measure the pattern of the stocks? I browse through the document of the well-used TA-Lib, and I found this, PatternRecognition! It can measure the trends with spcified pattern function and retrurn a figure indicating whether to buy a stock on one date. 

Voila! well done...? 

No, not yet. There are 30+ PatternRecognition functions in TA-Lib, results they give may differ significantly. How to determine which function should I value more, and which should be less accessed? Well, I tried a conventional practice: calculate the weighted average of all functions. Simply we called it the ***BearBull Index***, given as follow:

```math
BearBull = \sum_{i}{w_ix_i}
```
 其中 $w_i$ 表示對每個型態分析指標所賦的權值， $x_i$ 則分別對應它們給出的分值，就這樣， *BearBull* 指標會反映各種型態分析的均衡數值。
不過 TA-lib 提供了 30 幾種型態分析，那我該如何找到那組最有效反映股市多空的權值? 這就要用到剛剛提的 **Optuna** 了，它的基礎功能就是在變量取值的茫茫大海中找到使模型效果最大化的參數，這個功能恰巧就是我在找的。現在我要做的就是定義一個目標函數，讓它幫我找一組參數(權值) 能使這個目標函數得到最大值。
那我要怎麼定義目標函數? 目的是什麼，看在某個時間點做了一筆投資，這筆交易在未來的盈餘能力。因此我定義了一個新的指標: 平均盈餘率 *Average Earning Rate (AER)* ，即在某個時間點根據 BearBull 值做了一筆投資，它在未來一定週期的平均盈餘率。

Apparantly, BearBull represents an overall score given by all functions. Our task is to find an optimal set of weights that could compose a BearBull Index which give the most accurate investment suggestions.

Here, Optuna plays the role.

With a pre-defined goal function, Optuna can 'try' out the best parameters from trials.

So let's define the goal function. To evaluate the capability of earning money, I define the ***AER(Average Earning Rate)*** as follow:

```math
AER = BearBull \times\frac{\sum _{i=1}^{Period}{}P_i-P_0}{P_0\times Period}
```
式中 $Period$ 為時間週期、 $P_i$ ， $P_0$ 分別表示在該週期第 i 天及做交易當日股票的價格，而 BearBull 為負是表示應賣股票；為正時買股票。藉由將一組權值對應 BearBull 在每個日期的 AER 求出來做平均，便能構成能提供 Optuna 尋找權值的目標函數了:

 *AER* represents the average earning rate one would make in single investment in the given $Period$ . With *AER* , I formulaed the goal function as the average *AER* spanning across dates the data covered:
 
 $$Goal = max(Average(AER))$$ 
 
實踐這樣的技術路徑，發現 Optuna 確實能幫我找到一組目標權值，並且提供對應的平均 AER，當然這樣的結果不是最佳的，只是 Optuna 一步步逼近 "試" 出來的，不過觀察線圖確實發現，這樣求出的 BearBull 指標確實能在股票谷底時提供買的訊號、山頂時提前展現賣的訊號。

In practice, Optuna can really help me to find a set of weights along with the corresponding average *AER* . However, one should note that the result isn't the best, it's just the most profitable one Optuna 'try' in the trials. 

In general, this BearBull presents a good indication before the 'summit' and the 'valley' occurs in trends.


## Future Vision 未來願景
1. 繼續透過 NeuralProphet 訓練模型預測股價，預計加入一些提前變量如：美股波動一起訓練。

   Continue training models with NeuralProphet, try to add some advance valuables.
   
3. 完善技術分析部分線圖繪製，開發自定義線圖合一顯示功能。

   Make the TechnicalAnalysis more customizable.
   
5. BearBull 權值參數搜索加速。

   Boost the speed of weights searchign in BearBull section.
   
7. 加入型態分析（其實現在已經有了，只是在背景計算沒顯示出來）

   Add PatternRecognition presentation function (it's now hidden in the background).
   
9. 修復頁面跳轉bug （這是streamlit框架的限制，有待他們解決）

    Fix the page jumping bug.
   
11. 結合大語言模型分析新聞語義，給出基本面及消息面評價指標

    Incorporate the LLM models to analyze the semantics of news, making more general advices for investments.
