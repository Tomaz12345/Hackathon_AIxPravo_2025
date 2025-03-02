import os
import glob
import pandas as pd
from pathlib import Path
import re

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
    matching_files = [file_name for file_name in file_names if regex.match(file_name)]
    
    if not matching_files:
        raise FileNotFoundError("No matching files found.")
    
    # Read and concatenate all CSVs
    dfs = [pd.read_csv(folder /matching_files[i], sep=",") for i in range(len(matching_files))]
    texts = [dfs[i].to_csv(index=False, lineterminator='\r\n') for i in range(len(dfs))]
    #print(texts)
    return texts




if __name__ == "__main__":
    combine_files("Nike", None)