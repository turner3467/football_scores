# Plot distributions of parameters
# Correlations with score and explore collinearity
setwd("~/Projects/football_scores/exploratory code")

library(reshape2)
library(ggplot2)
library(dplyr)
measures <- read.csv("../data/processed/complete_measures.csv", stringsAsFactors = FALSE)

# Changing scores from A, D, H to -1, 0, 1
scores.map <- c("A"=-1, "D"=0, "H"=1)
measures$scores <- scores.map[measures$scores]

prop.table(table(measures$home_team_win_percent_last_5, measures$scores), margin = 1)

gg <- ggplot(data = measures, aes(x=factor(measures$scores), y=measures$home_team_win_percent_last_5))
gg +  geom_violin()

melt_df <- melt(measures[, c(27:37)])
h <- ggplot(data = melt_df, aes(x=value))
h + geom_density() + facet_wrap(~variable, scales = "free")

i <- ggplot(data = measures, aes(x=home_team_goals_conceded_last_10))
i + geom_histogram()

cor_mat <- cor(measures[, c(7:75)], use = "pairwise.complete.obs")

library(corrplot)
corrplot(cor_mat)
