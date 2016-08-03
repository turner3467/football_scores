setwd("~/Projects/football_scores/exploratory code")

library(tidyr)
library(dplyr)
library(glmnet)

measures <- read.csv("../data/processed/complete_measures.csv", stringsAsFactors = FALSE)
scores.map <- c("A"=-1, "D"=0, "H"=1)
measures$scores <- scores.map[measures$scores]

measures <- measures[, -c(1:6)]

## Dropping head to head columns with large number of missing values
measures <- measures[, -grep("^hth.*(10|15)$", colnames(measures))]
measures <- measures[complete.cases(measures), ]
## measures.imputed <- rfImpute(scores ~ ., data = measures)

smp_size <- floor(0.75 * nrow(measures))

## set the seed to make your partition reproductible
set.seed(101)
train_ind <- sample(seq_len(nrow(measures)), size = smp_size)

train <- measures[train_ind, ]
test <- measures[-train_ind, ]

## Using glmnet

y <- as.factor(train$scores)
x <- as.matrix(select(train, -scores))

lr.fit <- glmnet(x, y, family = "multinomial", alpha = 0, lambda = 0)

y.test <- as.factor(test$scores)
x.test <- as.matrix(select(test, -scores))
lr.pred <- predict(lr.fit, newx = x.test, s = "lambda.min", type = "response")

## Plotting

library(ggplot2)

tmp <- as.data.frame(lr.pred)
names(tmp) <- c("L", "D", "W")

tmp2 <- gather(data = tmp, "class", "prob", 1:3)
ggplot(data = tmp2, aes(x=prob, fill = class, alpha = 0.5)) + geom_density()

## Implement scoring rule

log.scoring.rule <- function(y.hat, y){
    score <- 0
    for(idx in seq(1:length(y))){
        i <- as.character(y[idx])
        R.i <- y.hat[idx, i, 1]
        score <- score + log(R.i)
    }
    return(score)
}
