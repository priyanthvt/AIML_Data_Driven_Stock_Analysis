import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

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

print(closing_percentage_df)

correlation_df = closing_percentage_df.corr()
print(correlation_df)
# sns.heatmap(correlation_df, annot = True)
# plt.show()


username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

closing_percentage_df.to_sql(name='stock_price_correlation', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()
