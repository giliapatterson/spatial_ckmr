library(tidyverse)
seal_parents <- read.csv("bearded_seal_parents.csv")
ggplot(seal_parents, aes(x = age)) +
  geom_histogram(binwidth = 1)

labels <- read.csv("bearded_seals/labels.csv")

ggplot(labels, aes(x = N_avg, y = npairs, color = factor(bias))) +
  geom_point() +
  geom_smooth()