import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File'
path = Path(folder_path)

excel_file_name_list = [excel_file_path.name
                        for excel_file_path in path.iterdir()
                        if (excel_file_path.is_file() and excel_file_path.suffix in ['.xlsx'])]

green_red_stocks_df = pd.DataFrame(columns = ['Ticker', 'Year_Start_Closing_Price', 'Year_End_Closing_Price'])

for excel_file_name in excel_file_name_list:
    df1 = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')
    stock_symbol = df1['Ticker'].unique()[0]

    year_start_closing_price = df1.loc[0, 'close']
    year_end_closing_price = df1['close'].iloc[-1]

    new_row = pd.DataFrame({'Ticker' : [stock_symbol], 'Year_Start_Closing_Price' : [year_start_closing_price],
                            'Year_End_Closing_Price' : [year_end_closing_price]})
    green_red_stocks_df = pd.concat([green_red_stocks_df, new_row], ignore_index = True)

green_red_stocks_df['Yearly_Return'] = ((green_red_stocks_df['Year_End_Closing_Price'] - green_red_stocks_df['Year_Start_Closing_Price']) / green_red_stocks_df['Year_Start_Closing_Price']) * 100
green_red_stocks_df['Yearly_Return'] = green_red_stocks_df['Yearly_Return'].round(2)
green_red_stocks_df = green_red_stocks_df.sort_values(by ='Yearly_Return', ascending = False)

top_10_green_stocks = green_red_stocks_df.head(10)
top_10_loss_stocks = green_red_stocks_df.tail(10).sort_values(by ='Yearly_Return', ascending = True)

green_red_stocks_df['Green_Red_Stock'] = green_red_stocks_df.apply(lambda row : 'Green' if row['Year_End_Closing_Price'] > row['Year_Start_Closing_Price'] else 'Red', axis = 1)

print(green_red_stocks_df)
print(top_10_green_stocks)
print(top_10_loss_stocks)




username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

green_red_stocks_df.to_sql(name='green_red_stocks', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()