setwd("~/Projects/football_scores/exploratory code")

library(randomForest)

measures <- read.csv("../data/processed/complete_measures.csv", stringsAsFactors = FALSE)

# Changing scores from A, D, H to -1, 0, 1
scores.map <- c("A"=-1, "D"=0, "H"=1)
measures$scores <- scores.map[measures$scores]

measures <- measures[, -c(1:6)]
measures <- measures[, -grep("^hth.*(10|15)$", colnames(measures))]
measures$scores <- as.factor(measures$scores)

## Imputation
mode.fn <- function(x){
    x <- x[!is.na(x)]
    mod <- unique(x)
    tab <- tabulate(match(x, mod))
    return(mod[tab == max(tab)])
}

for(j in seq(1:ncol(measures))){
    j.mod <- mode.fn(measures[, j])
    for(i in seq(1:nrow(measures))){
        if(is.na(measures[i, j])){
            measures[i, j] <- base::sample(j.mod, size = 1)
        }
    }
}


smp_size <- floor(0.75 * nrow(measures))

## set the seed to make your partition reproductible
set.seed(123)
train_ind <- sample(seq_len(nrow(measures)), size = smp_size)

train <- measures[train_ind, ]
test <- measures[-train_ind, ]

rf.fit <- randomForest(scores ~ ., data = train)
rf.class <- predict(rf.fit, newdata = test, type = "response")
rf.pred <- predict(rf.fit, newdata = test, type = "prob")

## Implement scoring rule

log.scoring.rule <- function(y.hat, y){
    score <- 0
    for(idx in seq(1:length(y))){
        i <- as.character(y[idx])
        R.i <- y.hat[idx, i]
        score <- score + log(R.i)
    }
    return(score)
}
