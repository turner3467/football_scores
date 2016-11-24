import numpy as np
import pymc3 as pm
import theano.tensor as T

from pymc3.distributions.dist_math import bound, factln, logpow


def plt():
    import matplotlib.pyplot as p
    p.show()

# Vector model
# Vectors to describe matches
home_team = np.array([[0], [0], [1], [1]])
away_team = np.array([[1], [1], [0], [0]])

home_goals = np.array([[5], [5], [0], [0]])
away_goals = np.array([[0], [0], [5], [5]])

scores = np.array([[5, 0], [5, 0], [0, 5], [0, 5]])
time = np.array([[0], [1], [2], [3]])


class JointScore(pm.Discrete):
    def __init__(self, mu_x, mu_y, *args, **kwargs):
        super(JointScore, self).__init__(*args, **kwargs)
        self.mu_x = mu_x
        self.mu_y = mu_y

    def logp(self, value):
        value_x = value[0][0]
        value_y = value[0][1]
        mu_x = self.mu_x
        mu_y = self.mu_y

        log_prob_x = bound(
            logpow(mu_x, value_x) - factln(value_x) - mu_x,
            mu_x >= 0, value_x >= 0)
        log_prob_y = bound(
            logpow(mu_y, value_y) - factln(value_y) - mu_y,
            mu_y >= 0, value_y >= 0)
        out = T.switch(1 * T.eq(mu_x, 0) * T.eq(value_x, 0), 0, log_prob_x)
        out += T.switch(1 * T.eq(mu_x, 0) * T.eq(value_x, 0), 0, log_prob_y)
        return out

basic_model = pm.Model()

with basic_model:
    # Team priors
    att_prop = pm.Normal("att_pror",
                         mu=0,
                         sd=0.2,
                         shape=2)
    def_prop = pm.Normal("def_prop",
                         mu=0,
                         sd=0.2,
                         shape=2)

    atts = pm.Deterministic("atts", att_prop - T.mean(att_prop))
    defs = pm.Deterministic("defs", def_prop - T.mean(def_prop))

    lambda_home = T.exp(1 + atts[home_team] - defs[away_team])
    lambda_away = T.exp(0.8 + atts[away_team] - defs[home_team])

    # score = JointScore("score", mu_x=lambda_home, mu_y=lambda_away, observed=scores)
    home_score = pm.Poisson("home_score", mu=lambda_home, observed=home_goals)
    away_score = pm.Poisson("away_score", mu=lambda_away, observed=away_goals)

with basic_model:
    start = pm.find_MAP()
    step = pm.NUTS()
    trace = pm.sample(2000, step, start=start)

    a = pm.traceplot(trace)
