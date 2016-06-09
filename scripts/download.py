#! /usr/bin/env python

import csv
import urllib.request as req
import io

base_url = "http://football-data.co.uk/mmz4281/" #1516/E0.csv

seasons = [str(i % 100).zfill(2) + str((i + 1) % 100).zfill(2) for i in range(93,116)]
leagues = {1: "E0", 2: "E1", 3: "E2", 4: "E3"}

for season in seasons:
	for league in leagues:
		url = base_url + "{}/{}.csv".format(season, leagues[league])
		r = req.urlopen(url)
		reader = csv.reader(io.TextIOWrapper(r, errors="ignore"))
		with open("../data/{}_{}.csv".format(season, str(league)), "w") as outfile:
			writer = csv.writer(outfile, delimiter=",")
			for row in reader:
				writer.writerow(row)

print("Historic seasons downloaded successfully.")
