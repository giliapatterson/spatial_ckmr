library(tidyverse)

theme_set(theme_gray(base_size = 22))

# Plot number of parent-offspring pairs vs population size

labels <- read.csv("../labels.csv", header = FALSE, col.names = c("path", "N", "n", "n_po_pairs")) |>
  separate_wider_delim(cols = path, delim = "_", names_sep = "") |>
  rename(K = path4, timepoint = path5) |>
  mutate(timepoint = as.numeric(timepoint))
labels_bias <- read.csv("../labels_bias.csv", header = FALSE, col.names = c("path", "N", "n", "n_po_pairs")) |>
  separate_wider_delim(cols = path, delim = "_", names_sep = "") |>
  rename(K = path4, timepoint = path5) |>
  mutate(timepoint = as.numeric(timepoint))

# Biased sampling with sample size 500
labels_bias_500 <- filter(labels_bias, n == 500)
short_labels <- select(labels, N, n_po_pairs, K, timepoint)
short_bias <- select(labels_bias_500, N, n_po_pairs, K, timepoint)

# Combine them
all <- full_join(short_labels, short_bias, by = c("N", "K", "timepoint"), suffix = c("", "_bias")) |>
  pivot_longer(c("n_po_pairs", "n_po_pairs_bias"), names_to = "Sampling", values_to = "pairs") |>
  mutate(Sampling = if_else(Sampling == "n_po_pairs_bias", "Biased", "Random"))

ggplot(all, aes(x = N, y = pairs, color = Sampling)) +
  geom_point() +
  ylab("Number of parent-offspring pairs") +
  scale_color_viridis_d(option = "H") +
  xlab("Population size")
ggsave("N_vs_PO.png")
