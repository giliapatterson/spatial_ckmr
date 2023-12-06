import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import sys
import itertools
import math
import pandas as pd
from PIL import Image, ImageDraw
rng = np.random.default_rng()

# R0, rep
R0 = sys.argv[1]
rep = sys.argv[2]
# Get the parents file path from the command line
parents_file = sys.argv[3]
popsize_file = sys.argv[4]
# Output files
spaghetti_out = sys.argv[5]
sampling_out = sys.argv[6]
intensity_out = sys.argv[7]
metadata_out = sys.argv[8]

# Parents of all dead individuals
parents = pd.read_csv(parents_file)

# Population sizes
popsize = pd.read_csv(popsize_file)
# Calculate average population size
N = np.mean(popsize.loc[:,'N'])


# Sample from the individuals according to a sampling intensity grid. 
# Individuals from all years are lumped together but I can change this later

def sample_cell(sample_parents, xmin, xmax, ymin, ymax, nmax):
    # Sample from individuals within one grid cell
    in_i = np.where(np.logical_and(np.logical_and(sample_parents.loc[:,'x'] <= xmax, sample_parents.loc[:,'x'] >= xmin),
                np.logical_and(sample_parents.loc[:,'y'] >= ymin, sample_parents.loc[:,'y'] <= ymax)))[0]
    # Sample size is nmax or the number of individuals in the area
    ss = min(len(in_i), nmax)
    sample_rows = rng.choice(in_i, ss, replace = False)
    return(ss, sample_rows)

def sample_grid(individuals, sampling_intensity, n, width = 10, height = 10):
    # Sample from each grid cell
    # Sample size 
    ss = np.array(np.ceil(n*sampling_intensity/np.sum(sampling_intensity)), dtype = int)
    # Keep track of actual sample sizes (since if there are fewer than ss individuals in a grid cell, all are sampled)
    realized_ss = np.zeros(ss.shape, dtype = int)
    
    # Width and height of grid cells
    x_cells = ss.shape[0]
    y_cells = ss.shape[1]
    dx = width/x_cells
    dy = height/y_cells
    
    # Keep track of sampled rows
    #sample_rows = np.empty(round(np.sum(ss)), dtype = int)
    sample_rows = np.empty(0, dtype = int)
    # Sample from each grid cell
    for ix, iy in np.ndindex(ss.shape):
        xmin = dx*ix
        xmax = dx*ix + dx
        ymin = dy*iy
        ymax = dy*iy + dy
        nmax = ss[ix, iy]
        realized_ss[ix, iy], grid_rows = sample_cell(individuals, xmin, xmax, ymin, ymax, nmax)
        sample_rows = np.concatenate([sample_rows, grid_rows])
    return(realized_ss, sample_rows)

def make_spaghetti(sample_parents, image_w, image_h, max_width, max_height):
    # creating new Image object
    w, h = image_w, image_h
    spaghetti = Image.new("1", (w, h))
    img1 = ImageDraw.Draw(spaghetti)

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
        img1.line([(x_child*w/max_width, y_child*h/max_height), (x_parent*w/max_width, y_parent*h/max_height)], fill ="white", width = 0)

    return(spaghetti, npairs)

def plot_samples(sample_parents, image_w, image_h, max_width, max_height):
    # creating new Image object
    w, h = image_w, image_h
    sampling = Image.new("1", (w, h))
    img2 = ImageDraw.Draw(sampling)

    # Plot sampling
    for ind_i, ind_row in sample_parents.iterrows():
        x, y = ind_row[['x','y']]
        img2.point((x*w/max_width, y*h/max_height), fill = "white")
    return(sampling)

def plot_intensity(sampling_intensity, image_w, image_h):
    w, h = image_w, image_h
    intensity = Image.new("L", (w, h))
    img3 = ImageDraw.Draw(intensity)

    # Width and height of grid cells
    x_cells = sampling_intensity.shape[0]
    y_cells = sampling_intensity.shape[1]
    dx = w/x_cells
    dy = h/y_cells
    # Maximum sampling intensity (will be 255 or all white)
    max_int = np.max(sampling_intensity)
    # Plot sampling intensity
    for ix, iy in np.ndindex(sampling_intensity.shape):
        xmin = dx*ix
        xmax = dx*ix + dx
        ymin = dy*iy
        ymax = dy*iy + dy
        # Sampling
        rel_intensity = round(255*sampling_intensity[ix, iy]/max_int)
        img3.rectangle([(xmin, ymin), (xmax, ymax)], fill = rel_intensity, outline=None, width=0)
    return(intensity)

# Define sampling intensity grid with one side twice as likely to be sampled as the other
sampling_intensity =  np.ones((10,10))*np.linspace(1, 5, 10)

# Sample according to the grid and return realized sampling size and sampled individuals
ss, sample_rows = sample_grid(parents, sampling_intensity, 1000, 10, 10)
sample = parents.iloc[sample_rows]

# Plot spaghetti, locations of samples, and sampling intensity
spaghetti, npairs = make_spaghetti(sample, 500, 500, 10, 10)
sampling = plot_samples(sample, 500, 500, 10, 10)
intensity = plot_intensity(sampling_intensity, 500, 500)

spaghetti.save(spaghetti_out)
sampling.save(sampling_out)
intensity.save(intensity_out)

n = np.sum(ss)

with open(metadata_out, "w") as f:
    f.write(str(R0) + "," + str(rep) + ","+ str(N) + "," + str(n) + "\n")