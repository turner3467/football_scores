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

## Helper functions
def match_filter(df,
                 home_team,
                 away_team,
                 n_games,
                 venue,
                 head_to_head,
                 team):
    """Returns matches as dataframe filtered by team, venue, and last n games"""
    
    cols_returned = ["HomeTeam", "AwayTeam", "FTR", "FTHG", "FTAG"]
    if head_to_head:
        df_filter = ((df.HomeTeam == home_team) & (df.AwayTeam == away_team)) | \
                    ((df.HomeTeam == away_team) & (df.AwayTeam == home_team))        
        temp_df = df[df_filter]
    elif venue == "home":
        temp_df = df[df.HomeTeam == home_team]
        temp_df = temp_df.sort_values("Date", ascending=False).head(n_games)[cols_returned]
    elif venue == "away":
        temp_df = df[df.AwayTeam == away_team]
        temp_df = temp_df.sort_values("Date", ascending=False).head(n_games)[cols_returned]
    else:
        if team == "home":
            temp_df = df[(df.HomeTeam == home_team) | (df.AwayTeam == home_team)]
        else:
            temp_df = df[(df.HomeTeam == away_team) | (df.AwayTeam == away_team)]
        temp_df = temp_df.sort_values("Date", ascending=False).head(n_games)[cols_returned]
    return temp_df

## Individual measure functions
def team_win_percentage(df, home_team, away_team, n_games, venue, head_to_head, team):
    """Returns the team win percentage from last n games."""

    temp_df = match_filter(df, home_team, away_team, n_games, venue, head_to_head, team)
    if len(temp_df) < n_games:
        return "NaN"
    if team == "home":
        wins = ((temp_df.HomeTeam == home_team) & (temp_df.FTR == "H")) | \
               ((temp_df.AwayTeam == home_team) & (temp_df.FTR == "A"))
    else:
        wins = ((temp_df.HomeTeam == away_team) & (temp_df.FTR == "H")) | \
               ((temp_df.AwayTeam == away_team) & (temp_df.FTR == "A"))
    if n_games != 1:
        output = round(wins.sum() / n_games, 2)
    else:
        output = wins.sum()
    return output

def team_lose_percentage(df, home_team, away_team, n_games, venue, head_to_head, team):
    """Returns the team lose percentage from last n games."""

    temp_df = match_filter(df, home_team, away_team, n_games, venue, head_to_head, team)
    if len(temp_df) < n_games:
        return "NaN"
    if team == "home":
        loses = ((temp_df.HomeTeam == home_team) & (temp_df.FTR == "A")) | \
               ((temp_df.AwayTeam == home_team) & (temp_df.FTR == "H"))
    else:
        loses = ((temp_df.HomeTeam == away_team) & (temp_df.FTR == "A")) | \
                ((temp_df.AwayTeam == away_team) & (temp_df.FTR == "H"))
    if n_games != 1:
        output = round(loses.sum() / n_games, 2)
    else:
        output = loses.sum()
    return output

def goals_scored(df, home_team, away_team, n_games, venue, head_to_head, team):
    """Returns the goals scored by team from last n games."""

    temp_df = match_filter(df, home_team, away_team, n_games, venue, head_to_head, team)
    if len(temp_df) < n_games:
        return "NaN"
    if team == "home":
        scored = temp_df[temp_df.HomeTeam == home_team]["FTHG"].sum() + \
                 temp_df[temp_df.AwayTeam == home_team]["FTAG"].sum()
    else:
        scored = temp_df[temp_df.HomeTeam == away_team]["FTHG"].sum() + \
                 temp_df[temp_df.AwayTeam == away_team]["FTAG"].sum()
    return scored

def goals_conceded(df, home_team, away_team, n_games, venue, head_to_head, team):
    """Returns the goals conceded by team from last n games."""

    temp_df = match_filter(df, home_team, away_team, n_games, venue, head_to_head, team)
    if len(temp_df) < n_games:
        return "NaN"
    if team == "home":
        conceded = temp_df[temp_df.HomeTeam == home_team]["FTAG"].sum() +\
                   temp_df[temp_df.AwayTeam == home_team]["FTHG"].sum()
    else:
        conceded = temp_df[temp_df.HomeTeam == away_team]["FTAG"].sum() + \
                   temp_df[temp_df.AwayTeam == away_team]["FTHG"].sum()
    return conceded

