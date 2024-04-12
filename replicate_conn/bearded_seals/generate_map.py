import math
from PIL import Image, ImageDraw

w, h = 11, 11
k_map = Image.new("L", (w, h))
img1 = ImageDraw.Draw(k_map)
min_rel_k = 0.75
max_rel_k = 1
min_k = round(min_rel_k * 255)
max_k = round(max_rel_k * 255)

img1.rectangle([(0, 0), (w/2, h)], fill = min_k)
img1.rectangle([(w/2, 0), (w, h)], fill = max_k)

k_map.save("k_map.png")