library(ggplot2)
#Read experimental data (histogram)

fontSize = 2

filename = "sim.csv"
DATA = read.csv(file = filename, sep = ",",header = TRUE)
#serverChoice,numberOfServers,ServerIndex,ArrivalTime,startServerTime,DepartureTime
postscript("ComparisonSim.eps")
par(mfrow=c(3,1),oma=c(0,3,1,1),mar=c(1.5,2,1.5,2),mgp=c(2,1,0),xpd=NA, cex.lab=1, cex.axis=1)

#SoyournTime
ggplot(DATA,aes(y = (DepartureTime - ArrivalTime), x = factor(numberOfServers))) +
xlab("Number of servers")+ ylab("Sojourn Time") +
geom_boxplot(aes(fill=factor(serverChoice))) #+
#stat_summary(fun.y=mean, colour="darkred", geom="point", shape=18, size=3,show.legend = FALSE)
#dummy = graphics.off() # not show "null device" in terminal

ggplot(DATA,aes(y = (DepartureTime - startServerTime), x = factor(numberOfServers))) +
xlab("Number of servers")+ ylab("Service Time") +
geom_boxplot(aes(fill=factor(serverChoice))) #+
#stat_summary(fun.y=mean, colour="darkred", geom="point", shape=18, size=3,show.legend = FALSE)
#dummy = graphics.off() # not show "null device" in terminal

ggplot(DATA,aes(y = (startServerTime - ArrivalTime), x = factor(numberOfServers))) +
xlab("Number of servers")+ ylab("Waiting Time") +
geom_boxplot(aes(fill=factor(serverChoice))) #+
#stat_summary(fun.y=mean, colour="darkred", geom="point", shape=18, size=3,show.legend = FALSE)
dummy = graphics.off() # not show "null device" in terminal
