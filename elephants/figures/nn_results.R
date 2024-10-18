library(tidyverse)
theme_set(theme_gray(base_size = 22))
res <- read.csv("network_results.csv")
names(res)

ggplot(res, aes(x = N, y = pred)) +
  geom_point() +
  ggtitle("Performance of CKMR network on simulated\n elephants for sample size around 300") +
  xlab("True N") +
  ylab("Predicted N") +
  geom_abline(slope = 1)
