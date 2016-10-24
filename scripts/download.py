#! /usr/bin/env python

import csv
import urllib.request as req
import io

base_url = "http://football-data.co.uk/mmz4281/"  # 1516/E0.csv

seasons = [str(i % 100).zfill(2) + str((i + 1) % 100).zfill(2)
           for i in range(100, 116)]
leagues = [1, 2]
cntry = {"eng": "E",
         "ger": "D",
         "fra": "F",
         "spa": "SP",
         "ita": "I"}

for s in seasons:
        for l in leagues:
                for c in cntry:
                        if c == 'eng':  # premiership = 0
                                l_tmp = l - 1
                        else:
                                l_tmp = l
                        url = base_url + "{}/{}{}.csv".format(s, cntry[c], l_tmp)
                        r = req.urlopen(url)
                        reader = csv.reader(io.TextIOWrapper(r, errors="ignore"))
                        file = "../data/raw_data/{}_{}_{}.csv".format(c, s, str(l))
                        with open(file, "w") as outfile:
                                writer = csv.writer(outfile, delimiter=",")
                                for row in reader:
                                        writer.writerow(row)

print("Historic seasons downloaded successfully.")