## Main measure function
def measures_main(idx, df):
    """Return list of form based measures using individual helper functions."""

    date, home_team, away_team = df.loc[idx, ["Date", "HomeTeam", "AwayTeam"]]

    row_filter = df.Date < date
    row_filter = row_filter & ((df.HomeTeam.isin([home_team, away_team])) |
                               df.AwayTeam.isin([home_team, away_team]))

    temp_df = df[row_filter]
    
    # win/lose percent measures
    home_team_win_percent_last_5 = team_win_percentage(temp_df, home_team, away_team, 5, "both", False, "home")
    home_team_win_percent_last_10 = team_win_percentage(temp_df, home_team, away_team, 10, "both", False, "home")
    home_team_win_percent_last_15 = team_win_percentage(temp_df, home_team, away_team, 15, "both", False, "home")
    away_team_win_percent_last_5 = team_win_percentage(temp_df, home_team, away_team, 5, "both", False, "away")
    away_team_win_percent_last_10 = team_win_percentage(temp_df, home_team, away_team, 10, "both", False, "away")
    away_team_win_percent_last_15 = team_win_percentage(temp_df, home_team, away_team, 15, "both", False, "away")
    home_team_lose_percent_last_5 = team_lose_percentage(temp_df, home_team, away_team, 5, "both", False, "home")
    home_team_lose_percent_last_10 = team_lose_percentage(temp_df, home_team, away_team, 10, "both", False, "home")
    home_team_lose_percent_last_15 = team_lose_percentage(temp_df, home_team, away_team, 15, "both", False, "home")
    away_team_lose_percent_last_5 = team_lose_percentage(temp_df, home_team, away_team, 5, "both", False, "away")
    away_team_lose_percent_last_10 = team_lose_percentage(temp_df, home_team, away_team, 10, "both", False, "away")
    away_team_lose_percent_last_15 = team_lose_percentage(temp_df, home_team, away_team, 15, "both", False, "away")
    
    # goals scored/conceded measures
    home_team_goals_scored_last_5 = goals_scored(temp_df, home_team, away_team, 5, "both", False, "home")
    home_team_goals_scored_last_10 = goals_scored(temp_df, home_team, away_team, 10, "both", False, "home")
    home_team_goals_scored_last_15 = goals_scored(temp_df, home_team, away_team, 15, "both", False, "home")
    away_team_goals_scored_last_5 = goals_scored(temp_df, home_team, away_team, 5, "both", False, "away")
    away_team_goals_scored_last_10 = goals_scored(temp_df, home_team, away_team, 10, "both", False, "away")
    away_team_goals_scored_last_15 = goals_scored(temp_df, home_team, away_team, 15, "both", False, "away")
    home_team_goals_conceded_last_5 = goals_conceded(temp_df, home_team, away_team, 5, "both", False, "home")
    home_team_goals_conceded_last_10 = goals_conceded(temp_df, home_team, away_team, 10, "both", False, "home")
    home_team_goals_conceded_last_15 = goals_conceded(temp_df, home_team, away_team, 15, "both", False, "home")
    away_team_goals_conceded_last_5 = goals_conceded(temp_df, home_team, away_team, 5, "both", False, "away")
    away_team_goals_conceded_last_10 = goals_conceded(temp_df, home_team, away_team, 10, "both", False, "away")
    away_team_goals_conceded_last_15 = goals_conceded(temp_df, home_team, away_team, 15, "both", False, "away")

    # last game measures
    home_team_win_percent_last_game = team_win_percentage(temp_df, home_team, away_team, 1, "both", False, "home")
    away_team_win_percent_last_game = team_win_percentage(temp_df, home_team, away_team, 1, "both", False, "away")
    home_team_lose_percent_last_game = team_lose_percentage(temp_df, home_team, away_team, 1, "both", False, "home")
    away_team_lose_percent_last_game = team_lose_percentage(temp_df, home_team, away_team, 1, "both", False, "away")
    home_team_goals_scored_last_game = goals_scored(temp_df, home_team, away_team, 1, "both", False, "home")
    away_team_goals_scored_last_game = goals_scored(temp_df, home_team, away_team, 1, "both", False, "away")
    home_team_goals_conceded_last_game = goals_conceded(temp_df, home_team, away_team, 1, "both", False, "home")
    away_team_goals_conceded_last_game = goals_conceded(temp_df, home_team, away_team, 1, "both", False, "away")
    
    # venue specific measures
    home_team_win_percent_venue_last_5 = team_win_percentage(temp_df, home_team, away_team, 5, "home", False, "home")
    home_team_win_percent_venue_last_10 = team_win_percentage(temp_df, home_team, away_team, 10, "home", False, "home")
    home_team_win_percent_venue_last_15 = team_win_percentage(temp_df, home_team, away_team, 15, "home", False, "home")
    away_team_win_percent_venue_last_5 = team_win_percentage(temp_df, home_team, away_team, 5, "away", False, "away")
    away_team_win_percent_venue_last_10 = team_win_percentage(temp_df, home_team, away_team, 10, "away", False, "away")
    away_team_win_percent_venue_last_15 = team_win_percentage(temp_df, home_team, away_team, 15, "away", False, "away")
    home_team_lose_percent_venue_last_5 = team_lose_percentage(temp_df, home_team, away_team, 5, "home", False, "home")
    home_team_lose_percent_venue_last_10 = team_lose_percentage(temp_df, home_team, away_team, 10, "home", False, "home")
    home_team_lose_percent_venue_last_15 = team_lose_percentage(temp_df, home_team, away_team, 15, "home", False, "home")
    away_team_lose_percent_venue_last_5 = team_lose_percentage(temp_df, home_team, away_team, 5, "away", False, "away")
    away_team_lose_percent_venue_last_10 = team_lose_percentage(temp_df, home_team, away_team, 10, "away", False, "away")
    away_team_lose_percent_venue_last_15 = team_lose_percentage(temp_df, home_team, away_team, 15, "away", False, "away")
    home_team_goals_scored_venue_last_5 = goals_scored(temp_df, home_team, away_team, 5, "home", False, "home")
    home_team_goals_scored_venue_last_10 = goals_scored(temp_df, home_team, away_team, 10, "home", False, "home")
    home_team_goals_scored_venue_last_15 = goals_scored(temp_df, home_team, away_team, 15, "home", False, "home")
    away_team_goals_scored_venue_last_5 = goals_scored(temp_df, home_team, away_team, 5, "away", False, "away")
    away_team_goals_scored_venue_last_10 = goals_scored(temp_df, home_team, away_team, 10, "away", False, "away")
    away_team_goals_scored_venue_last_15 = goals_scored(temp_df, home_team, away_team, 15, "away", False, "away")
    home_team_goals_conceded_venue_last_5 = goals_conceded(temp_df, home_team, away_team, 5, "home", False, "home")
    home_team_goals_conceded_venue_last_10 = goals_conceded(temp_df, home_team, away_team, 10, "home", False, "home")
    home_team_goals_conceded_venue_last_15 = goals_conceded(temp_df, home_team, away_team, 15, "home", False, "home")
    away_team_goals_conceded_venue_last_5 = goals_conceded(temp_df, home_team, away_team, 5, "away", False, "away")
    away_team_goals_conceded_venue_last_10 = goals_conceded(temp_df, home_team, away_team, 10, "away", False, "away")
    away_team_goals_conceded_venue_last_15 = goals_conceded(temp_df, home_team, away_team, 15, "away", False, "away")
    
    # head-to-head measures
    hth_home_win_percent_last_5 = team_win_percentage(temp_df, home_team, away_team, 5, "both", True, "home")
    hth_home_win_percent_last_10 = team_win_percentage(temp_df, home_team, away_team, 10, "both", True, "home")
    hth_home_win_percent_last_15 = team_win_percentage(temp_df, home_team, away_team, 15, "both", True, "home")
    hth_home_lose_percent_last_5 = team_lose_percentage(temp_df, home_team, away_team, 5, "both", True, "home")
    hth_home_lose_percent_last_10 = team_lose_percentage(temp_df, home_team, away_team, 10, "both", True, "home")
    hth_home_lose_percent_last_15 = team_lose_percentage(temp_df, home_team, away_team, 15, "both", True, "home")
    hth_home_goals_scored_last_5 = goals_scored(temp_df, home_team, away_team, 5, "home", True, "home")
    hth_home_goals_scored_last_10 = goals_scored(temp_df, home_team, away_team, 10, "both", True, "home")
    hth_home_goals_scored_last_15 = goals_scored(temp_df, home_team, away_team, 15, "both", True, "home")
    hth_home_goals_conceded_last_5 = goals_conceded(temp_df, home_team, away_team, 5, "both", True, "home")
    hth_home_goals_conceded_last_10 = goals_conceded(temp_df, home_team, away_team, 10, "both", True, "home")
    hth_home_goals_conceded_last_15 = goals_conceded(temp_df, home_team, away_team, 15, "both", True, "home")
    
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
                   away_team_lose_percent_last_15,
                   home_team_goals_scored_last_5,
                   home_team_goals_scored_last_10,
                   home_team_goals_scored_last_15,
                   away_team_goals_scored_last_5,
                   away_team_goals_scored_last_10,
                   away_team_goals_scored_last_15,
                   home_team_goals_conceded_last_5,
                   home_team_goals_conceded_last_10,
                   home_team_goals_conceded_last_15,
                   away_team_goals_conceded_last_5,
                   away_team_goals_conceded_last_10,
                   away_team_goals_conceded_last_15,
                   home_team_win_percent_last_game,
                   away_team_win_percent_last_game,
                   home_team_lose_percent_last_game,
                   away_team_lose_percent_last_game,
                   home_team_goals_scored_last_game,
                   away_team_goals_scored_last_game,
                   home_team_goals_conceded_last_game,
                   away_team_goals_conceded_last_game,
                   home_team_win_percent_venue_last_5,
                   home_team_win_percent_venue_last_10,
                   home_team_win_percent_venue_last_15,
                   away_team_win_percent_venue_last_5,
                   away_team_win_percent_venue_last_10,
                   away_team_win_percent_venue_last_15,
                   home_team_lose_percent_venue_last_5,
                   home_team_lose_percent_venue_last_10,
                   home_team_lose_percent_venue_last_15,
                   away_team_lose_percent_venue_last_5,
                   away_team_lose_percent_venue_last_10,
                   away_team_lose_percent_venue_last_15,
                   home_team_goals_scored_venue_last_5,
                   home_team_goals_scored_venue_last_10,
                   home_team_goals_scored_venue_last_15,
                   away_team_goals_scored_venue_last_5,
                   away_team_goals_scored_venue_last_10,
                   away_team_goals_scored_venue_last_15,
                   home_team_goals_conceded_venue_last_5,
                   home_team_goals_conceded_venue_last_10,
                   home_team_goals_conceded_venue_last_15,
                   away_team_goals_conceded_venue_last_5,
                   away_team_goals_conceded_venue_last_10,
                   away_team_goals_conceded_venue_last_15,
                   hth_home_win_percent_last_5,
                   hth_home_win_percent_last_10,
                   hth_home_win_percent_last_15,
                   hth_home_lose_percent_last_5,
                   hth_home_lose_percent_last_10,
                   hth_home_lose_percent_last_15,
                   hth_home_goals_scored_last_5,
                   hth_home_goals_scored_last_10,
                   hth_home_goals_scored_last_15,
                   hth_home_goals_conceded_last_5,
                   hth_home_goals_conceded_last_10,
                   hth_home_goals_conceded_last_15]

    return output_list

