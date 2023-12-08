library(tidyverse)
theme_set(theme_gray(base_size = 22))
un_un <- read.csv("unbiased_nn_results.csv")
bias_bias <- read.csv("biased_nn_results.csv")
un_bias <- read.csv("unbiased_nn_biased_data.csv")
bias_un <- read.csv("bias_nn_unbiased_data.csv")

names(un_un)
names(bias_bias)
names(un_bias)
names(bias_un)

ggplot(un_un, aes(x = truth, y = unbiased_nn_pred)) +
  geom_point() +
  ggtitle("Trained on: random sampling\nTested on: random sampling") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1) +
  ylim(c(0, 10000))

ggplot(bias_bias, aes(x = bias_truth, y = biased_nn_pred)) +
  geom_point() +
  ggtitle("Trained on: spatially-biased sampling\nTested on: spatially-biased sampling") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1) +
  ylim(c(0, 10000))

ggplot(un_bias, aes(x = bias_truth, y = unbiased_nn_pred)) +
  geom_point() +
  ggtitle("Trained on: random sampling\nTested on: spatially-biased sampling") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1)+
  geom_abline(slope = 1/4)+
  ylim(c(0, 10000))

ggplot(bias_un, aes(x = truth, y = biased_nn_pred)) +
  geom_point() +
  ggtitle("Trained on: spatially-biased sampling\nTested on: random sampling") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1) +
  geom_abline(slope = 4) +
  ylim(0, 15000)
