import numpy as np
np.bool = np.bool_
from matplotlib import pyplot as plt
from scipy import stats
import sys
import itertools
import math
import pandas as pd
from PIL import Image, ImageDraw
rng = np.random.default_rng()

def find_POPs_or_sibs(focal_parents, sample_array, type):
    # focal_parents: List of individual IDs of the focal parents. The focal parents do not need to be in the sample.
    # sample_array: Array of information about the whole sample
    # type: "PO" or "HS"
    #   "PO": find pairs with parent in focal_parent_array and offspring in sample_array
    #   "sib": find pairs of children in sample_array that share a parent in focal_parent_array
    # Returns:
    # An array of tuples of either [(parent, offspring), ...] or [(sibling 1, sibling 2), ...]
    print("Finding pairs")
    relative_pairs = []
    for parent_id in focal_parents:
        #print("Parent", parent_id)
        children = sample_array[np.logical_or(sample_array.loc[:,'parent1'] == parent_id,
                                        sample_array.loc[:,'parent2'] == parent_id)]
        #print("Children")
        #print(children)
        if type == "PO":
        # Record POPs
            for j, child in children.iterrows():
                child_id = child['individual']
                relative_pairs.append((parent_id, child_id))
        if type == "HS":
            if len(children) == 2:
                sib_ids = children.loc[:,'individual'].values
                relative_pairs.append(tuple(np.sort(sib_ids)))
            if len(children) > 2:
                for pair in itertools.combinations(children.loc[:,'individual'], 2):
                    relative_pairs.append(tuple(np.sort(pair)))
    return(relative_pairs)

def draw_pairs(pairs, image, sample_array, max_width, max_height, w, h, color = "white"):
    # pairs: An array of tuples of individual ids
    # image: An image object to add lines to
    # sample_array: Array containing information about each individual
    # max_width, max_height: Size of map used in SLiM simulation
    # w, h: Size of image
    for pair in pairs:
        index1 = np.where(sample_array.loc[:,'individual'] == pair[0])
        index2 = np.where(sample_array.loc[:,'individual'] == pair[1])
        row1 = sample_array.iloc[index1]
        row2 = sample_array.iloc[index2]
        x1, y1 = row1[['x', 'y']].values[0]
        x2, y2 = row2[['x', 'y']].values[0]
        image.line([(x1*w/max_width, y1*h/max_height), (x2*w/max_width, y2*h/max_height)], fill =color, width = 0)