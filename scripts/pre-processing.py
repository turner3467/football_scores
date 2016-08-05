#! /usr/bin/env python

import os
import csv
import pandas as pd

file_path = "../data/historical scores"


def get_historical_scores(file_path):
    # Collects historical scores from raw csv downloads in give file location

    files = [file for file in os.listdir(file_path)]

    df_list = []

    for file in files:
        season, league = file.strip(".csv").split("_")
        with open(os.path.join(file_path, file), "r") as input_file:
            reader = csv.reader(input_file)
            header = list(filter(None, next(reader)))
            col_number = len(header)
            file_list = [row[0:col_number] for row in reader if row[0]]

            df = pd.DataFrame(file_list, columns=header)
            df['Season'] = season
            df['League'] = league

            df_list.append(df)

    return pd.concat(df_list)

data = get_historical_scores(file_path)
data.to_csv("../data/processed/historical_scores.csv")
