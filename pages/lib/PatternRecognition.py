
import talib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from talib import abstract

#型態識別 Pattern Recognition
def pattern_recognition(df,PR,PR_property,PR_name):
    
    '''PR_col = ['cdl2crows','cdl3blackcrows','cdl3inside','cdl3linestrike','cdleveningstar','cdl3outside','cdl3starsinsouth','cdl3whitesoldiers',
            'cdladbandonedbaby','cdladvanceblock','cdlbelthold','cdlbreakaway','cdlclosingmazubozu','cdlconcealbabyswall','cdlcounterattack',
            'cdldarkcloudcover','cdldoji','cdldojistar','cdldragonflydoji','cdlengulfing','cdleveningdojistar','cdlrisefall3methods',
            'cdlgapsidesidewhite','cdlgravestonedoji','cdlhammer','cdlharami','cdlharamicross','cdlhighwave','cdlhikkake','cdlhikkakemod',
            'cdlhomingpigeon','cdlidentical3crows','cdlinneck','cdlinvertedhammer','cdlkicking','cdlkickingbylength','cdlladderbottom','cdllongleggeddoji',
            'cdlmarubozu','cdlmatchinglow','cdlmathold','cdlmorningdojistar','cdlmorningstar','cdlonneck','cdlpiercing','cdlrickshawman','cdlseparatinglines',
            'cdlshootingstar','cdlstalledpattern','cdlsticksandwitch','cdltasukigap','cdlthrusting','cdltristar','cdlunique3river','cdlupsidegap2crows','cdlupsidegap2crows',
            'cdlxsidegap3methods']'''

    


    #兩隻烏鴉
    PR_property.loc['info','cdl2crows'] = '簡介：三日K線模式，第一天長陽，第二天高開收陰，第三天再次高開繼續收陰，收盤比前一日收盤價低，預示股價下跌。'
    PR_property.loc['EN_name','cdl2crows'] = '2 Crows'
    PR_property.loc['CN_name','cdl2crows'] = '兩隻烏鴉'
    cdl2crows = abstract.CDL2CROWS(df)
    PR['cdl2crows'] = cdl2crows

    #三隻烏鴉
    PR_property.loc['info','cdl3blackcrows'] = '簡介：三日K線模式，連續三根陰線，每日收盤價都下跌且接近最低價，每日開盤價都在上根K線實體內，預示股價下跌。'
    PR_property.loc['EN_name','cdl3blackcrows'] = '3 Black Crows'
    PR_property.loc['CN_name','cdl3blackcrows'] = '三隻烏鴉'
    cdl3blackcrows = abstract.CDL3BLACKCROWS(df)
    PR['cdl3blackcrows'] = cdl3blackcrows


    #內三漲三跌
    PR_property.loc['info','cdl3inside'] = '簡介：三日K線模式，母子信號+長K線，以三內部上漲為例，K線為陰陽陽，第三天收盤價高於第一天開盤價，第二天K線在第一天K線內部，預示著股價上漲。'
    PR_property.loc['EN_name','cdl3inside'] = '3 Inside Up/Down'
    PR_property.loc['CN_name','cdl3inside'] = '內三漲三跌'
    cdl3inside = abstract.CDL3INSIDE(df)
    PR['cdl3inside'] = cdl3inside


    #三線打擊

    PR_property.loc['info','cdl3linestrike'] = '簡介：四日K線模式，前三根陽線，每日收盤價都比前一日高，開盤價在前一日實體內，第四日市場高開，收盤價低於第一日開盤價，預示股價下跌。'
    PR_property.loc['EN_name','cdl3linestrike'] = '3 Lines Strike'
    PR_property.loc['CN_name','cdl3linestrike'] = '三線打擊'
    cdl3linestrike = abstract.CDL3LINESTRIKE(df)
    PR['cdl3linestrike'] = cdl3linestrike

    #外三漲三跌
    ''''''
    PR_property.loc['info','cdl3outside'] = '簡介：三日K線模式，與三內部上漲和下跌類似，K線為陰陽陽，但第一日與第二日的K線形態相反，以三外部上漲為例，第一日K線在第二日K線內部，預示著股價上漲。'
    PR_property.loc['EN_name','cdl3outside'] = '3 Outside Up/Down'
    PR_property.loc['CN_name','cdl3outside'] = '外三漲三跌'
    cdl3outside = abstract.CDL3OUTSIDE(df)
    PR['cdl3outside'] = cdl3outside

    # 南方三星
    ''''''
    PR_property.loc['info','cdl3starsinsouth'] = '簡介：三日K線模式，與大敵當前相反，三日K線皆陰，第一日有長下影線，第二日與第一日類似，K線整體小於第一日，第三日無下影線實體信號，成交價格都在第一日振幅之內，預示下跌趨勢反轉，股價上升。'
    PR_property.loc['EN_name','cdl3starsinsouth'] = '3 Stars in South'
    PR_property.loc['CN_name','cdl3starsinsouth'] = '南方三星'
    cdl3starsinsouth = abstract.CDL3STARSINSOUTH(df)
    PR['cdl3starsinsouth'] = cdl3starsinsouth

    #三個白兵
    ''''''
    PR_property.loc['info','cdl3whitesoldiers'] = '簡介：三日K線模式，三日K線皆陽，每日收盤價變高且接近最高價，開盤價在前一日實體上半部，預示股價上升。'
    PR_property.loc['EN_name','cdl3whitesoldiers'] = '3 White Soldiers'
    PR_property.loc['CN_name','cdl3whitesoldiers'] = '三個白兵'
    cdl3whitesoldiers = abstract.CDL3WHITESOLDIERS(df)
    PR['cdl3whitesoldiers'] = cdl3whitesoldiers

    #棄嬰
    ''''''
    PR_property.loc['info','cdlabandonedbaby'] = '簡介：三日K線模式，第二日價格跳空且收十字星（開盤價與收盤價接近，最高價最低價相差不大），預示趨勢反轉，發生在頂部下跌，底部上漲。'
    PR_property.loc['EN_name','cdlabandonedbaby'] = 'Abandoned Baby'
    PR_property.loc['CN_name','cdlabandonedbaby'] = '棄嬰'
    cdladbandonedbaby = abstract.CDLABANDONEDBABY(df)
    PR['cdlabandonedbaby'] = cdladbandonedbaby

    #大敵當前
    ''''''
    PR_property.loc['info','cdladvanceblock'] = '簡介：三日K線模式，三日都收陽，每日收盤價都比前一日高，開盤價都在前一日實體以內，實體變短，上影線變長。'
    PR_property.loc['EN_name','cdladvanceblock'] = 'Advance Block'
    PR_property.loc['CN_name','cdladvanceblock'] = '大敵當前'
    cdladvanceblock = abstract.CDLADVANCEBLOCK(df)
    PR['cdladvanceblock'] = cdladvanceblock

    #捉腰帶線
    PR_property.loc['info','cdlbelthold'] = '簡介：兩日K線模式，下跌趨勢中，第一日陰線，第二日開盤價為最低價，陽線，收盤價接近最高價，預示價格上漲。'
    PR_property.loc['EN_name','cdlbelthold'] = 'Belt Hold'
    PR_property.loc['CN_name','cdlbelthold'] = '捉腰帶線'
    cdlbelthold = abstract.CDLBELTHOLD(df)
    PR['cdlbelthold'] = cdlbelthold

    #脫離
    ''''''
    PR_property.loc['info','cdlbreakaway'] = '簡介：五日K線模式，以看漲脫離為例，下跌趨勢中，第一日長陰線，第二日跳空陰線，延續趨勢開始震盪，第五日長陽線，收盤價在第一天收盤價與第二天開盤價之間，預示價格上漲。'
    PR_property.loc['EN_name','cdlbreakaway'] = 'Breakaway'
    PR_property.loc['CN_name','cdlbreakaway'] = '脫離'
    cdlbreakaway = abstract.CDLBREAKAWAY(df)
    PR['cdlbreakaway'] = cdlbreakaway


    #藏嬰吞沒
    ''''''
    PR_property.loc['info','cdlconcealbabyswall'] = '簡介：四日K線模式，下跌趨勢中，前兩日陰線無影線，第二日開盤、收盤價皆低於第二日，第三日倒錘頭，第四日開盤價高於前一日最高價，收盤價低於前一日最低價，預示著底部反轉。'
    PR_property.loc['EN_name','cdlconcealbabyswall'] = 'ConcealBaby Swallow'
    PR_property.loc['CN_name','cdlconcealbabyswall'] = '藏嬰吞沒'
    cdlconcealbabyswall = abstract.CDLCONCEALBABYSWALL(df)
    PR['cdlconcealbabyswall'] = cdlconcealbabyswall

    #反擊線
    ''''''
    PR_property.loc['info','cdcounterattack'] = '簡介：二日K線模式，與分離線類似。'
    PR_property.loc['EN_name','cdcounterattack'] = 'Counter-Attack'
    PR_property.loc['CN_name','cdcounterattack'] = '反擊線'
    cdlcounterattack = abstract.CDLCOUNTERATTACK(df)
    PR['cdcounterattack'] = cdlcounterattack

    #烏雲壓頂
    ''''''
    PR_property.loc['info','cdldarkcloudcover'] = '簡介：二日K線模式，第一日長陽，第二日開盤價高於前一日最高價，收盤價處於前一日實體中部以下，預示著股價下跌。 '
    PR_property.loc['EN_name','cdldarkcloudcover'] = 'Dark Cloud Cover'
    PR_property.loc['CN_name','cdldarkcloudcover'] = '烏雲壓頂'
    cdldarkcloudcover = abstract.CDLDARKCLOUDCOVER(df)
    PR['cdldarkcloudcover'] = cdldarkcloudcover


    #十字星
    ''''''
    PR_property.loc['info','cdldojistar'] = '簡介：一日K線模式，開盤價與收盤價基本相同，上下影線不會很長，預示著當前趨勢反轉。 '
    PR_property.loc['EN_name','cdldojistar'] = 'Doji Star'
    PR_property.loc['CN_name','cdldojistar'] = '十字星'
    cdldojistar = abstract.CDLDOJISTAR(df)
    PR['cdldojistar'] = cdldojistar

    #蜻蜓十字
    ''''''
    PR_property.loc['info','cdldragonflydoji'] = '簡介：一日K線模式，開盤後價格一路走低，之後收復，收盤價與開盤價相同，預示趨勢反轉。 '
    PR_property.loc['EN_name','cdldragonflydoji'] = 'Dragonfly Doji'
    PR_property.loc['CN_name','cdldragonflydoji'] = '蜻蜓十字'
    cdldragonflydoji = abstract.CDLDRAGONFLYDOJI(df)
    PR['cdldragonflydoji'] = cdldragonflydoji


    #十字暮星
    ''''''
    PR_property.loc['info','cdleveningdojistar'] = '簡介：三日K線模式，基本模式為暮星，第二日收盤價和開盤價相同，預示頂部反轉。'
    PR_property.loc['EN_name','cdleveningdojistar'] = 'Evening Doji Star'
    PR_property.loc['CN_name','cdleveningdojistar'] = '十字暮星'
    cdleveningdojistar = abstract.CDLEVENINGDOJISTAR(df)
    PR['cdleveningdojistar'] = cdleveningdojistar

    #暮星
    ''''''
    PR_property.loc['info','cdleveningstar'] = '簡介：三日K線模式，與晨星相反，上升趨勢中,第一日陽線，第二日價格振幅較小，第三日陰線，預示頂部反轉。'
    PR_property.loc['EN_name','cdleveningstar'] = 'Evening Star'
    PR_property.loc['CN_name','cdleveningstar'] = '暮星'
    cdleveningstar = abstract.CDLEVENINGSTAR(df)
    PR['cdleveningstar'] = cdleveningstar

    #向上/向下跳空並列陽線
    ''''''
    PR_property.loc['info','cdlgapsidesidewhite'] = '簡介：二日K線模式，上升趨勢向上跳空，下跌趨勢向下跳空,第一日與第二日有相同開盤價，實體長度差不多，則趨勢持續。'
    PR_property.loc['EN_name','cdlgapsidesidewhite'] = 'Gap Side by Side White'
    PR_property.loc['CN_name','cdlgapsidesidewhite'] = '向上/向下跳空並列陽線'
    cdlgapsidesidewhite = abstract.CDLGAPSIDESIDEWHITE(df)
    PR['cdlgapsidesidewhite'] = cdlgapsidesidewhite

    #墓碑十字/倒T十字
    ''''''
    PR_property.loc['info','cdlgravestonedoji'] = '簡介：一日K線模式，開盤價與收盤價相同，上影線長，無下影線，預示底部反轉。'
    PR_property.loc['EN_name','cdlgravestonedoji'] = 'Gravestone Doji'
    PR_property.loc['CN_name','cdlgravestonedoji'] = '墓碑十字/倒T十字'
    cdlgravestonedoji = abstract.CDLGRAVESTONEDOJI(df)
    PR['cdlgravestonedoji'] = cdlgravestonedoji


    #母子線
    ''''''
    PR_property.loc['info','cdlharami'] = '簡介：二日K線模式，分多頭母子與空頭母子，兩者相反，以多頭母子為例，在下跌趨勢中，第一日K線長陰，第二日開盤價收盤價在第一日價格振幅之內，為陽線，預示趨勢反轉，股價上升。'
    PR_property.loc['EN_name','cdlharami'] = 'Harami Line'
    PR_property.loc['CN_name','cdlharami'] = '母子線'
    cdlharami = abstract.CDLHARAMI(df)
    PR['cdlharami'] = cdlharami


    #三胞胎烏鴉
    ''''''
    PR_property.loc['info','cdlidentical3crows'] = '簡介：三日K線模式，上漲趨勢中，三日都為陰線，長度大致相等，每日開盤價等於前一日收盤價，收盤價接近當日最低價，預示價格下跌。'
    PR_property.loc['EN_name','cdlidentical3crows'] = 'Identical 3 Crows'
    PR_property.loc['CN_name','cdlidentical3crows'] = '三胞胎烏鴉'
    cdlidentical3crows = abstract.CDLIDENTICAL3CROWS(df)
    PR['cdlidentical3crows'] = cdlidentical3crows

    #頸內線
    ''''''
    PR_property.loc['info','cdlinneck'] = '簡介：二日K線模式，下跌趨勢中，第一日長陰線，第二日開盤價較低，收盤價略高於第一日收盤價，陽線，實體較短，預示著下跌繼續。'
    PR_property.loc['EN_name','cdlinneck'] = 'In-Neck Line'
    PR_property.loc['CN_name','cdlinneck'] = '頸內線'
    cdlinneck = abstract.CDLINNECK(df)
    PR['cdlinneck'] = cdlinneck

    #倒錘頭
    ''''''
    PR_property.loc['info','cdlinvertedhammer'] = '簡介：一日K線模式，上影線較長，長度為實體2倍以上，無下影線，在下跌趨勢底部，預示著趨勢反轉。'
    PR_property.loc['EN_name','cdlinvertedhammer'] = 'Inverted Hammer'
    PR_property.loc['CN_name','cdlinvertedhammer'] = '倒錘頭'
    cdlinvertedhammer = abstract.CDLINVERTEDHAMMER(df)
    PR['cdlinvertedhammer'] = cdlinvertedhammer

    #反沖型態
    ''''''
    PR_property.loc['info','cdlkicking'] = '簡介：二日K線模式，與分離線類似，兩日K線為禿線，顏色相反，存在跳空缺口。'
    PR_property.loc['EN_name','cdlkicking'] = 'Kicking'
    PR_property.loc['CN_name','cdlkicking'] = '反沖型態'
    cdlkicking = abstract.CDLKICKING(df)
    PR['cdlkicking'] = cdlkicking

    #由較長缺影線決定的反沖型態
    ''''''
    PR_property.loc['info','cdlkickingbylength'] = '簡介：二日K線模式，與反沖形態類似，較長缺影線決定價格的漲跌。'
    PR_property.loc['EN_name','cdlkickingbylength'] = 'Kicking by Length'
    PR_property.loc['CN_name','cdlkickingbylength'] = '由較長缺影線決定的反沖型態'
    cdlkickingbylength = abstract.CDLKICKINGBYLENGTH(df)
    PR['cdlkickingbylength'] = cdlkickingbylength


    #梯底
    ''''''
    PR_property.loc['info','cdlladderbottom'] = '簡介：五日K線模式，下跌趨勢中，前三日陰線，開盤價與收盤價皆低於前一日開盤、收盤價，第四日倒錘頭，第五日開盤價高於前一日開盤價，陽線，收盤價高於前幾日價格振幅，預示著底部反轉。'
    PR_property.loc['EN_name','cdlladderbottom'] = 'Ladder Bottom'
    PR_property.loc['CN_name','cdlladderbottom'] = '梯底'
    cdlladderbottom = abstract.CDLLADDERBOTTOM(df)
    PR['cdlladderbottom'] = cdlladderbottom

    #光頭光腳/缺影線
    ''''''
    PR_property.loc['info','cdlmarubozu'] = '簡介：一日K線模式，上下兩頭都沒有影線的實體，陰線預示著熊市持續或者牛市反轉，陽線相反。'
    PR_property.loc['EN_name','cdlmarubozu'] = 'Marubozu Line'
    PR_property.loc['CN_name','cdlmarubozu'] = '光頭光腳/缺影線'
    cdlmarubozu = abstract.CDLMARUBOZU(df)
    PR['cdlmarubozu'] = cdlmarubozu

    #相同低價
    ''''''
    PR_property.loc['info','cdlmatchinglow'] = '簡介：二日K線模式，下跌趨勢中，第一日長陰線，第二日陰線，收盤價與前一日相同，預示底部確認，該價格為支撐位。'
    PR_property.loc['EN_name','cdlmatchinglow'] = 'Matching Low'
    PR_property.loc['CN_name','cdlmatchinglow'] = '相同低價'
    cdlmatchinglow = abstract.CDLMATCHINGLOW(df)
    PR['cdlmatchinglow'] = cdlmatchinglow

    #十字晨星
    ''''''
    PR_property.loc['info','cdlmorningdojistar'] = '簡介：三日K線模式，基本模式為晨星，第二日K線為十字星，預示底部反轉。'
    PR_property.loc['EN_name','cdlmorningdojistar'] = 'Morning Doji Star'
    PR_property.loc['CN_name','cdlmorningdojistar'] = '十字晨星'
    cdlmorningdojistar = abstract.CDLMORNINGDOJISTAR(df)
    PR['cdlmorningdojistar'] = cdlmorningdojistar

    #晨星
    ''''''
    PR_property.loc['info','cdlmorningstar'] = '簡介：三日K線模式，下跌趨勢，第一日陰線，第二日價格振幅較小，第三天陽線，預示底部反轉。'
    PR_property.loc['EN_name','cdlmorningstar'] = 'Morning Star'
    PR_property.loc['CN_name','cdlmorningstar'] = '晨星'
    cdlmorningstar = abstract.CDLMORNINGSTAR(df)
    PR['cdlmorningstar'] = cdlmorningstar

    #頸上線
    ''''''
    PR_property.loc['info','cdlonneck'] = '簡介：二日K線模式，下跌趨勢中，第一日長陰線，第二日開盤價較低，收盤價與前一日最低價相同，陽線，實體較短，預示著延續下跌趨勢。'
    PR_property.loc['EN_name','cdlonneck'] = 'On-Neck Line'
    PR_property.loc['CN_name','cdlonneck'] = '頸上線'
    cdlonneck = abstract.CDLONNECK(df)
    PR['cdlonneck'] = cdlonneck

    #刺透型態
    ''''''
    PR_property.loc['info','cdlpiercing'] = '簡介：兩日K線模式，下跌趨勢中，第一日陰線，第二日收盤價低於前一日最低價，收盤價處在第一日實體上部，預示著底部反轉。'
    PR_property.loc['EN_name','cdlpiercing'] = 'Piercing'
    PR_property.loc['CN_name','cdlpiercing'] = '刺透型態'
    cdlpiercing = abstract.CDLPIERCING(df)
    PR['cdlpiercing'] = cdlpiercing


    #上升/下降三法
    ''''''
    PR_property.loc['info','cdlrisefall3methods'] = '簡介：五日K線模式，以上升三法為例，上漲趨勢中，第一日長陽線，中間三日價格在第一日範圍內小幅震盪，第五日長陽線，收盤價高於第一日收盤價，預示股價上升。'
    PR_property.loc['EN_name','cdlrisefall3methods'] = 'Rise/Fall 3 Methods'
    PR_property.loc['CN_name','cdlrisefall3methods'] = '上升/下降三法'
    cdlrisefall3methods = abstract.CDLRISEFALL3METHODS(df)
    PR['cdlrisefall3methods'] = cdlrisefall3methods


    #射擊之星
    ''''''
    PR_property.loc['info','cdlshootingstar'] = '簡介：一日K線模式，上影線至少為實體長度兩倍，沒有下影線，預示著股價下跌。'
    PR_property.loc['EN_name','cdlshootingstar'] = 'Shooting Star'
    PR_property.loc['CN_name','cdlshootingstar'] = '射擊之星'
    cdlshootingstar = abstract.CDLSHOOTINGSTAR(df)
    PR['cdlshootingstar'] = cdlshootingstar


    #條形三明治
    ''''''
    PR_property.loc['info','cdlsticksandwitch'] = '簡介：三日K線模式，第一日長陰線，第二日陽線，開盤價高於前一日收盤價，第三日開盤價高於前兩日最高價，收盤價於第一日收盤價相同。'
    PR_property.loc['EN_name','cdlsticksandwitch'] = 'Stick Sandwitch'
    PR_property.loc['CN_name','cdlsticksandwitch'] = '條形三明治'
    cdlsticksandwitch = abstract.CDLSTICKSANDWICH(df)
    PR['cdlsticksandwitch'] = cdlsticksandwitch

    #跳空並列陰陽線
    ''''''
    PR_property.loc['info','cdltasukigap'] = '簡介：三日K線模式，分上漲和下跌，以上升為例，前兩日陽線，第二日跳空，第三日陰線，收盤價於缺口中，上升趨勢持續。'
    PR_property.loc['EN_name','cdltasukigap'] = 'Tasuki Gap'
    PR_property.loc['CN_name','cdltasukigap'] = '跳空並列陰陽線'
    cdltasukigap = abstract.CDLTASUKIGAP(df)
    PR['cdltasukigap'] = cdltasukigap

    #插入
    ''''''
    PR_property.loc['info','cdlthrusting'] = '簡介：二日K線模式，與頸上線類似，下跌趨勢中，第一日長陰線，第二日開盤價跳空，收盤價略低於前一日實體中部，與頸上線相比實體較長，預示著趨勢持續。'
    PR_property.loc['EN_name','cdlthrusting'] = 'Thrusting'
    PR_property.loc['CN_name','cdlthrusting'] = '插入'
    cdlthrusting = abstract.CDLTHRUSTING(df)
    PR['cdlthrusting'] = cdlthrusting


    #向上跳空的兩隻烏鴉
    ''''''
    PR_property.loc['info','cdlupsidegap2crows'] = '簡介：三日K線模式，第一日陽線，第二日跳空以高於第一日最高價開盤，收陰線，第三日開盤價高於第二日，收陰線，與第一日比仍有缺口。'
    PR_property.loc['EN_name','cdlupsidegap2crows'] = 'Up-Side Gap 2 Crows'
    PR_property.loc['CN_name','cdlupsidegap2crows'] = '向上跳空的兩隻烏鴉'
    cdlupsidegap2crows = abstract.CDLUPSIDEGAP2CROWS(df)
    PR['cdlupsidegap2crows'] = cdlupsidegap2crows

    #上升/下降跳空三法
    ''''''
    PR_property.loc['info','cdlxsidegap3methods'] = '簡介：五日K線模式，以上升跳空三法為例，上漲趨勢中，第一日長陽線，第二日短陽線，第三日跳空陽線，第四日陰線，開盤價與收盤價於前兩日實體內，第五日長陽線，收盤價高於第一日收盤價，預示股價上升。'
    PR_property.loc['EN_name','cdlxsidegap3methods'] = 'X-Side Gap 3 Methods'
    PR_property.loc['CN_name','cdlxsidegap3methods'] = '上升/下降跳空三法'
    cdlxsidegap3methods = abstract.CDLXSIDEGAP3METHODS(df)
    PR['cdlxsidegap3methods'] = cdlxsidegap3methods

    PR.reset_index(inplace=True)
    PR.rename({'date':'ds'},inplace=True)
    
    PR_name['names'] = pd.Series(PR_property.columns)
    PR_name['w_names'] = 'w_' + PR_name.names.values 