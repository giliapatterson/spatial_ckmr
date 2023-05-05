import math
from PIL import Image, ImageDraw
import pandas as pd
import numpy as np

# Get the kin file path from the command line
#kin_path = "/" + sys.argv[1]
kin_path = "flat_maps_data/spatial_kin/spatial_sim_5_0.csv"


kin = pd.read_csv(kin_path)
print(pd.names(kin))
print(np.max(kin[" x0"]))
print(np.max(kin[" x1"]))
print(np.max(kin[" y0"]))
print(np.max(kin[" y1"]))