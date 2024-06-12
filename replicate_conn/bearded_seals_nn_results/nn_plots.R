library(tidyverse)
theme_set(theme_gray(base_size = 22))
seals_seals <- read.csv("model_pops_sibs.csv")
names(seals_seals)

ggplot(seals_seals, aes(x = truth, y = bearded_nn_pred, color = bias)) +
  geom_point() +
  ggtitle("Trained on: bearded seals\nTested on: bearded seals") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1)

ggplot(seals_seals, aes(x = truth, y = bearded_nn_pred)) +
  geom_point() +
  ggtitle("Performance of CKMR network for different levels of spatial sampling bias") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1) +
  facet_wrap(~bias, labeller = "label_both")

random_seals <- filter(seals_seals, bias == 1)
ggplot(random_seals, aes(x = truth, y = bearded_nn_pred)) +
  geom_point() +
  ggtitle("Performance of CKMR network for different levels of spatial sampling bias") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1)
