import pandas as pd

measures_path = "../data/processed/complete_measures.csv"
complete_measures = pd.read_csv(measures_path, index_col=[0])
