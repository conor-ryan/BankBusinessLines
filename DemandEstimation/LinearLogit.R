rm(list=ls())
library(data.table)
library(ggplot2)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
data = as.data.table(read.csv("Data/frdata_refined.csv"))
data[,date:=as.Date(date)]
data[,year:=as.numeric(format(date,"%Y"))]


### By Quarter Quantities
byQuarter = data[insurance_assets>0,list(total_assets = sum(total_assets,na.rm=TRUE)/1e6,
                       total_deposits=sum(total_deposits,na.rm=TRUE)/1e6,
                       new_cons_loans=sum(new_consumer_loans,na.rm=TRUE)/1e6,
                       new_comm_loans=sum(new_commercial_loans,na.rm=TRUE)/1e6,
                       insured_assets=sum(insurance_assets,na.rm=TRUE)/1e6),
                 by=c("date")]



#### Selection: Top 20, in any market in any quarter #####
firms = c()
for (var in c("deposit_market_share","consumer_market_share","commercial_market_share","insurance_market_share")){
  data[,share:=.SD,.SDcol=var]
  data[,temp_rank:=rank(-share,ties.method="average"),by="date"]
  firms_prod = data[share>0&temp_rank<=20,unique(RSSD9001)]
  firms = c(firms,firms_prod)
  data[,temp_rank:=NULL]
  data[,share:=NULL]
}
firms = sort(unique(firms))




data = data[RSSD9001%in%firms]


#### Merge in Branch Info ####


load("Data/bankbranches.Rdata")

### Manually Match IDs that are mismatched due to organizational structure

# 1020340 - BMO Bankcorp (15)
#  1026632 - Charles Schwab (16)
# 1037003 - M&T Bank (1)
# 1078529 - BBVA (1)
# 1132449 - Citizens Financial (32)
#  1201934 - TCF Financial (1)
# 1231968 - BNP Paribas (26)
# 1245415 - BMO Financial (1)
# 1249758 - General Electric (14)
# 1378434 - Mitsubishi Financial (1)
# 1447376 - USAA (16)
# 1562176 - AIG (4)
# 1575569



#### Merge in Parent ID Mappings
load("Data/MarketStructure/OrgStructureByQuarter.rData")
data[,datenum:=year(date)*10000+month(date)*100+30]
nrow(data)

data = merge(data,qtr_map,by.x=c("RSSD9001","datenum"),by.y=c("OFFSPRING","quarter"),all.x=TRUE)
data[is.na(PARENT),PARENT:=RSSD9001]
data[,datenum:=NULL]

branches[,datenum:=YEAR*10000+0330]
branches = merge(branches,qtr_map,by.x=c("RSSDHCR","datenum"),by.y=c("OFFSPRING","quarter"),all.x=TRUE)
branches[is.na(PARENT),PARENT:=RSSDHCR]
branches[,datenum:=NULL]


data = merge(data,branches,by.x=c("year","RSSD9001"),by.y=c("YEAR","RSSDHCR"),all.x=TRUE)
data = merge(data,branches,by.x=c("year","PARENT"),by.y=c("YEAR","PARENT"),all.x=TRUE)


test = data[,list(missing=sum(is.na(geo_coverage)),
                  any_deposits = sum(!is.na(total_deposits&total_deposits>0)),
                  avg_deposit_share = mean(deposit_market_share,na.rm=TRUE)),
            by="PARENT"]
test

data[year>=2008&!is.na(total_deposits)&total_deposits>0,table(PARENT,is.na(geo_coverage))]

avg_share = data[,mean(deposit_market_share,na.rm=TRUE),by="RSSD9001"]


load("Data/Branches/AllBranchData.rData")

#
# #### Average Trends (Quality Check) ####
# trends = data[,list(total_deposits=sum(total_deposits,na.rm=TRUE),
#                     consumer_loans=sum(consumer_loans,na.rm=TRUE),
#                     commercial_loans=sum(commercial_loans,na.rm=TRUE),
#                     deposit_rate=mean(deposit_rate,na.rm=TRUE),
#                     consumer_rate=mean(consumer_rate,na.rm=TRUE),
#                     commericial_rate=mean(commercial_rate,na.rm=TRUE),
#                     salaries=sum(salaries,na.rm=TRUE),
#                     premises_cost=sum(premises_cost,na.rm=TRUE),
#                     other_cost=sum(other_cost,na.rm=TRUE),
#                     total_cost=sum(total_cost,na.rm=TRUE)),
#               by="date"]
# trends[,date:=as.Date(date)]
#
# ### Quantity Trends
# ggplot(trends) +
#   geom_line(aes(x=date,y=total_deposits,color="Deposits")) +
#   geom_line(aes(x=date,y=consumer_loans,color="Consumer Loans")) +
#   geom_line(aes(x=date,y=commercial_loans,color="Commercial Loans"))
#
# ### Interest Trends
# ggplot(trends) +
#   geom_line(aes(x=date,y=deposit_rate,color="Deposits")) +
#   geom_line(aes(x=date,y=consumer_rate,color="Consumer Loans")) +
#   geom_line(aes(x=date,y=commericial_rate,color="Commercial Loans"))
#
# ### Cost Trends
# ggplot(trends) +
#   geom_line(aes(x=date,y=salaries,color="Salaries")) +
#   geom_line(aes(x=date,y=premises_cost,color="Premises")) +
#   geom_line(aes(x=date,y=other_cost,color="Other")) +
#   geom_line(aes(x=date,y=total_cost,color="Total Cost"))
#
#


