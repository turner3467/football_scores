from bs4 import BeautifulSoup
import urllib.request as ur
import csv
import os

URL = "http://www.statto.com/football/stats/england/premier-league/2014-2015/table/2015-02-11"
headers = {'User-Agent' : 'Mozilla/5.0'}
measures_path = r"C:\Users\jeremy.turner\Documents\Personal\football_scores\data\processed\complete_measures.csv"
output_folder = r"C:\Users\jeremy.turner\Documents\Personal\football_scores\data\historical leagues"

col_names = ["position",
             "team",
             "played",
             "full_won",
             "full_draw",
             "full_lost",
             "full_for",
             "full_against",
             "home_won",
             "home_draw",
             "home_lost",
             "home_for",
             "home_against",
             "away_won",
             "away_draw",
             "away_lost",
             "away_for",
             "away_against",
             "goal_diff",
             "points"]

pre_league_dict = {"1": "premier-league",
                   "2": "division-one",
                   "3": "division-two",
                   "4": "division-three"}
post_league_dict = {"1": "premier-league",
                   "2": "league-championship",
                   "3": "league-one",
                   "4": "league-two"}


def get_league_info():
    with open(measures_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        league_info_set = set()
        for row in reader:
            league_info_set.add((row[5].zfill(4), row[4], row[2]))
        return league_info_set


def get_league(url):
    req = ur.Request(url, None, headers)
    html = ur.urlopen(req).read()
    soup = BeautifulSoup(html, "lxml")
    html_table = soup.find("table", "table league-table lightbox")

    league = []
    for row in html_table.find_all("tr")[2:]:
        league_row = list(filter(None,
                                 [td.get_text() for td in row.find_all("td")][0:23]))
        league.append(league_row)

    return league


def write_league(league):
    with open("test.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(col_names)
        for row in league:
            writer.writerow(row)
    return 0

def create_url(league_info):
    season = league_info[0]
    division = league_info[1]
    date = league_info[2]

    season = [season[:2], season[-2:]]
    season = list(map(lambda x: "19"+x if int(x) > 50 else "20"+x, season))

    if int(season[0]) <= 2003:
        division = pre_league_dict[division]
    else:
        division = post_league_dict[division]

    url = "http://www.statto.com/football/stats/england/{}/{}/table/{}"\
        .format(division, "-".join(season), date)
    return url
