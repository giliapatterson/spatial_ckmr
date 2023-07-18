import math
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import sys
from scipy import stats
import itertools
rng = np.random.default_rng()

# Get the parents file path from the command line
parents_file = sys.argv[1]
n = int(sys.argv[2])
spaghetti_out = sys.argv[3]
sampling_out = sys.argv[4]
outN = sys.argv[5]

# Sample and get all combinations of pairs
parents = pd.read_csv(parents_file)
# Why don't column names get read in
parents.columns = ['individual', 'parent1', 'parent2', 'x', 'y', 'age']
N = len(parents)
sample_rows = rng.choice(np.arange(N), n, replace = False)

# Make this faster, maybe with a dictionary
pairs = list(itertools.combinations(sample_rows, 2))

# creating new Image object for spaghetti and sampling
w, h = 500, 500
spaghetti = Image.new("1", (w, h))
sampling = Image.new("1", (w, h))
img1 = ImageDraw.Draw(spaghetti)
img2 = ImageDraw.Draw(sampling)

#Number of parent offspring pairs
npairs = 0
# Plot spaghetti and sampling
for pair in pairs:
    ind0_i = pair[0]
    ind1_i = pair[1]
    ind0 = parents.iloc[ind0_i, :]
    ind1 = parents.iloc[ind1_i, :]
    x0 = ind0['x']*w
    y0 = ind0['y']*h
    x1 = ind1['x']*w
    y1 = ind1['y']*h
    if(ind0['individual'] == ind1['parent1'] or ind1['individual'] == ind0['parent1']):
        img1.line([(x0, y0), (x1, y1)], fill ="white", width = 0)
        npairs += 1
    img2.point([(x0, y0), (x1, y1)], fill = "white") 


spaghetti.save(spaghetti_out)
sampling.save(sampling_out)
with open(outN, "w") as f:
    f.write(spaghetti_out.replace("_spaghetti.png", "") + "," + str(N) + "," + str(n) + "," + str(npairs) + "\n")