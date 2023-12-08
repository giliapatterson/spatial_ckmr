library(ggplot2)
library(emojifont)
library(png)





# Low, medium, and intermediate densities
# Low K = 2000
low <- read.csv("../spatial_parents/spatial_sim_parents_2000_0.csv")
low_samples <- readPNG("../images/spatial_sim_parents_2000_0_500_samples.png")
h<-dim(low_samples)[1]
w<-dim(low_samples)[2]
low_locations <- as_tibble(which(low_samples > 0, arr.ind = TRUE)) |>
  rename(x = col, y = row) |>
  mutate(x = x/w, y = 1- y/h)
low_bias <- readPNG("../images_bias/spatial_sim_parents_2000_0_500_samples.png")
low_bias_locations <- as_tibble(which(low_bias > 0, arr.ind = TRUE)) |>
  rename(x = col, y = row) |>
  mutate(x = x/w, y = 1- y/h)


# Mid K = 6000
mid <- read.csv("../spatial_parents/spatial_sim_parents_6000_0.csv")
mid_samples <- readPNG("../images/spatial_sim_parents_6000_0_500_samples.png")
mid_locations <- as_tibble(which(mid_samples > 0, arr.ind = TRUE)) |>
  rename(x = col, y = row) |>
  mutate(x = x/w, y = y/h)
mid_bias <- readPNG("../images_bias/spatial_sim_parents_6000_0_500_samples.png")
mid_bias_locations <- as_tibble(which(mid_bias > 0, arr.ind = TRUE)) |>
  rename(x = col, y = row) |>
  mutate(x = x/w, y = 1- y/h)

# High K = 9900
high <- read.csv("../spatial_parents/spatial_sim_parents_9900_0.csv")
high_samples <- readPNG("../images/spatial_sim_parents_9900_0_500_samples.png")
high_locations <- as_tibble(which(high_samples > 0, arr.ind = TRUE)) |>
  rename(x = col, y = row) |>
  mutate(x = x/w, y = 1- y/h)
high_bias <- readPNG("../images_bias/spatial_sim_parents_9900_0_500_samples.png")
high_bias_locations <- as_tibble(which(high_bias > 0, arr.ind = TRUE)) |>
  rename(x = col, y = row) |>
  mutate(x = x/w, y = 1- y/h)

ggplot() +
  geom_point(aes(x=x, y=y), data = low) +
  geom_point(aes(x=x, y=y), data = low_locations, color = "blue") +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("")
ggsave("low_sim.png")
ggplot() +
  geom_point(aes(x=x, y=y), data = low_locations, color = "blue") +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("") +
  xlim(c(0, 1)) +
  ylim(c(0, 1))
ggsave("low_samples.png")
ggplot() +
  geom_point(aes(x=x, y=y), data = low_bias_locations, color = "blue") +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("") +
  xlim(c(0, 1)) +
  ylim(c(0, 1))
ggsave("low_bias.png")


ggplot() +
  geom_point(aes(x=x, y=y), data = mid) +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("")
ggsave("mid_sim.png")
ggplot() +
  geom_point(aes(x=x, y=y), data = mid_locations, color = "blue") +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("") +
  xlim(c(0, 1)) +
  ylim(c(0, 1))
ggsave("mid_samples.png")
ggplot() +
  geom_point(aes(x=x, y=y), data = mid_bias_locations, color = "blue") +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("") +
  xlim(c(0, 1)) +
  ylim(c(0, 1))
ggsave("mid_bias.png")

ggplot() +
  geom_point(aes(x=x, y=y), data = high) +
  coord_quickmap() +
  theme_bw()+
  xlab("") +
  ylab("")
ggsave("high_sim.png")
ggplot() +
  geom_point(aes(x=x, y=y), data = high_locations, color = "blue") +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("") +
  xlim(c(0, 1)) +
  ylim(c(0, 1))
ggsave("high_samples.png")
ggplot() +
  geom_point(aes(x=x, y=y), data = high_bias_locations, color = "blue") +
  coord_quickmap() +
  theme_bw() +
  xlab("") +
  ylab("") +
  xlim(c(0, 1)) +
  ylim(c(0, 1))
ggsave("high_bias.png")
