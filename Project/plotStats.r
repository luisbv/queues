library(ggplot2)
#Read experimental data (histogram)

fontSize = 2

filename = "stats.csv"
DATA = read.csv(file = filename, sep = ",",header = TRUE)

postscript("Comparison.eps")
ggplot(DATA,aes(y = servicePercentage, x = factor(numberServers))) +
xlab("Number of servers")+ ylab("Service Percentage") +
geom_boxplot(aes(fill=factor(serverChoice))) #+
#stat_summary(fun.y=mean, colour="darkred", geom="point", shape=18, size=3,show.legend = FALSE)
dummy = graphics.off() # not show "null device" in terminal
