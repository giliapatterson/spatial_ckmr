import numpy as np
from scipy import stats
import sys
import itertools
import math
import pandas as pd
from PIL import Image, ImageDraw
import argparse
import sampling_and_kin_functions as skf

parser = argparse.ArgumentParser()
parser.add_argument("-N", type = int, help = "population size")
parser.add_argument("-n", help = "sample size")
parser.add_argument("--rep", help = "replicate number")
parser.add_argument("--parents_file", help = "path to parents file")
parser.add_argument("--popsize_file", help = "path to popsize file")
parser.add_argument("--spaghetti_pops_out", help = "path to spaghetti plot of POPs")
parser.add_argument("--spaghetti_sibs_out", help = "path to spaghetti plot of sibs")
parser.add_argument("--metadata_out", help = "path to metadata file")
args = parser.parse_args()

N = args.N
n = args.n
rep = args.rep
parents_file = args.parents_file
popsize_file = args.popsize_file
spaghetti_pops_out = args.spaghetti_pops_out
spaghetti_sibs_out = args.spaghetti_sibs_out
metadata_out = args.metadata_out

# Population sizes
popsize = pd.read_csv(popsize_file)
# Calculate average population size
N_avg = np.mean(popsize.loc[:,'N'])
N_final = popsize.loc[:, 'N'].values[-1]

# Sampled individuals
parents = pd.read_csv(parents_file)
sample_parents = parents.drop_duplicates()

# Find individuals in the sample that have a child in the sample
ind_in_p1 = np.isin(sample_parents.loc[:,'individual'].values, sample_parents.loc[:,'parent1'])
ind_in_p2 = np.isin(sample_parents.loc[:,'individual'].values, sample_parents.loc[:,'parent2'])

# Mothers and Fathers
mothers = sample_parents[ind_in_p1]
fathers = sample_parents[ind_in_p2]
mother_list = mothers.loc[:,'individual'].values
father_list = fathers.loc[:,'individual'].values

# Find the parents of children in the sample and how many children in the sample they have (the parents don't need to be in the sample)
# Mothers are parent1 and fathers are parent2
all_mothers, all_mother_counts = np.unique(sample_parents.loc[:,'parent1'].values, return_counts = True)
all_fathers, all_father_counts = np.unique(sample_parents.loc[:,'parent2'].values, return_counts = True)

# Find parents with multiple children in the sample (parents of siblings)
maternal_sib_parents = all_mothers[all_mother_counts > 1]
paternal_sib_parents = all_fathers[all_father_counts > 1]

# Record POPs and half-sibling pairs
maternal_pops = skf.find_POPs_or_sibs(mother_list, sample_parents, "PO")
paternal_pops = skf.find_POPs_or_sibs(father_list, sample_parents, "PO")
maternal_sibs = skf.find_POPs_or_sibs(maternal_sib_parents, sample_parents, "HS")
paternal_sibs = skf.find_POPs_or_sibs(paternal_sib_parents, sample_parents, "HS")

# Full sibling pairs appear in both maternal and paternal arrays
if np.any([x in paternal_sibs for x in maternal_sibs]):
    full_sibs = maternal_sibs[np.where([x in paternal_sibs for x in maternal_sibs])[0][0]]
else:
    full_sibs = []

# Plot maternal POPs, paternal POPs, and half-sibling pairs
w, h = 500, 500
max_width = 10
max_height = 10

pops_spaghetti = Image.new("1", (w, h))
img1 = ImageDraw.Draw(pops_spaghetti)
skf.draw_pairs(maternal_pops, img1, sample_parents, max_width, max_height, w, h)
skf.draw_pairs(paternal_pops, img1, sample_parents, max_width, max_height, w, h)

sibs_spaghetti = Image.new("1", (w, h))
img2 = ImageDraw.Draw(sibs_spaghetti)
skf.draw_pairs(maternal_sibs, img2, sample_parents, max_width, max_height, w, h)
skf.draw_pairs(paternal_sibs, img2, sample_parents, max_width, max_height, w, h)

# Number of parent offspring and HS pairs
npops = len(maternal_pops) + len(paternal_pops)
nsibs =  len(maternal_sibs) + len(paternal_sibs)
nfullsibs = len(full_sibs)

print("Number of parent offspring pairs: ", npops)
print("Number of half-sibling pairs: ", nsibs)
print("Number of full-sibling pairs: ", nfullsibs)

pops_spaghetti.save(spaghetti_pops_out)
sibs_spaghetti.save(spaghetti_sibs_out)

with open(metadata_out, "w") as f:
    f.write(str(N) + "," + str(rep) + ","+ str(N_final) + ","+ str(n) + "," + str(npops) + "," + str(nsibs) + "," + str(nfullsibs) + "\n")
