import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np

complete_measures = pd.read_csv("../data/processed/complete_measures.csv", index_col=[0])

processed_measures = complete_measures.drop(["AwayTeam", "Date", "HomeTeam", "Season"], axis=1)

enc = OneHotEncoder()
enc.fit(processed_measures.scores)

