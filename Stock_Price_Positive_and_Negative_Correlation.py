import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

pd.set_option('display.max_rows', None)

stock_list = []
closing_percentage_df = pd.DataFrame()
folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File'

path = Path(folder_path)

excel_file_name_list = [excel_file_path.name
                        for excel_file_path in path.iterdir()
                        if (excel_file_path.is_file() and excel_file_path.suffix in ['.xlsx'])]


for excel_file_name in excel_file_name_list:
    df1 = pd.read_excel(rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{excel_file_name}', engine='openpyxl')
    stock_symbol = df1['Ticker'].unique()[0]
    closing_percentage_df[stock_symbol] = df1['close'].pct_change() * 100

closing_percentage_df = closing_percentage_df.dropna()

correlation_df = closing_percentage_df.corr()

corr_pairs = correlation_df.unstack().reset_index()
corr_pairs.columns = ['Stock_1', 'Stock_2', 'Correlation']

corr_pairs = corr_pairs[corr_pairs['Stock_1'] != corr_pairs['Stock_2']]

corr_pairs['Pair'] = corr_pairs.apply(lambda row: tuple(sorted([row['Stock_1'], row['Stock_2']])), axis=1)
corr_pairs = corr_pairs.drop_duplicates(subset='Pair').drop(columns='Pair')
corr_pairs['Correlation'] = corr_pairs['Correlation'].round(4)

strong_positive_correlation = corr_pairs[corr_pairs['Correlation'] > 0.5]
print(strong_positive_correlation)

negative_correlation = corr_pairs[corr_pairs['Correlation'] < 0]
print(negative_correlation)

username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

strong_positive_correlation.to_sql(name='positive_correlation', con=engine, if_exists='replace', index=False)
negative_correlation.to_sql(name='negative_correlation', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()