#! /usr/bin/env python

import os
import csv
import pandas as pd

file_path = "../data/raw_data"


def process_raw_data(file_path):
    # Collects historical scores from raw csv downloads in give file location

    files = [file for file in os.listdir(file_path)]

    df_list = []

    for file in files:
        country, season, league = os.path.splitext(file)[0].split("_")
        print(country, season, league)
        with open(os.path.join(file_path, file), "r") as input_file:
            reader = csv.reader(input_file)
            header = list(filter(None, next(reader)))
            col_number = len(header)
            file_list = [row[0:col_number] for row in reader if row[0]]

            df = pd.DataFrame(file_list, columns=header)
            try:
                df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%y")
            except ValueError:
                df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
            df['Country'] = country
            df['Season'] = '_'.join([season[0:2], season[2:4]])
            df['League'] = league

            # Find duplicates and drop them
            cols = list(df.columns)
            dup_cols = list(set([x for x in cols if cols.count(x) > 1]))
            df.drop(dup_cols, inplace=True, axis=1)

            df_list.append(df)

    return pd.concat(df_list)

data = process_raw_data(file_path)
data.to_csv("../data/main_data.csv")
