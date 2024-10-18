library(tidyverse)
library(mgcv)
theme_set(theme_gray(base_size = 22))

base_folder = "../elephant_data/"

spatial_labels <- read_csv(paste0(base_folder,"spatial_labels.csv"))
random_labels <- read_csv(paste0(base_folder,"random_labels.csv"))
spatial_labels$type = "spatial"
random_labels$type = "random"
labels = bind_rows(spatial_labels, random_labels)

ggplot(labels, aes(x = N, y = npops, color = type)) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of POPs") +
  scale_color_discrete(name = "Sample") +
  facet_wrap(~n, nrow = 4)
ggplot(labels, aes(x = N, y = nsibs, color = type)) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of POPs") +
  scale_color_discrete(name = "Sample") +
  facet_wrap(~n, nrow = 4)

ggplot(labels, aes(x = N, y = nsibs + npops, color = type)) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of half-sibling and parent-offspring pairs") +
  facet_wrap(~n, labeller = "label_both") 
