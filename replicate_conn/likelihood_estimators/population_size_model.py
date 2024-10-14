import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import argparse
R0, eta1_tilde, eta2_tilde, eta3_tilde, nu11_tilde, nu12_tilde, nu21_tilde, nu22_tilde
parser = argparse.ArgumentParser()
parser.add_argument("--R0", type = float, help = "R0")
parser.add_argument("--eta1_tilde", type = float)
parser.add_argument("--eta2_tilde", type = float)
parser.add_argument("--eta3_tilde", type = float)
parser.add_argument("--nu11_tilde", type = float)
parser.add_argument("--nu12_tilde", type = float)
parser.add_argument("--nu21_tilde", type = float)
parser.add_argument("--nu22_tilde", type = float)

args = parser.parse_args()

R0 = args.R0
eta1_tilde = args.eta1_tilde
eta2_tilde = args.eta2_tilde
eta3_tilde = args.eta3_tilde
nu11_tilde = args.nu11_tilde
nu12_tilde = args.nu12_tilde
nu21_tilde = args.nu21_tilde
nu22_tilde = args.nu22_tilde

# Survival, fecundity, and population size
def S(a, eta1_tilde, eta2_tilde, eta3_tilde, c):
    """
    Survival function
    """
    S = np.exp(-c*((eta1_tilde*a)**eta2_tilde + (eta1_tilde*a)**(1/eta2_tilde) + eta3_tilde - (eta1_tilde*(a-1))**eta2_tilde - (eta1_tilde*(a-1))**(1/eta2_tilde)))
    #S = np.exp(-c*((eta1_tilde*a)**eta2_tilde + (eta1_tilde*a)**(1/eta2_tilde) + eta3_tilde*a))
    return(S)
def f(a, nug1_tilde, nug2_tilde):
    """
    Fecundity function
    """
    return((1 + np.exp(-nug1_tilde*(a - nug2_tilde)))**(-1))
def N(params, max_a, max_t, c):
    """
    Number of males and females of ages 1, ..., max_a at years 1, ..., max_t
    """
    R0, eta1_tilde, eta2_tilde, eta3_tilde, nu11_tilde, nu12_tilde, nu21_tilde, nu22_tilde = params
    N_males = np.zeros((max_a + 1, max_t + 1))
    N_females = np.zeros((max_a + 1, max_t + 1))
    ages = np.arange(max_a + 1)
    years = np.arange(max_t + 1)
    # Set all time 0 population sizes to NA because time starts at 1
    N_males[:, 0] = None
    N_females[:, 0] = None
    # Set all age 0 population sizes to NA because age starts at 1
    N_males[0,:] = None
    N_females[0,:] = None
    # Initialize the population at time 1
    N_males[1, 1] = np.exp(R0)
    N_females[1, 1] = np.exp(R0)
    # For ages 2 to max_a, initialize as a stable age distribution
    for a in ages[2:]:
        S_amin1 = S(a - 1, eta1_tilde, eta2_tilde, eta3_tilde, c)
        N_males[a, 1] = N_males[a - 1, 1] * S_amin1
        N_females[a, 1] = N_females[a - 1, 1] * S_amin1
        #print("age: ", a, "time: 1", "Ns: ", N_males[a, 1], "   ", N_females[a, 1])
    for t in years[2:]:
        # Survival model
        for a in ages[2:]:
            S_amin1 = S(a - 1, eta1_tilde, eta2_tilde, eta3_tilde, c)
            N_males[a, t] = N_males[a - 1, t - 1] * S_amin1
            N_females[a, t] = N_females[a - 1, t - 1] * S_amin1
            #print("age: ", a, "time: ", t, "Ns: ", N_males[a, 1], "   ", N_females[a, 1])
        #print("age: ", 1, "time: ", t, "Ns: ", N_males[a, 1], "   ", N_females[a, 1])
        # Fecundity model
        n_new_offspring = np.sum([f(a, nu11_tilde, nu12_tilde) * N_females[a, t] for a in ages[2:,]])
        #print(n_new_offspring)
        N_males[1, t] = 0.5 * n_new_offspring
        N_females[1, t] = 0.5 * n_new_offspring
    return N_females, N_males

