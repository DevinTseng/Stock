
from FinMind.data import DataLoader
import pandas as pd
api = DataLoader()

def FetchPrice(stock_id, start_date, end_date):
    data = api.taiwan_stock_daily(
    stock_id = stock_id,
    start_date = start_date,
    end_date = end_date,
    )
    #Data Formtting
    data.index = data.date
    data.rename(columns={'date': 'ds','max':'high','min':'low','Trading_Volume':'volume'}, inplace=True)
    data.ds = pd.to_datetime(data['ds'])
    return data