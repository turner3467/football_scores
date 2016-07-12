setwd("~/Projects/football_scores/exploratory code")

library(mlogit)

measures <- read.csv("../data/processed/complete_measures.csv", stringsAsFactors = FALSE)
scores.map <- c("A"=-1, "D"=0, "H"=1)
measures$scores <- scores.map[measures$scores]

measures <- measures[, -c(1:6)]

#measures.imputed <- rfImpute(scores ~ ., data = measures)

smp_size <- floor(0.75 * nrow(measures))

## set the seed to make your partition reproductible
set.seed(101)
train_ind <- sample(seq_len(nrow(measures)), size = smp_size)

train <- measures[train_ind, ]
test <- measures[-train_ind, ]

d <- duplicated(train)
train.dd <- train[-d, ]

n <- names(train)
f <- as.formula(paste("scores ~ ", paste(n[!n %in% "scores"], collapse = " + ")))
ml.fit <- mlogit(f, data = train.dd, shape = "wide", choice = 0)


## Problem with singular matrix, therefore non invertible