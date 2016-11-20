import numpy as np
import pymc3 as pm
import theano.tensor as T

from pymc3.distributions.dist_math import bound, factln, logpow

# Initialize team properties
mu_a_A, sigma_a_A = 0.2, 1
mu_d_A, sigma_d_A = 0.2, 1
mu_a_B, sigma_a_B = 0.2, 1
mu_d_B, sigma_d_B = 0.2, 1

# For joint prob dist
scores = np.array([[2, 1], [3, 1], [3, 1]])


class JointScore(pm.Discrete):
    def __init__(self, mu_x, mu_y, *args, **kwargs):
        super(JointScore, self).__init__(*args, **kwargs)
        self.mu_x = mu_x
        self.mu_y = mu_y

    def logp(self, value):
        value_x = value[0]
        value_y = value[1]
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
    att_A = pm.Normal("att_A", mu=mu_a_A, sd=sigma_a_A)
    def_A = pm.Normal("def_A", mu=mu_d_A, sd=sigma_d_A)
    att_B = pm.Normal("att_B", mu=mu_a_B, sd=sigma_a_B)
    def_B = pm.Normal("def_B", mu=mu_d_B, sd=sigma_d_B)

    lambda_x = 2.3 + att_A - def_B
    lambda_y = 1.4 + att_B - def_A

    score = JointScore("score", mu_x=lambda_x, mu_y=lambda_y, observed=scores)


with basic_model:
    start = pm.find_MAP()
    step = pm.NUTS()
    trace = pm.sample(2000, step, start=start)

    a = pm.traceplot(trace)