def main():
    measures = get_measures()

    raw_data = pd.read_csv("../data/processed/historical_scores.csv", index_col=0)
    raw_data = raw_data[match_info + match_statistics]
    raw_data.Date = pd.to_datetime(raw_data.Date)
    raw_data = raw_data.reset_index()

    measures_list = ["home_team_win_percent_last_5",
                   "home_team_win_percent_last_10",
                   "home_team_win_percent_last_15",
                   "away_team_win_percent_last_5",
                   "away_team_win_percent_last_10",
                   "away_team_win_percent_last_15",
                   "home_team_lose_percent_last_5",
                   "home_team_lose_percent_last_10",
                   "home_team_lose_percent_last_15",
                   "away_team_lose_percent_last_5",
                   "away_team_lose_percent_last_10",
                   "away_team_lose_percent_last_15",
                   "home_team_goals_scored_last_5",
                   "home_team_goals_scored_last_10",
                   "home_team_goals_scored_last_15",
                   "away_team_goals_scored_last_5",
                   "away_team_goals_scored_last_10",
                   "away_team_goals_scored_last_15",
                   "home_team_goals_conceded_last_5",
                   "home_team_goals_conceded_last_10",
                   "home_team_goals_conceded_last_15",
                   "away_team_goals_conceded_last_5",
                   "away_team_goals_conceded_last_10",
                   "away_team_goals_conceded_last_15",
                   "home_team_win_percent_last_game",
                   "away_team_win_percent_last_game",
                   "home_team_lose_percent_last_game",
                   "away_team_lose_percent_last_game",
                   "home_team_goals_scored_last_game",
                   "away_team_goals_scored_last_game",
                   "home_team_goals_conceded_last_game",
                   "away_team_goals_conceded_last_game",
                   "home_team_win_percent_venue_last_5",
                   "home_team_win_percent_venue_last_10",
                   "home_team_win_percent_venue_last_15",
                   "away_team_win_percent_venue_last_5",
                   "away_team_win_percent_venue_last_10",
                   "away_team_win_percent_venue_last_15",
                   "home_team_lose_percent_venue_last_5",
                   "home_team_lose_percent_venue_last_10",
                   "home_team_lose_percent_venue_last_15",
                   "away_team_lose_percent_venue_last_5",
                   "away_team_lose_percent_venue_last_10",
                   "away_team_lose_percent_venue_last_15",
                   "home_team_goals_scored_venue_last_5",
                   "home_team_goals_scored_venue_last_10",
                   "home_team_goals_scored_venue_last_15",
                   "away_team_goals_scored_venue_last_5",
                   "away_team_goals_scored_venue_last_10",
                   "away_team_goals_scored_venue_last_15",
                   "home_team_goals_conceded_venue_last_5",
                   "home_team_goals_conceded_venue_last_10",
                   "home_team_goals_conceded_venue_last_15",
                   "away_team_goals_conceded_venue_last_5",
                   "away_team_goals_conceded_venue_last_10",
                   "away_team_goals_conceded_venue_last_15",
                   "hth_home_win_percent_last_5",
                   "hth_home_win_percent_last_10",
                   "hth_home_win_percent_last_15",
                   "hth_home_lose_percent_last_5",
                   "hth_home_lose_percent_last_10",
                   "hth_home_lose_percent_last_15",
                   "hth_home_goals_scored_last_5",
                   "hth_home_goals_scored_last_10",
                   "hth_home_goals_scored_last_15",
                   "hth_home_goals_conceded_last_5",
                   "hth_home_goals_conceded_last_10",
                   "hth_home_goals_conceded_last_15"]

    measures = pd.concat([measures, pd.DataFrame(columns=measures_list)])
    max_index = max(measures.index)
    percent_complete = 1
    for index in measures.index:
        measures.loc[index, measures_list] = measures_main(index, raw_data)
        if 100 * index / max_index > percent_complete:
            print("%s%%" % percent_complete)
            percent_complete += 1
    measures.to_csv("../data/processed/complete_measures.csv")

if __name__ == "__main__":
    main()
