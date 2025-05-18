import pandas as pd
import yaml
from pathlib import Path

path = Path(r'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\data')

folder_list = [folder.name for folder in path.iterdir() if folder.is_dir()]
df_list = []

for folder_name in folder_list:
    file_path = path / folder_name
    yaml_file_path_list = [yaml_file for yaml_file in file_path.iterdir() if (yaml_file.is_file() and yaml_file.suffix in ['.yaml', '.yml'])]
    # print(file_name)

    for yaml_file_path in yaml_file_path_list:
        with open( rf'{yaml_file_path}' ) as f:
            data = yaml.safe_load(f)

        df = pd.DataFrame(data)
        df_list.append(df)

stock_list = pd.concat(df_list, ignore_index = True)

df_groupby = stock_list.groupby('Ticker')
print(df_groupby)

for symbol, group in df_groupby:
    group.to_excel(
        rf'C:\Users\Sheasaanth\Desktop\Priyanth\Projects\Data_Driven_Stock_Analysis\Ticker_Excel_File\{symbol}.xlsx',
        index=False)
print('converted yaml to excel')