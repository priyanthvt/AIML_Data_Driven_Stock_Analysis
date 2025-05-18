import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File'

path = Path(folder_path)

excel_file_name_list = [excel_file_path.name
                        for excel_file_path in path.iterdir()
                        if (excel_file_path.is_file() and excel_file_path.suffix in ['.xlsx'])]

cumulative_return_over_time_df = pd.DataFrame({'Ticker' : pd.Series(dtype = 'str'), 'Cumulative_Return_Over_Time' : pd.Series(dtype = 'float')})

for excel_file_name in excel_file_name_list:

    df = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')

    df['Daily_Return'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)
    df['Daily_Return'] = df['Daily_Return'].fillna(0)

    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1

    new_row = pd.DataFrame({'Ticker' : [df['Ticker'].iloc[0]], 'Cumulative_Return_Over_Time' : [df['Cumulative_Return'].iloc[-1]]})
    cumulative_return_over_time_df = pd.concat([cumulative_return_over_time_df, new_row], ignore_index=True)

cumulative_return_over_time_df = cumulative_return_over_time_df.sort_values(by = 'Cumulative_Return_Over_Time', ascending=False)
cumulative_return_over_time_df['Cumulative_Return_Over_Time'] = cumulative_return_over_time_df['Cumulative_Return_Over_Time'].round(3)
top_5_performing_stocks = cumulative_return_over_time_df.head(5)
print(top_5_performing_stocks)


username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

top_5_performing_stocks.to_sql(name='cumulative_return_over_time', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()