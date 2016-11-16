import numpy as np
from pymc3 import Model, Poisson

# Initialize team properties
att_A, sigma_a_A = 1, 0.2
def_A, sigma_d_A = 1, 0.2
att_B, sigma_a_B = 1, 0.2
def_B, sigma_d_B = 1, 0.2

# Create game observation
data = np.array([[5, 1]])

basic_model = Model()

with basic_model:
    att_A = Poisson("att_A", mu=sigma_a_A)
    def_A = Poisson("def_A", mu=sigma_d_A)
    att_B = Poisson("att_B", mu=sigma_a_B)
    def_B = Poisson("def_B", mu=sigma_d_B)

    lambda_x = att_A - def_B
    lambda_y = att_B - def_A
