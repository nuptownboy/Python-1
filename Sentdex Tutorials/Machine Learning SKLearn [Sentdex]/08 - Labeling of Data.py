import pandas as pd
import os
import time
from datetime import datetime
import quandl

api_key = '-ksDg4as87XubzhJVyJQ'

path = '/Users/JohnHanlon/Desktop/Python/Sentdex Tutorials/Machine Learning/Machine Learning SKLearn [Sentdex]/intraQuarter/'

def Key_Stats(gather='Total Debt/Equity (mrq)'):
	stats_path = '{}_KeyStats'.format(path)
	stock_list = [x[0] for x in os.walk(stats_path)]
	df = pd.DataFrame(columns=['Date',
							   'Unix',
							   'Ticker',
							   'DE Ratio',
							   'Price',
							   'stock_p_change'
							   'SP500',
							   'sp500_p_change']) 

	sp500_df = quandl.get('EOD/SPY', authtoken=api_key)



	ticker_list = []

	for each_dir in stock_list[1:25]: #the first output is the root directory, do not want this
		each_file = os.listdir(each_dir)
		ticker = each_dir.split("/")[-1]
		ticker_list.append(ticker)

		starting_stock_value = False
		starting_sp500_value = False


		if len(each_file) > 0:
			for file in each_file:
				date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
				unix_time = time.mktime(date_stamp.timetuple())
				# print(date_stamp, unix_time)

				full_file_path = '{}/{}'.format(each_dir, file)
				# print(full_file_path)
				source = open(full_file_path, 'r', encoding='utf8').read()
				# print(source)
				try:
					value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
					try:
						sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')					
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row['Adj_Close'])
					except:
						sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')					
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row['Adj_Close'])


					stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
					# print('stock price: {}, ticker: {}'.format(stock_price, ticker))

					if not starting_stock_value:
						starting_stock_value = stock_price

					if not starting_sp500_value:
						starting_sp500_value = sp500_value

					stock_p_change = (stock_price - starting_stock_value) / starting_stock_value * 100.0
					sp500_p_change = (sp500_value - starting_sp500_value) / starting_sp500_value * 100.0

					df = df.append({'Date':date_stamp, 
									'Unix':unix_time, 
									'Ticker':ticker, 
									'DE Ratio':value,
									'Price':stock_price,
									'pct change':stock_p_change,
									'sp500':sp500_value,
									'sp500 pct change':sp500_p_change}, ignore_index=True)

				except Exception as e:
					pass
				# print('{}:{}'.format(ticker, value))

				# time.sleep()
	save = gather.replace('','').replace(')','').replace('(','').replace('/','')+('.csv')
	df.to_csv('{}{}'.format(path, save))

Key_Stats()


