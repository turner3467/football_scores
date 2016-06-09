#! /usr/bin/env python

import numpy as np
import pandas as pd

match_info = ["Season",
              "Div",
              "Date",
              "HomeTeam",
              "AwayTeam"]
match_statistics = ["FTHG",
                    "FTAG",
                    "FTR",
                    "HTHG",
                    "HTAG",
                    "HTR",
                    "Attendance",
                    "Referee",
                    "HS",
                    "AS",
                    "HST",
                    "AST",
                    "HHW",
                    "AHW",
                    "HC",
                    "AC",
                    "HF",
                    "AF",
                    "HO",
                    "AO",
                    "HY",
                    "AY",
                    "HR",
                    "AR",
                    "HBP",
                    "ABP"]

def create_measures_from_historical_scores(df):
    measures = df[match_info].copy()
    measures["Date"] = pd.to_datetime(measures["Date"])
    measures.to_csv("../data/processed/measures.csv")
    return measures

def main():
    historical_scores = pd.read_csv("../data/processed/historical_scores.csv", index_col=0)
    historical_scores = historical_scores[match_info + match_statistics]

    measures = create_measures_from_historical_scores(historical_scores)


if __name__ == "__main__":
    main()