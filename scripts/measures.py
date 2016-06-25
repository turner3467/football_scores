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
    """Returns measures dataframe.

    If measures file does not exists, it uses a filtered down version of the raw historical scores csv.
    """

    if os.path.isfile("../data/processed/measures.csv"):
        measures = pd.read_csv("../data/processed/measures.csv")
        measures.Date = pd.to_datetime(measures.Date)
        return measures
    else:
        measures = pd.read_csv("../data/processed/historical_scores.csv", index_col=0)
        measures = measures[match_info]
        measures.Date = pd.to_datetime(measures.Date)
        measures = measures.reset_index()
        measures.to_csv("../data/processed/measures.csv")
        return measures

def team_win_percentage(df, team, n_games):
    """Returns the team win percentage from last n games."""

    temp_df = df[(df.HomeTeam == team) | (df.AwayTeam == team)]
    temp_df = temp_df.sort_values("Date", ascending=False).head(n_games)[["HomeTeam", "AwayTeam", "FTR"]]
    if len(temp_df) < n_games:
        return "NaN"
    wins = ((temp_df.HomeTeam == team) & (temp_df.FTR == "H")) | \
           ((temp_df.AwayTeam == team) & (temp_df.FTR == "A"))
    win_percent = wins.sum() / n_games
    return round(win_percent, 2)

def team_lose_percentage(df, team, n_games):
    """Returns the team win percentage from last n games."""

    temp_df = df[(df.HomeTeam == team) | (df.AwayTeam == team)]
    temp_df = temp_df.sort_values("Date", ascending=False).head(n_games)[["HomeTeam", "AwayTeam", "FTR"]]
    if len(temp_df) < n_games:
        return "NaN"
    loses = ((temp_df.HomeTeam == team) & (temp_df.FTR == "A")) | \
           ((temp_df.AwayTeam == team) & (temp_df.FTR == "H"))
    lose_percent = loses.sum() / n_games
    return round(lose_percent, 2)

def form_measures(idx, df):
    """Master function to calculate form based measures. Main purpose of this function is to provide a filtered
    dataframe to sub-functions which will calculate individual measures. See measures.md for description of measures."""

    date, home_team, away_team = df.loc[idx, ["Date", "HomeTeam", "AwayTeam"]]

    row_filter = df.Date < date
    row_filter = row_filter & ((df.HomeTeam.isin([home_team, away_team])) |
                               df.AwayTeam.isin([home_team, away_team]))

    temp_df = df[row_filter]

    home_team_win_percent_last_5 = team_win_percentage(temp_df, home_team, 5)
    home_team_win_percent_last_10 = team_win_percentage(temp_df, home_team, 10)
    home_team_win_percent_last_15 = team_win_percentage(temp_df, home_team, 15)
    away_team_win_percent_last_5 = team_win_percentage(temp_df, away_team, 5)
    away_team_win_percent_last_10 = team_win_percentage(temp_df, away_team, 10)
    away_team_win_percent_last_15 = team_win_percentage(temp_df, away_team, 15)
    home_team_lose_percent_last_5 = team_lose_percentage(temp_df, home_team, 5)
    home_team_lose_percent_last_10 = team_lose_percentage(temp_df, home_team, 10)
    home_team_lose_percent_last_15 = team_lose_percentage(temp_df, home_team, 15)
    away_team_lose_percent_last_5 = team_lose_percentage(temp_df, away_team, 5)
    away_team_lose_percent_last_10 = team_lose_percentage(temp_df, away_team, 10)
    away_team_lose_percent_last_15 = team_lose_percentage(temp_df, away_team, 15)

    output_list = [home_team_win_percent_last_5,
                   home_team_win_percent_last_10,
                   home_team_win_percent_last_15,
                   away_team_win_percent_last_5,
                   away_team_win_percent_last_10,
                   away_team_win_percent_last_15,
                   home_team_lose_percent_last_5,
                   home_team_lose_percent_last_10,
                   home_team_lose_percent_last_15,
                   away_team_lose_percent_last_5,
                   away_team_lose_percent_last_10,
                   away_team_lose_percent_last_15]

    return output_list

def main():
    measures = get_measures()

    raw_data = pd.read_csv("../data/processed/historical_scores.csv", index_col=0)
    raw_data = raw_data[match_info + match_statistics]
    raw_data.Date = pd.to_datetime(raw_data.Date)
    raw_data = raw_data.reset_index()

    print(form_measures(551, raw_data))

if __name__ == "__main__":
    main()