#### Create Market Shares ####
## Merge in data on total quantities in each quarter
market = as.data.table(read.csv("Data/MarketSizeByQuarter.csv"))
names(market) = c("date","mkt_deposits","mkt_consumer_loans","mkt_commercial_loans")
data = merge(data,market,by="date",all.x=TRUE)


## Compute Market Share
data[,deposit_share:=total_deposits/mkt_deposits]
data[,cons_loan_share:=consumer_loans/mkt_consumer_loans]
data[,comm_loan_share:=commercial_loans/mkt_commercial_loans]

## Compute Marketshare of the Outside Good
data[,deposit_s0:=1-sum(deposit_share),by="date"]
data[,cons_loan_s0:=1-sum(cons_loan_share),by="date"]
data[,comm_loan_s0:=1-sum(comm_loan_share),by="date"]


#### Merge Info on Macro Environment ####
ffrate = as.data.table(read.csv("Data/OtherData/FEDFUNDS.csv"))
ffrate[,FEDFUNDS:=as.numeric(as.character(FEDFUNDS))]
ffrate[,DATE:=as.Date(DATE)]

## Need to convert beginning of quarter dates to end of quarter dates
quarter_map = ffrate[,"DATE"]
setkey(quarter_map,DATE)
quarter_map[,index:=1:nrow(quarter_map)]
quarter_ends = copy(quarter_map)
quarter_ends[,index:=index-1]
names(quarter_ends) = c("date_end","index_end")
quarter_map = merge(quarter_map,quarter_ends,by.x="index",by.y="index_end")
quarter_map[,date_end:=date_end-1]
quarter_map[,index:=NULL]

## Merge FF rate data into main data
ffrate = merge(ffrate,quarter_map,by="DATE")
data = merge(data,ffrate[,c("date_end","FEDFUNDS")],by.x="date",by.y="date_end",all.x=TRUE)


#### Naive Demand Estimations ####
data[,depvar:=log(deposit_share)-log(deposit_s0)]
summary(data[,lm(depvar~deposit_rate+as.factor(RSSD9001)+as.factor(date))])

data[,depvar:=log(cons_loan_share)-log(cons_loan_s0)]
summary(data[,lm(depvar~consumer_rate+as.factor(RSSD9001)+as.factor(date))])

data[,depvar:=log(comm_loan_share)-log(comm_loan_s0)]
summary(data[,lm(depvar~commercial_rate+as.factor(RSSD9001)+as.factor(date))])

#### Normalized Costs ####
data[,salary_perasset:=salaries/total_assets]
data[,premises_perasset:=premises_cost/total_assets]
data[,other_perasset:=other_cost/total_assets]
data[,total_perasset:=total_cost/total_assets]

#### Instrument for Deposit Rate ####
dep_iv = data[,lm(deposit_rate~as.factor(RSSD9001)*FEDFUNDS)]

data[!is.na(deposit_rate),deposit_rate_iv:=predict(dep_iv)]

data[,depvar:=log(deposit_share)-log(deposit_s0)]
summary(data[,lm(depvar~deposit_rate+as.factor(RSSD9001)+as.factor(date))])
summary(data[,lm(depvar~deposit_rate_iv+as.factor(RSSD9001)+as.factor(date))])


#### Instrument for Consumer Loan Rate ####
cons_iv = data[,lm(consumer_rate~deposit_rate+salary_perasset+premises_perasset+other_perasset+total_perasset+as.factor(date)+as.factor(RSSD9001))]

data[!is.na(consumer_rate),consumer_rate_iv:=predict(cons_iv)]

data[,depvar:=log(cons_loan_share)-log(cons_loan_s0)]
summary(data[,lm(depvar~consumer_rate+as.factor(RSSD9001)+as.factor(date))])
summary(data[,lm(depvar~consumer_rate_iv+as.factor(RSSD9001)+as.factor(date))])

#### Instrument for Commercial Loan Rate ####
comm_iv = data[,lm(commercial_rate~deposit_rate+salary_perasset+premises_perasset+other_perasset+total_perasset+as.factor(date)+as.factor(RSSD9001))]

data[!is.na(commercial_rate),commercial_rate_iv:=predict(comm_iv)]

data[,depvar:=log(comm_loan_share)-log(comm_loan_s0)]
summary(data[,lm(depvar~commercial_rate+as.factor(RSSD9001)+as.factor(date))])
summary(data[,lm(depvar~commercial_rate_iv+as.factor(RSSD9001)+as.factor(date))])
