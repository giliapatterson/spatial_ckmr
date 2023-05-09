import math
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import sys

# Get the kin file path from the command line
path = sys.argv[1]

spaghetti_out = sys.argv[2]
sampling_out = sys.argv[3]

kin = pd.read_csv(path, header = 0)
w, h = 500, 500
# creating new Image object
spaghetti = Image.new("RGB", (w, h))
sampling = Image.new("RGB", (w, h))
# create line image of parents
img1 = ImageDraw.Draw(spaghetti)
img2 = ImageDraw.Draw(sampling)
for i in range(len(kin)):
    row = kin.iloc[i]
    x0 = row["x0"]*w
    x1 = row["x1"]*w
    y0 = row["y0"]*h
    y1 = row["y1"]*h
    if row["parent0of1"]==1 or row["parent1of0"]==1:
        img1.line([(x0, y0), (x1, y1)], fill ="white", width = 0)
    img2.point([(x0, y0), (x1, y1)], fill = "white")    

spaghetti.save(spaghetti_out)
sampling.save(sampling_out)
