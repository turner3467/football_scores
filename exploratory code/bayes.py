import numpy as np
import pymc3 as pm
import theano.tensor as T

from pymc3.distributions.dist_math import bound, factln, logpow

# Vector model
# Vectors to describe matches
home_team = np.array([[0], [0], [1], [1]])
away_team = np.array([[1], [1], [0], [0]])
scores = np.array([[5, 0], [5, 0], [0, 5], [0, 5]])
time = np.array([[0], [1], [2], [3]])


class JointScore(pm.Discrete):
    def __init__(self, mu_x, mu_y, *args, **kwargs):
        super(JointScore, self).__init__(*args, **kwargs)
        self.mu_x = mu_x
        self.mu_y = mu_y

    def logp(self, value):
        value_x = value[0][0]
        value_y = value[1][1]
        mu_x = self.mu_x
        mu_y = self.mu_y

        log_prob_x = bound(
            logpow(mu_x, value_x) - factln(value_x) - mu_x,
            mu_x >= 0, value_x >= 0)
        log_prob_y = bound(
            logpow(mu_y, value_y) - factln(value_y) - mu_y,
            mu_y >= 0, value_y >= 0)
        return T.switch(1 * T.eq(mu_x, 0) * T.eq(value_x, 0) *
                        T.eq(mu_y, 0) * T.eq(value_y, 0),
                        0, log_prob_x + log_prob_y)


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

    atts = att_prop - T.mean(att_prop)
    defs = def_prop - T.mean(def_prop)

    lambda_home = T.exp(1 + atts[home_team] - defs[away_team])
    lambda_away = T.exp(0.8 + atts[away_team] - defs[home_team])

    score = JointScore("score",
                       mu_x=lambda_home,
                       mu_y=lambda_away,
                       observed=scores)


dynamic_model = pm.Model()

with dynamic_model:
    # Team priors
    att_prop = pm.Normal("att_prop",
                         mu=0,
                         sd=0.2,
                         shape=(4, 2))
    def_prop = pm.Normal("def_prop",
                         mu=0,
                         sd=0.2,
                         shape=(4, 2))

    atts = att_prop - T.mean(att_prop)
    defs = def_prop - T.mean(def_prop)

    lambda_home = T.exp(1 + atts[time, home_team] - defs[time, away_team])
    lambda_away = T.exp(0.8 + atts[time, away_team] - defs[time, home_team])

    score = JointScore("score",
                       mu_x=lambda_home,
                       mu_y=lambda_away,
                       observed=scores)

with dynamic_model:
    start = pm.find_MAP()
    step = pm.NUTS()
    trace = pm.sample(2000, step, start=start)

    a = pm.traceplot(trace)
