
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
parser.add_argument("--intensity_in", help = "path to input")
parser.add_argument("--intensity_out", help = "path to output")
args = parser.parse_args()

intensity_in = args.intensity_in
intensity_out = args.intensity_out

w, h = 500, 500
max_width = 10
max_height = 10

spatial_sample_intensity = pd.read_csv(intensity_in)

intensity = Image.new("L", (w, h))
img1 = ImageDraw.Draw(intensity)
xlist = spatial_sample_intensity.loc[:,'x'].values
ylist = spatial_sample_intensity.loc[:,'y'].values
fills = spatial_sample_intensity.loc[:,'nsampled'].values.astype(int)
dw = 1/3
dh = dw
maxfill = max(fills)
for i, fill in enumerate(fills):
    x0 = (xlist[i] - dw/2)*w/max_width
    y0 = (ylist[i] - dh/2)*h/max_height
    x1 = (xlist[i] + dw/2)*w/max_width
    y1 = (ylist[i] + dh/2)*h/max_height
    fill_n = int(255*fill/maxfill)
    img1.rectangle([x0, y0, x1, y1], fill = fill_n)
intensity.save(intensity_out)