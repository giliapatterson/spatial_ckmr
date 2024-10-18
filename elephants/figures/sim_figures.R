library(tidyverse)
library(mgcv)
theme_set(theme_gray(base_size = 22))
library(png)
library(stars)
library(sf)
library(tigris)
library(raster)
library(ggforce)
library(viridis)

dir = "."

kibale = read_stars("../kibale.png")
map_w = dim(kibale$kibale.png)['x']
map_h = dim(kibale$kibale.png)['y']
sim_w = 10
sim_h = 10

parents = read_csv("random_sample_586_1000_11.csv", col_types = "fffifiinn")
parents <- mutate(parents, map_x = map_w*x/sim_w, map_y = map_h*y/sim_h)

if(nrow(parents) != length(unique(parents$individual))){
  print("Not all individuals were sampled")
}
parents <- mutate(parents, age_class = case_when(age < 15 ~ "Juvenile", .default = "Adult"))

females <- filter(parents, sex == "F")
males <- filter(parents, sex == "M")

femandjuv <- filter(parents, sex == "F" | age <15)
adultmale <- filter(parents, sex == "M" & age >= 15)

ggplot() +
  geom_stars(data=kibale) +
  scale_fill_gradientn(colours=c("grey", "white"), guide='none') +
  coord_sf() +
  geom_point(data = females, aes(x = map_x, y = map_y, color = age_class)) +
  scale_color_viridis_d(name = "Age class") +
  theme_void(base_size = 22) +
  ggtitle("Female elephants")

ggplot() +
  geom_stars(data=kibale) +
  scale_fill_gradientn(colours=c("grey", "white"), guide='none') +
  coord_sf() +
  geom_point(data = males, aes(x = map_x, y = map_y, color = age_class)) +
  scale_color_viridis_d(name = "Age class") +
  theme_void(base_size = 22) +
  ggtitle("Male elephants")

ggplot() +
  geom_stars(data=kibale) +
  scale_fill_gradientn(colours=c("grey", "white"), guide='none') +
  coord_sf() +
  geom_point(data = femandjuv, aes(x = map_x, y = map_y, color = age_class)) +
  scale_color_viridis_d(name = "Age class") +
  theme_void(base_size = 22) +
  ggtitle("Female and juvenile male elephants")

ggplot() +
  geom_stars(data=kibale) +
  scale_fill_gradientn(colours=c("grey", "white"), guide='none') +
  coord_sf() +
  geom_point(data = adultmale, aes(x = map_x, y = map_y, color = age_class)) +
  scale_color_viridis_d(name = "Age class") +
  theme_void(base_size = 22) +
  ggtitle("Adult male elephants")

  