library(tidyverse)
library(mgcv)
theme_set(theme_gray(base_size = 22))

seal_parents <- read.csv("bearded_seal_parents.csv")
ggplot(seal_parents, aes(x = age)) +
  geom_histogram(binwidth = 1)

labels <- read.csv("bearded_seals/labels.csv")

ggplot(labels, aes(x = N_avg, y = npops, color = factor(bias))) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of POPs") +
  scale_color_discrete(name = "Sampling bias")

ggplot(labels, aes(x = N_avg, y = npops)) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of POPs") +
  facet_wrap(~bias)

ggplot(labels, aes(x = N_avg, y = nsibs, color = factor(bias))) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of sibs") +
  scale_color_discrete(name = "Sampling bias")

ggplot(labels, aes(x = N_avg, y = nsibs)) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of sibs") +
  facet_wrap(~bias)

ggplot(labels, aes(x = N_avg, y = n)) +
  geom_point() +
  xlab("Average N") +
  ylab("Sample size") +
  facet_wrap(~bias)

ggplot(labels, aes(x = N_avg, y = nsibs + npops)) +
  geom_point() +
  geom_smooth() +
  xlab("Average N") +
  ylab("Number of half-sibling and parent-offspring pairs") +
  facet_wrap(~bias, labeller = "label_both") 

labels_random <- mutate(labels, total_pairs = npops + nsibs) %>% filter(bias == 1)
model <- gam(N_avg ~ s(total_pairs, bs = "cs"), data = labels_random)
labels_random$fitted_N = model$fitted.values
labels_random[which(between(labels_random$fitted_N, 11990, 12010)),]

ggplot(labels_random, aes(x = total_pairs, y = N_avg)) +
  geom_point() +
  geom_line(aes(y = fitted_N), color = "blue") +
  xlab("Average N") +
  ylab("Number of half-sibling and parent-offspring pairs")
