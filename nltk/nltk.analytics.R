
bin <- read.csv("field_binary_by_prov.csv", sep=",")
count <- read.csv("field_count_by_prov.csv", sep=",")
anal <- read.csv("analyt_by_prov.csv", sep=",")
nltk <- read.csv("nltk.stats.csv", sep=",")
merged <- merge(bin, count, by="Provider")
merged <- merge(merged, anal, by="Provider")
merged <- merge(merged,nltk, by="Provider")

subset <- merged[,c('Provider','subject','total.fields','rec.count','Analytics')]
subset$fwc <- merged$fwc
subset$rightsPer <- (merged$rights / merged$rec.count)

subset$subPer <- (subset$subject / subset$rec.count)
subset$fieldPer <- (subset$total.fields / subset$rec.count)
subset$viewPer <- (subset$Analytics / subset$rec.count)
subset$wordsPer <- (subset$fwc / subset$rec.count)
subset$lowerhaps <- (merged$lowerhaps)
subset$vocab <- (merged$funiq)
subset$percentHaps <- (merged$lowerhaps / merged$fwc)

options(scipen=999)
coll_lm <- lm(viewPer ~ subPer+fieldPer+wordsPer, data=subset)
summary(coll_lm)

coll_lm2 <- lm(viewPer ~ subPer+rightsPer+fieldPer+wordsPer+lowerhaps+
                 vocab+percentHaps, data=subset)
summary(coll_lm2)

coll_haps <- lm(viewPer ~ lowerhaps, data=subset)
summary(coll_haps)

library(ggplot2)
ggplot(subset, aes(x=total.fields, y=viewPer))+
  geom_point(shape=1) +
  geom_smooth(method=lm)

library(car)
vif(coll_lm2)
