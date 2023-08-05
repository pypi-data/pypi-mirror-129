from numpy import add
from rltrade import config
from rltrade.data import IBKRDownloader,DayTradeFeatureEngineer

train_period = ('2021-11-23','2021-11-24') #for training the model
test_period = ('2021-11-24','2021-11-25') 

path = 'models/daytrade/dow30'
ticker_list = config.DOW_30_TICKER[:5]
tech_indicators = config.STOCK_INDICATORS_LIST # indicators from stockstats
additional_indicators = config.ADDITIONAL_DAYTRADE_INDICATORS

print('Downloading Data')
df = IBKRDownloader(start_date = train_period[0], # first date
                    end_date = test_period[1], #last date
                    ticker_list = ticker_list).fetch_min_data(demo=True) #requires subscription

fe = DayTradeFeatureEngineer(stock_indicator_list=tech_indicators,
                            additional_indicators=additional_indicators)

train,test = fe.train_test_split(df,train_period,test_period)