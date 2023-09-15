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
if (len(sys.argv) > 6):
    method = sys.argv[6]
else:
    method = "random"
#print("Sampling with method", method)
# Sample and get all combinations of pairs
parents = pd.read_csv(parents_file)
# Why don't column names get read in
parents.columns = ['individual', 'parent1', 'parent2', 'age', 'x', 'y']
N = len(parents)

def spatially_biased(parents, nmax):
    # Sampling area size
    width = 0.5
    height = 0.5
    # Randomly choose sampling area
    xmin = rng.uniform(0, 1-width)
    xmax = xmin + width
    ymin = rng.uniform(0, 1-height)
    ymax = ymin + height

    # Sample from individuals within the area
    in_i = np.where(np.logical_and(np.logical_and(parents.loc[:,'x'] <= xmax, parents.loc[:,'x'] >= xmin),
                    np.logical_and(parents.loc[:,'y'] >= ymin, parents.loc[:,'y'] <= ymax)))[0]
    # Sample size is nmax or the number of individuals in the area
    ss = min(len(in_i), nmax)
    sample_rows = rng.choice(in_i, ss, replace = False)
    return(sample_rows, ss)

# Sample
if (method == "random"):
    sample_rows = rng.choice(np.arange(N), n, replace = False)
    ss = n
if (method == "biased"):
    sample_rows, ss = spatially_biased(parents, n)

sample_parents = parents.iloc[sample_rows, :]

# creating new Image object for spaghetti and sampling
w, h = 500, 500
spaghetti = Image.new("1", (w, h))
sampling = Image.new("1", (w, h))
img1 = ImageDraw.Draw(spaghetti)
img2 = ImageDraw.Draw(sampling)

# Find individuals with a parent that is in the sample
p_in_i = np.isin(sample_parents.loc[:,'parent1'], sample_parents.loc[:,'individual'])
npairs = sum(p_in_i)

# Get location of parent-offspring pairs and plot
children = sample_parents.loc[p_in_i, :]
for child_i, child_row in children.iterrows():
    parent_i = np.where(sample_parents.loc[:,'individual'] == child_row['parent1'])[0][0]
    parent_row = sample_parents.iloc[parent_i,:]
    # print(parent_row['individual'], child_row['individual'])
    x_child, y_child = child_row[['x','y']]
    x_parent, y_parent = parent_row[['x','y']]
    img1.line([(x_child*w, y_child*h), (x_parent*w, y_parent*h)], fill ="white", width = 0)

# Plot sampling
for ind_i, ind_row in sample_parents.iterrows():
    x, y = ind_row[['x','y']]
    img2.point((x*w, y*h), fill = "white")

spaghetti.save(spaghetti_out)
sampling.save(sampling_out)

with open(outN, "w") as f:
    f.write(spaghetti_out.replace("_spaghetti.png", "") + "," + str(N) + "," + str(ss) + "," + str(npairs) + "\n")