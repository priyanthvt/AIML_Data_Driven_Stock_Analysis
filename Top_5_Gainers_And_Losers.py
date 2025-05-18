import pandas as pd
import yaml
from pathlib import Path
from sqlalchemy import create_engine

pd.set_option('display.max_rows', None)

path = Path(r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\data')

top_5_gainers = pd.DataFrame()
top_5_losers = pd.DataFrame()

sorted_folder = sorted(path.iterdir())
for folder in sorted_folder:
    month_return_percentage_list = []
    sorted_yaml_file_path = sorted(folder.iterdir())
    yaml_file_path_list = [yaml_file_path for yaml_file_path in sorted_yaml_file_path]
    month_return_percentage_list.append(yaml_file_path_list[0])
    month_return_percentage_list.append(yaml_file_path_list[-1])

    with open(rf'{month_return_percentage_list[0]}') as open_file:
        open_data = yaml.safe_load(open_file)
    open_df = pd.DataFrame(open_data)

    month_return_percentage_df = pd.DataFrame()

    with open(rf'{month_return_percentage_list[-1]}') as close_file:
        close_data = yaml.safe_load(close_file)
    close_df = pd.DataFrame(close_data)

    month_return_percentage_df = pd.merge(open_df[['Ticker', 'month', 'open']], close_df[['Ticker', 'close']], on ='Ticker',
                                          how = 'inner')

    month_return_percentage_df['Monthly_Return'] = round((((month_return_percentage_df['close'] - month_return_percentage_df['open']) / month_return_percentage_df['open']) * 100), 2)

    month_return_percentage_df = month_return_percentage_df.sort_values(by ='Monthly_Return', ascending = False)

    top_5_gainers = pd.concat([top_5_gainers, month_return_percentage_df.head(5)], ignore_index = True)

    top_5_losers = pd.concat([top_5_losers, month_return_percentage_df.tail(5)], ignore_index = True)

print(top_5_gainers)
print(top_5_losers)


username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

top_5_gainers.to_sql(name='top_5_gainers', con=engine, if_exists='replace', index=False)

top_5_losers.to_sql(name='top_5_losers', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()
