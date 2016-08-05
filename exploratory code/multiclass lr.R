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
###measures <- measures[complete.cases(measures), ]

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
set.seed(101)
train_ind <- sample(seq_len(nrow(measures)), size = smp_size)

train <- measures[train_ind, ]
test <- measures[-train_ind, ]

## Using glmnet

y <- as.factor(train$scores)
x <- as.matrix(select(train, -scores))

lr.cv <- cv.glmnet(x, y, family = "multinomial", alpha = 0)
## lr.fit <- glmnet(x, y, family = "multinomial", alpha = 0, lambda = 0)

y.test <- as.factor(test$scores)
x.test <- as.matrix(select(test, -scores))
lr.class <- predict(lr.cv, newx = x.test, s = lr.cv$lambda.min, type = "class")
lr.pred <- predict(lr.cv, newx = x.test, s = lr.cv$lambda.min, type = "response")


## Using PCA

n.pc <- 7
y <- measures$scores
x <- as.matrix(select(measures, -scores))

pca <- prcomp(x, scale = TRUE)
x.pca <- pca$x

y.train <- y[train_ind]
y.test <- y[-train_ind]
x.train <- x.pca[train_ind, 1:n.pc]
x.test <- x.pca[-train_ind, 1:n.pc]

pca.fit <- glmnet(x.train, y.train, family = "multinomial", lambda = 0)
pca.class <- predict(pca.fit, newx = x.test, type = "class")
pca.pred <- predict(pca.fit, newx = x.test, type = "response")


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
