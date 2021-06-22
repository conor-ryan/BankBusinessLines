rm(list=ls())
library(data.table)
library(ggplot2)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
data = as.data.table(read.csv("Data/frdata_refined.csv"))
data[,date:=as.Date(date)]
data[,year:=as.numeric(format(date,"%Y"))]

## Bank Characteristics 

data[,salary_per_asset:=salaries/total_assets]
data[,premises_per_asset:=premises_cost/total_assets]
data[,other_per_asset:=other_cost/total_assets]
data[,total_per_asset:=total_cost/total_assets]

#Drop the banks(quarters) that report 0 assets or 0 costs
data = data[!is.na(total_assets)&total_assets>0]
data = data[!is.na(total_cost)&total_cost>0]

## Market Share as Percentage
data[,deposit_market_share:=deposit_market_share/100]
data[,consumer_market_share:=consumer_market_share/100]
data[,commercial_market_share:=commercial_market_share/100]
data[,insurance_market_share:=insurance_market_share/100]


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


#### Merge in Parent ID Mappings
load("Data/MarketStructure/OrgStructureByQuarter.rData")
data[,datenum:=year(date)*10000+month(date)*100+30]
nrow(data)

data = merge(data,qtr_map,by.x=c("RSSD9001","datenum"),by.y=c("OFFSPRING","quarter"),all.x=TRUE)
data[is.na(PARENT),PARENT:=RSSD9001]
data[,datenum:=NULL]
nrow(data)

## Check Duplicates 
data[,count:=1]
data[,count:=sum(count),by=c("RSSD9001","date")]
data[,sum(count>1)]


#### Merge in Branch Info ####
load("Data/bankbranches.Rdata")

### Manually Match IDs that are mismatched due to organizational structure

# 1020340 - BMO Bankcorp (15/25)
#  1025608 - First Hawaiian (26/26)
# 1037003 - M&T Bank (12/52)
# 1132449 - Citizens Financial (32/52)
#  1201934 - TCF Financial (2/44)
# 1245415 - BMO Financial (52/52)
# 3232316 - HSBC (52/52)
# 3489594 - 


# data = merge(data,branches,by.x=c("year","RSSD9001"),by.y=c("YEAR","RSSDHCR"),all.x=TRUE)
# data[,PARENT:=PARENT.x]
# data[,c("PARENT.x","PARENT.y"):=NULL]
data = merge(data,branches,by.x=c("year","PARENT"),by.y=c("YEAR","PARENT"),all.x=TRUE)


# test = data[,list(missing=sum(is.na(geo_coverage)),
#                   any_deposits = sum(!is.na(total_deposits&total_deposits>0)),
#                   avg_deposit_share = mean(deposit_market_share,na.rm=TRUE)),
#             by=c("RSSD9001","PARENT")]
# test
# 
# data[year>=2008&!is.na(total_deposits)&total_deposits>0,table(PARENT,is.na(geo_coverage))]
# 
# avg_share = data[,mean(deposit_market_share,na.rm=TRUE),by="RSSD9001"]
# 
# 
# load("Data/Branches/AllBranchData.rData")


#### Create Market Shares ####

## Compute Marketshare of the Outside Good
data[is.na(geo_coverage),deposit_market_share:=NA]
data[insurance_market_share<0.01,insurance_market_share:=NA]

data[,deposit_s0:=1-sum(deposit_market_share,na.rm=TRUE),by="date"]
data[,cons_loan_s0:=1-sum(consumer_market_share,na.rm=TRUE),by="date"]
data[,comm_loan_s0:=1-sum(commercial_market_share,na.rm=TRUE),by="date"]
data[,insurance_s0:=1-sum(insurance_market_share,na.rm=TRUE),by="date"]


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


#### Demand Estimation For Deposits #### 

### Naive 

data[,depvar:=log(deposit_market_share)-log(deposit_s0)]
summary(data[,lm(depvar~deposit_rate+as.factor(RSSD9001)+as.factor(date)+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])

## IV
dep_iv = data[,lm(deposit_rate~as.factor(RSSD9001)*FEDFUNDS)]

data[!is.na(deposit_rate),deposit_rate_iv:=predict(dep_iv)]

summary(data[,lm(depvar~deposit_rate_iv+as.factor(RSSD9001)+as.factor(date)+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])
data[,depvar:=NULL]


#### Demand Estimation For Consumer Loans #### 

## Naive
data[consumer_market_share>0,depvar:=log(consumer_market_share)-log(cons_loan_s0)]
summary(data[,lm(depvar~consumer_rate+as.factor(RSSD9001)+as.factor(date)+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])

## IV
cons_iv = data[,lm(consumer_rate~deposit_rate+salary_per_asset+premises_per_asset+other_per_asset+total_per_asset+as.factor(date)+as.factor(RSSD9001))]

data[!is.na(consumer_rate)&!is.na(deposit_rate),consumer_rate_iv:=predict(cons_iv)]

summary(data[,lm(depvar~consumer_rate_iv+as.factor(RSSD9001)+as.factor(date)+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])
summary(data[,lm(depvar~consumer_rate_iv+as.factor(RSSD9001)+as.factor(date)+salary_per_asset+premises_per_asset)])
data[,depvar:=NULL]

#### Demand Estimation For Commercial Loans #### 

## Naive
data[commercial_market_share>0,depvar:=log(commercial_market_share)-log(comm_loan_s0)]
summary(data[,lm(depvar~commercial_rate+as.factor(RSSD9001)+as.factor(date)+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])

## IV
comm_iv = data[,lm(commercial_rate~deposit_rate+salary_per_asset+premises_per_asset+other_per_asset+total_per_asset+as.factor(date)+as.factor(RSSD9001))]

data[!is.na(commercial_rate)&!is.na(deposit_rate),commercial_rate_iv:=predict(comm_iv)]

summary(data[,lm(depvar~commercial_rate_iv+as.factor(RSSD9001)+as.factor(date)+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])
summary(data[,lm(depvar~commercial_rate_iv+as.factor(RSSD9001)+as.factor(date)+salary_per_asset+premises_per_asset)])
data[,depvar:=NULL]

#### Insurance Demand Estimation ####
data[,depvar:=log(insurance_market_share)-log(insurance_s0)]
summary(data[,lm(depvar~insurance_price +as.factor(RSSD9001)+as.factor(date)+salary_per_asset+premises_per_asset)])

## IV
ins_iv = data[!is.na(insurance_market_share),lm(insurance_price~salary_per_asset+premises_per_asset+other_per_asset+total_per_asset+as.factor(date)+as.factor(RSSD9001))]

data[!is.na(insurance_market_share)&!is.na(insurance_price),insurance_price_iv:=predict(ins_iv)]

summary(data[,lm(depvar~insurance_price_iv+as.factor(RSSD9001)+as.factor(date)+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])
summary(data[,lm(depvar~insurance_price_iv+as.factor(RSSD9001)+as.factor(date)+salary_per_asset+premises_per_asset)])
data[,depvar:=NULL]
