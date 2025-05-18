import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)

folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File'
path = Path(folder_path)

excel_file_name_list = [excel_file_path.name
                        for excel_file_path in path.iterdir()
                        if (excel_file_path.is_file() and excel_file_path.suffix in ['.xlsx'])]

average_price_df = pd.DataFrame(columns = ['Ticker', 'Average_Price'])

for excel_file_name in excel_file_name_list:
    df1 = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')
    stock_symbol = df1['Ticker'].unique()[0]
    average_price = df1['close'].mean()

    new_row = pd.DataFrame({'Ticker' : [stock_symbol], 'Average_Price' : [average_price]})
    average_price_df = pd.concat([average_price_df, new_row], ignore_index = True)

average_price_df['Average_Price'] = average_price_df['Average_Price'].round(2)

print(average_price_df)

average_price_across_all_stocks = average_price_df['Average_Price'].mean()

print(round(average_price_across_all_stocks))


username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

average_price_df.to_sql(name='stocks_average_price', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()