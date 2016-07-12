setwd("~/Projects/football_scores/exploratory code")

library(randomForest)

measures <- read.csv("../data/processed/complete_measures.csv", stringsAsFactors = FALSE)

# Changing scores from A, D, H to -1, 0, 1
scores.map <- c("A"=-1, "D"=0, "H"=1)
measures$scores <- scores.map[measures$scores]

measures <- measures[, -c(1:6)]

#measures.imputed <- rfImpute(scores ~ ., data = measures)

smp_size <- floor(0.75 * nrow(measures))

## set the seed to make your partition reproductible
set.seed(123)
train_ind <- sample(seq_len(nrow(measures)), size = smp_size)

train <- measures[train_ind, ]
test <- measures[-train_ind, ]

rf.fit <- randomForest(scores ~ ., data = train)
