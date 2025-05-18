import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
stock_list = []

folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File'

path = Path(folder_path)

excel_file_name_list = [excel_file_path.name
                        for excel_file_path in path.iterdir()
                        if (excel_file_path.is_file() and excel_file_path.suffix in ['.xlsx'])]

for excel_file_name in excel_file_name_list:
    df = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')

    stock_symbol = df['Ticker'].unique()[0]
    stock_list.append(stock_symbol)

sector_data_df = pd.read_csv(r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Sector_data.csv')

sector_data_df['Ticker'] = None
sector_data_df['Year_Start_Closing_Price'] = None
sector_data_df['Year_End_Closing_Price'] = None

for stock in stock_list:
    sector_data_df.loc[sector_data_df['Symbol'].str.contains(stock), 'Ticker'] = stock

for excel_file_name in excel_file_name_list:
    df1 = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')
    stock_symbol = df1['Ticker'].unique()[0]

    sector_data_df.loc[(sector_data_df['Ticker'].apply(lambda x : isinstance(x, str)))
                        & (sector_data_df['Ticker'].str.contains(stock_symbol)), 'Year_Start_Closing_Price'] = df1.loc[0, 'close']

    sector_data_df.loc[(sector_data_df['Ticker'].apply(lambda x: isinstance(x, str)))
                       & (sector_data_df['Ticker'].str.contains(stock_symbol)), 'Year_End_Closing_Price'] = df1['close'].iloc[-1]

sector_data_df['Yearly_Return'] = ((sector_data_df['Year_End_Closing_Price']- sector_data_df['Year_Start_Closing_Price']) / sector_data_df['Year_Start_Closing_Price']) * 100

sector_data_df = sector_data_df.dropna()
average_yearly_returns = sector_data_df.groupby(by = 'sector', as_index = False)['Yearly_Return'].mean()
average_yearly_returns['Yearly_Return'] = average_yearly_returns['Yearly_Return'].astype(float)
average_yearly_returns['Yearly_Return'] = average_yearly_returns['Yearly_Return'].round(2)

# print(average_yearly_returns.dtypes)
print(average_yearly_returns)


username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

average_yearly_returns.to_sql(name='sectorwise_performance', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()