import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)

folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File'
path = Path(folder_path)

excel_file_name_list = [excel_file_path.name
                        for excel_file_path in path.iterdir()
                        if (excel_file_path.is_file() and excel_file_path.suffix in ['.xlsx'])]

number_of_green_vs_red_stocks = pd.DataFrame(columns = ['Ticker', 'Year_Start_Closing_Price', 'Year_End_Closing_Price'])

for excel_file_name in excel_file_name_list:
    df1 = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')
    stock_symbol = df1['Ticker'].unique()[0]

    year_start_closing_price = df1.loc[0, 'close']
    year_end_closing_price = df1['close'].iloc[-1]

    new_row = pd.DataFrame({'Ticker' : [stock_symbol], 'Year_Start_Closing_Price' : [year_start_closing_price],
                            'Year_End_Closing_Price' : [year_end_closing_price]})
    number_of_green_vs_red_stocks = pd.concat([number_of_green_vs_red_stocks, new_row], ignore_index = True)

number_of_green_vs_red_stocks['Green_Red_Stock'] = number_of_green_vs_red_stocks.apply(lambda row : 'Green' if row['Year_End_Closing_Price'] > row['Year_Start_Closing_Price'] else 'Red', axis = 1)

print(number_of_green_vs_red_stocks)


username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

number_of_green_vs_red_stocks.to_sql(name='number_of_green_vs_red_stocks', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()