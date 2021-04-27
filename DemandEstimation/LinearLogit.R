rm(list=ls())
library(data.table)
library(ggplot2)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
data = as.data.table(read.csv("Data/loan_deposit_data.csv"))


## Keep data series that has consumer loan rate, set INF to missing
data = data[!is.na(consumer_rate)]
data[,sum(deposit_rate==-Inf |deposit_rate==Inf,na.rm=TRUE)]
data[deposit_rate==-Inf |deposit_rate==Inf ,deposit_rate:=NA]
data[,sum(consumer_rate==-Inf |consumer_rate==Inf)]
data[consumer_rate==-Inf |consumer_rate==Inf ,consumer_rate:=NA]
data[,sum(commercial_rate==-Inf|commercial_rate==Inf)]
data[commercial_rate==-Inf|commercial_rate==Inf,commercial_rate:=NA]


data[,summary(lm(consumer_rate~deposit_rate+date + as.factor(ID)))]
data[,summary(lm(commercial_rate~deposit_rate))]
data[,summary(lm(consumer_rate~commercial_rate))]


#### Big Banks Only (by deposits) ####
data[,quarterly_deposits:=sum(total_deposits),by="date"]
data[,deposit_share:=total_deposits/quarterly_deposits]
data[,avg_share:=mean(deposit_share),by="ID"]

big = data[avg_share>0.005]
big[,length(unique(ID))]
big[,big_deposits:=sum(total_deposits),by="quarterly_deposits"]
big[,big_bank_ratio:=big_deposits/quarterly_deposits]
big[,deposit_loan_ratio:=(consumer_loans+commercial_loans)/total_deposits]


big[,summary(lm(consumer_rate~deposit_rate + date))]


ggplot(big[date=="2008-09-30"]) + aes(x=deposit_rate,y=consumer_rate) + geom_point() + geom_smooth(method="lm")
