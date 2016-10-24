#! /usr/bin/env python

import pandas as pd

match_info = ['Country',
              'Season',
              'League',
              'Date',
              'HomeTeam',
              'AwayTeam',
              'FTR']

match_statistics = ['FTHG',
                    'FTAG',
                    'HTHG',
                    'HTAG',
                    'HTR',
                    'Attendance',
                    'Referee',
                    'HS',
                    'AS',
                    'HST',
                    'AST',
                    'HHW',
                    'AHW',
                    'HC',
                    'AC',
                    'HF',
                    'AF',
                    'HO',
                    'AO',
                    'HY',
                    'AY',
                    'HR',
                    'AR',
                    'HBP',
                    'ABP']

measures_list = ['ht_home_form',
                 'ht_form',
                 'ht_goals_for',
                 'ht_goals_agnst',
                 'at_away_form',
                 'at_form',
                 'at_goals_for',
                 'at_goals_agnst']

N_GAMES = 10


# Helper functions
def first_N_games(bool_vector, n):
    output_vector = bool_vector
    count = 0
    for idx, i in enumerate(output_vector):
        if count >= n:
            output_vector[idx] = False
        if i:
            count += 1

    return output_vector


def get_raw_data():
    tmp_df = pd.read_csv('../data/main_data.csv',
                         usecols=match_info + match_statistics)
    tmp_df['Date'] = pd.to_datetime(tmp_df['Date'])

    return tmp_df


def get_measures(df, measures_list):
    tmp_df = df[match_info]
    tmp_df = pd.concat([tmp_df, pd.DataFrame(columns=measures_list)])

    return tmp_df


def create_measures(idx, df):

    date, home_team, away_team = df.loc[idx, ['Date', 'HomeTeam', 'AwayTeam']]

    date_filter = df.Date < date
    home_filter = (df.HomeTeam == home_team) | (df.AwayTeam == home_team)
    away_filter = (df.HomeTeam == away_team) | (df.AwayTeam == away_team)

    home_filter = date_filter & home_filter
    away_filter = date_filter & away_filter

    home_filter = first_N_games(home_filter, N_GAMES)
    away_filter = first_N_games(away_filter, N_GAMES)

    row_filter = (home_filter | away_filter)
    tmp_df = df[row_filter]

    home_dict = {'H': 1, 'D': 0, 'A': -1}
    away_dict = {'H': -1, 'D': 0, 'A': 1}

    # Home team home form
    results = tmp_df[tmp_df.HomeTeam == home_team]['FTR']
    ht_home_form = sum([home_dict[r] for r in results])

    # Away team away form
    results = tmp_df[tmp_df.AwayTeam == away_team]['FTR']
    at_away_form = sum([away_dict[r] for r in results])

    # Home team form
    results = tmp_df[tmp_df.AwayTeam == home_team]['FTR']
    ht_form = ht_home_form + sum([away_dict[r] for r in results])

    # Away team form
    results = tmp_df[tmp_df.HomeTeam == away_team]['FTR']
    at_form = at_away_form + sum([home_dict[r] for r in results])

    # TODO: create goals for and against measures
    goals = tmp_df[tmp_df.HomeTeam == home_team]['FTHG'].sum()
    goals += tmp_df[tmp_df.AwayTeam == home_team]['FTAG'].sum()
    ht_goals_for = goals

    goals = tmp_df[tmp_df.HomeTeam == home_team]['FTAG'].sum()
    goals += tmp_df[tmp_df.AwayTeam == home_team]['FTHG'].sum()
    ht_goals_agnst = goals

    goals = tmp_df[tmp_df.HomeTeam == away_team]['FTHG'].sum()
    goals += tmp_df[tmp_df.AwayTeam == away_team]['FTAG'].sum()
    at_goals_for = goals

    goals = tmp_df[tmp_df.HomeTeam == away_team]['FTAG'].sum()
    goals += tmp_df[tmp_df.AwayTeam == away_team]['FTHG'].sum()
    at_goals_agnst = goals

    output_list = [ht_home_form,
                   ht_form,
                   ht_goals_for,
                   ht_goals_agnst,
                   at_away_form,
                   at_form,
                   at_goals_for,
                   at_goals_agnst]

    return output_list


def main():

    raw_data = get_raw_data()
    measures = get_measures(raw_data, measures_list)

    max_index = max(measures.index)
    percent_complete = 1
    for index in measures.index:
        measures.loc[index, measures_list] = create_measures(index, raw_data)

        if 100 * index / max_index > percent_complete:
            print('%s%%' % percent_complete)
            percent_complete += 1
    measures.to_csv('../data/measures.csv', encoding='utf_8')

if __name__ == '__main__':
    main()
