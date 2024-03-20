library(tidyverse)
seal_parents <- read.csv("bearded_seal_parents.csv")
ggplot(seal_parents, aes(x = age)) +
  geom_histogram(binwidth = 1)

labels <- read.csv("bearded_seals/labels.csv")

ggplot(labels, aes(x = npairs, y = N_avg, color = factor(bias))) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of POPs") +
  scale_color_discrete(name = "Sampling bias")

ggplot(labels, aes(x = N_avg, y = npairs)) +
  geom_point() +
  xlab("Average N") +
  ylab("Number of POPs") +
  facet_wrap(~bias)

ggplot(labels, aes(x = N_avg, y = n)) +
  geom_point() +
  xlab("Average N") +
  ylab("Number of POPs") +
  facet_wrap(~bias)

