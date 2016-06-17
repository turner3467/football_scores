#! /usr/bin/env python

import os.path
import pandas as pd

match_info = ["Season",
              "League",
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

def get_measures():
    if os.path.isfile("../data/processed/measures.csv"):
        measures = pd.read_csv("../data/processed/measures.csv")
        return measures
    else:
        measures = pd.read_csv("../data/processed/historical_scores.csv", index_col=0)
        measures = measures[match_info]
        measures["Date"] = pd.to_datetime(measures["Date"])
        measures.to_csv("../data/processed/measures.csv")
        return measures

def main():
    measures = get_measures()

    raw_data = pd.read_csv("../data/processed/historical_scores.csv", index_col=0)
    raw_data = raw_data[match_info + match_statistics]

if __name__ == "__main__":
    main()