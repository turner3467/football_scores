import numpy as np
import pymc3 as pm
import matplotlib

# Initialize team properties
mu_a_A, sigma_a_A = 1, 0.2
mu_d_A, sigma_d_A = 1, 0.2
mu_a_B, sigma_a_B = 1, 0.2
mu_d_B, sigma_d_B = 1, 0.2

# Create game observation
home_goals = np.array([[10], [10]])
away_goals = np.array([[1], [0]])

basic_model = pm.Model()

with basic_model:
    att_A = pm.Normal("att_A", mu=mu_a_A, sd=sigma_a_A)
    def_A = pm.Normal("def_A", mu=mu_d_A, sd=sigma_d_A)
    att_B = pm.Normal("att_B", mu=mu_a_B, sd=sigma_a_B)
    def_B = pm.Normal("def_B", mu=mu_d_B, sd=sigma_d_B)

    lambda_x = 1.2 + att_A - def_B
    lambda_y = 0.8 + att_B - def_A

    home_score = pm.Poisson("home_score", mu=lambda_x, observed=home_goals)
    away_score = pm.Poisson("away_score", mu=lambda_x, observed=away_goals)

with basic_model:
    start = pm.find_MAP()
    step = pm.NUTS()
    trace = pm.sample(2000, step, start=start)

    a = pm.traceplot(trace)
