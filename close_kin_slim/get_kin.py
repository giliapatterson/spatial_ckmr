import msprime, pyslim
import tskit
import json
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import itertools
import math
import sys

rng = np.random.default_rng()

# Get the tree sequence file path and output file path from the command line
ts_path = sys.argv[1]
outfile = sys.argv[2]
outN = sys.argv[3]

slim_ts = tskit.load(ts_path)

def get_kin(tree_seq, pairs):
    '''
    tree_seq: tree sequence with all individuals remembered
    pairs: individuals to compare [ind1, ind2]
    Returns a numpy array, each row is a pair, columns are: self (0 or 1), half-sib (0 or 1), full-sib (0 or 1),
    x-coordinate, y-coordinate, x-coordinate, y-coordinate
    '''
    pairs = list(pairs)
    npairs = len(pairs)
    input_matrix = np.zeros([npairs, 6])                                   
    i = 0
    for pair in pairs:
        ind0 = slim_ts.individual(pair[0])
        ind1 = slim_ts.individual(pair[1])
        parents0 = ind0.parents
        parents1 = ind1.parents
        # print(i, pair[0], "parents:", parents0, pair[1], "parents:", parents1)
        shared = np.isin(parents0, parents1)
        nshared = sum(shared)
        # Half-sibs
        if nshared == 1:
            input_matrix[i, 0] = 1
            # print("half-sibs")
        # Sibs
        elif nshared == 2:
            input_matrix[i, 1] = 1
            # print("full-sibs")
        # Locations
        input_matrix[i, [2, 3]] = ind0.location[[0,1]]
        input_matrix[i, [4, 5]] = ind1.location[[0,1]]
        i += 1
    return(input_matrix)

# Sample from individuals currently alive and get close-kin relationships
current_individuals = pyslim.individuals_alive_at(slim_ts, 0)
sample = rng.choice(current_individuals, 20, replace = False)
pairs = itertools.combinations(sample, 2)
input_matrix = get_kin(slim_ts.first(), pairs)

# Population size
N = len(current_individuals)

np.savetxt(outfile, input_matrix, delimiter = ',', header = "half-sibs, sibs, x0, y0, x1, y1")


with open(outN, "w") as f:
    f.write(outfile + "," + str(N) + "\n")

