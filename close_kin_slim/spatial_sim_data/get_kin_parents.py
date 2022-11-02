import numpy as np
from scipy import stats
import itertools
import math
import sys
import pandas as pd


rng = np.random.default_rng()

# Get the parents file path and output file path from the command line
parents_file = sys.argv[1]
outfile = sys.argv[2]
outN = sys.argv[3]
n = int(sys.argv[4])

def get_parents(parents_file, n):
    parents = pd.read_csv(parents_file)
    parents.columns = ['individual', 'parent1', 'parent2', 'x', 'y', 'age']
    N = len(parents)
    sample_rows = rng.choice(np.arange(N), n, replace = False)
    pairs = list(itertools.combinations(sample_rows, 2))
    # Rows are pairs, columns are ind0 is parent of ind1 (0 or 1), ind1 is parent of ind0 (0 or 1), x0, y0, x1, y1, age0, age1
    kin_matrix = np.zeros([len(pairs), 8])
    i = 0
    for pair in pairs:
        ind0_i = pair[0]
        ind1_i = pair[1]
        ind0 = parents.iloc[ind0_i, :]
        ind1 = parents.iloc[ind1_i, :]
        if(ind0['individual'] == ind1['parent1']):
            kin_matrix[i, 0] = 1
        if(ind1['individual'] == ind0['parent1']):
            kin_matrix[i, 1] = 1
        kin_matrix[i, 2:4] = ind0[['x', 'y']]
        kin_matrix[i, 4:6] = ind1[['x', 'y']]
        kin_matrix[i, 6:8] = [ind0['age'], ind1['age']]
        i += 1
    return(kin_matrix, N)

# Sample from individuals currently alive and get parent offspring relationships
kin_matrix, N = get_parents(parents_file, n)

np.savetxt(outfile, kin_matrix, delimiter = ',', header = "parent0of1, parent1of0, x0, y0, x1, y1, age0, age1")

with open(outN, "w") as f:
    f.write(outfile + "," + str(N) + "\n")

