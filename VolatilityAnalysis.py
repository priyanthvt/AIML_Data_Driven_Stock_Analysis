import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File'

path = Path(folder_path)

excel_file_name_list = [excel_file_path.name
                        for excel_file_path in path.iterdir()
                        if (excel_file_path.is_file() and excel_file_path.suffix in ['.xlsx'])]

volatility_analysis_df = pd.DataFrame(columns = ['Ticker', 'Volatility'])

for excel_file_name in excel_file_name_list:
    df = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')

    df['Daily_Return'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)

    stock_symbol = df['Ticker'].unique()[0]
    daily_return_sd = round(df['Daily_Return'].std(), 3)

    new_row = pd.DataFrame({'Ticker' : [f'{stock_symbol}'], 'Volatility' : [f'{daily_return_sd}']})
    volatility_analysis_df = pd.concat([volatility_analysis_df, new_row], ignore_index = True)

volatility_analysis_df['Volatility'] = volatility_analysis_df['Volatility'].astype(float)
volatility_analysis_df = volatility_analysis_df.sort_values(by='Volatility', ascending = False)
top_10_volatile_stocks = volatility_analysis_df.head(10)

print(volatility_analysis_df)
print(top_10_volatile_stocks)


username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

top_10_volatile_stocks.to_sql(name='volatility_analysis', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()