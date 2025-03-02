import os
import glob
import pandas as pd
from pathlib import Path
import re


def get_specific_data(office: str, brand: str, goods_services: str) -> pd.DataFrame:
    script_dir = Path(__file__).parent
    folder = script_dir / "../query_data"

    pattern = r"^{}_".format(office)
    if brand:
        pattern += re.escape(brand) + "_"
    if goods_services:
        pattern += re.escape(goods_services) + "_"
    pattern += r"[0-9a-fA-F-]+\.csv$"  # Match the UUID and .txt extension

    regex = re.compile(pattern)
    files = [file for file in folder.iterdir() if file.is_file()]
    matching_files = [file for file in files if regex.match(file.name)]

    if not matching_files:
        raise FileNotFoundError("No matching files found euipo.")

    df = pd.read_csv(folder / matching_files[0], sep=",")
    df = df[sorted(df.columns)]
    columns_sorted = sorted(df.columns)
    columns_sorted.remove("image")
    df = df[columns_sorted]
    text = df.to_csv(index=False, lineterminator='\r\n')

    return text



def combine_files(brand: str | None, goods_services: str | None) -> pd.DataFrame:
    script_dir = Path(__file__).parent
    folder = script_dir / "../query_data"

    pattern = r"^(sipo|euipo|wipo)_"
    if brand:
        pattern += re.escape(brand) + "_"
    if goods_services:
        pattern += re.escape(goods_services) + "_"
    pattern += r"[0-9a-fA-F-]+\.csv$"  # Match the UUID and .txt extension

    regex = re.compile(pattern)
    
    # Get matching files for sipo, euipo, and wipo
    files = []
    files_all = [file for file in folder.resolve().iterdir() if file.is_file()]
    file_names = [x.name for x in files_all]
    file_names = sorted(file_names)
    matching_files = [file_name for file_name in file_names if regex.match(file_name)]
    
    if not matching_files:
        raise FileNotFoundError("No matching files found.")
    
    # Read and concatenate all CSVs
    #dfs = []
    text_all = ""
    for i in range(len(matching_files)):
        df = pd.read_csv(folder / matching_files[i], sep=",")
        df = df[sorted(df.columns)]
        columns_sorted = sorted(df.columns)
        columns_sorted.remove("image")
        df = df[columns_sorted]
        #dfs.append(df)
        text = df.to_csv(index=False, lineterminator='\r\n')
        if i == 0:
            text_all += "euipo: \n" + text
        elif i == 1:
            text_all += "sipo: \n" + text
        elif i == 2:
            text_all += "wipo: \n" + text
        else:
            text_all += text
    #print(texts)
    return text_all

