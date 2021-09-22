rm(list=ls())
library(data.table)
library(ggplot2)
library(stargazer)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
data = as.data.table(read.csv("Data/frdata_refined.csv"))
data[,date:=as.Date(date)]
data[,year:=as.numeric(format(date,"%Y"))]
data[,X:=NULL]

ibanks = as.data.table(read.csv("Data/investment_refined.csv"))
ibanks[,date:=as.Date(date)]
ibanks = ibanks[date!="2021-03-31"]
ibanks[,X:=NULL]


data = merge(data,ibanks,by.x=c("date","RSSD9001"),by.y=c("date","id"),all=TRUE)
data[,total_assets:=total_assets.x]
data[,c("total_assets.y","total_assets.x"):=NULL]


## Bank Characteristics 

data[,salary_per_asset:=salaries/total_assets]
data[,premises_per_asset:=premises_cost/total_assets]
data[,other_per_asset:=other_cost/total_assets]
data[,total_per_asset:=total_cost/total_assets]

data[,insurance_price:=insurance_price*100]
data[,investment_price:=investment_price*100]

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
for (var in c("deposit_market_share","consumer_market_share","commercial_market_share","insurance_market_share","investment_market_share")){
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
# data[is.na(geo_coverage),deposit_market_share:=NA]
# data[insurance_market_share<0.005,insurance_market_share:=NA]
# 
# data[,deposit_s0:=1-sum(deposit_market_share,na.rm=TRUE),by="date"]
# data[,cons_loan_s0:=1-sum(consumer_market_share,na.rm=TRUE),by="date"]
# data[,comm_loan_s0:=1-sum(commercial_market_share,na.rm=TRUE),by="date"]
# data[,insurance_s0:=1-sum(insurance_market_share,na.rm=TRUE),by="date"]


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


#### Some additional Variable Edits ####
data[,bankFactor:=as.factor(RSSD9001)]
data[,dateFactor:=as.factor(date)]


save(data,file="Data/EstimationSample.RData")
#### Demand Estimation For Deposits #### 

### Naive 

data[,depvar:=log(total_deposits)]
dep_ols = data[,lm(depvar~deposit_rate+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)]

## IV
dep_iv = data[,lm(deposit_rate~FEDFUNDS + FEDFUNDS*bankFactor)]

data[!is.na(deposit_rate),deposit_rate_iv:=predict(dep_iv)]

dep_res = data[,lm(depvar~deposit_rate_iv+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)]
data[,depvar:=NULL]


#### Demand Estimation For Consumer Loans #### 

## Naive
data[consumer_market_share>0,depvar:=log(new_consumer_loans)]
cons_ols = data[,lm(depvar~consumer_rate+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)]

## IV
cons_iv = data[,lm(consumer_rate~deposit_rate+salary_per_asset+premises_per_asset+other_per_asset+total_per_asset+dateFactor+bankFactor)]
cons_iv = data[,lm(consumer_rate~FEDFUNDS+bankFactor*FEDFUNDS)]

# data[!is.na(consumer_rate)&!is.na(deposit_rate),consumer_rate_iv:=predict(cons_iv)]
data[!is.na(consumer_rate),consumer_rate_iv:=predict(cons_iv)]

summary(data[,lm(depvar~consumer_rate_iv+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])
cons_res = data[,lm(depvar~consumer_rate_iv+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)]
data[,depvar:=NULL]

#### Demand Estimation For Commercial Loans #### 

## Naive
data[commercial_market_share>0,depvar:=log(new_commercial_loans)]
comm_ols = data[,lm(depvar~commercial_rate+branch_count+geo_coverage+bankFactor+dateFactor+salary_per_asset+premises_per_asset)]

## IV
comm_iv = data[,lm(commercial_rate~deposit_rate+salary_per_asset+premises_per_asset+other_per_asset+total_per_asset+dateFactor+bankFactor)]

data[!is.na(commercial_rate)&!is.na(deposit_rate),commercial_rate_iv:=predict(comm_iv)]

# summary(data[,lm(depvar~commercial_rate_iv+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])
comm_res = data[,lm(depvar~commercial_rate_iv+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)]
data[,depvar:=NULL]

#### Insurance Demand Estimation ####
data[insurance_market_share>0.005,depvar:=log(insurance_assets)]
ins_ols = data[,lm(depvar~insurance_price +bankFactor+dateFactor+salary_per_asset+premises_per_asset)]

## IV
ins_iv = data[insurance_market_share>0.005,lm(insurance_price~salary_per_asset+premises_per_asset+other_per_asset+total_per_asset+dateFactor+bankFactor)]

data[insurance_market_share>0.005&!is.na(insurance_price),insurance_price_iv:=predict(ins_iv)]

# summary(data[,lm(depvar~insurance_price_iv+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)])
ins_res = data[,lm(depvar~insurance_price_iv+bankFactor+dateFactor+salary_per_asset+premises_per_asset)]
data[,depvar:=NULL]


#### Investment Bank Demand Estimation ####
data[investment_quantity>0,depvar:=log(investment_quantity)]
inv_ols = data[,lm(depvar~investment_price+bankFactor+dateFactor+salary_per_asset+premises_per_asset)]

## IV
inv_iv = data[,lm(investment_price~salary_per_asset+premises_per_asset+other_per_asset+total_per_asset+dateFactor+bankFactor)]

data[!is.na(investment_price),investment_price_iv:=predict(inv_iv)]

inv_res = data[,lm(depvar~investment_price_iv+bankFactor+dateFactor+salary_per_asset+premises_per_asset)]
data[,depvar:=NULL]


#### Output Latex Tables ####
names(dep_res$coefficients) = gsub("_iv","",names(dep_res$coefficients))

names(cons_res$coefficients) = gsub("(commercial|consumer)_","",names(cons_res$coefficients))
names(cons_ols$coefficients) = gsub("(commercial|consumer)_","",names(cons_ols$coefficients))
names(cons_res$coefficients) = gsub("_iv","",names(cons_res$coefficients))

names(comm_res$coefficients) = gsub("(commercial|consumer)_","",names(comm_res$coefficients))
names(comm_ols$coefficients) = gsub("(commercial|consumer)_","",names(comm_ols$coefficients))
names(comm_res$coefficients) = gsub("_iv","",names(comm_res$coefficients))

names(ins_res$coefficients) = gsub("(insurance|investment)_","",names(ins_res$coefficients))
names(ins_ols$coefficients) = gsub("(insurance|investment)_","",names(ins_ols$coefficients))
names(ins_res$coefficients) = gsub("_iv","",names(ins_res$coefficients))

names(inv_res$coefficients) = gsub("(insurance|investment)_","",names(inv_res$coefficients))
names(inv_ols$coefficients) = gsub("(insurance|investment)_","",names(inv_ols$coefficients))
names(inv_res$coefficients) = gsub("_iv","",names(inv_res$coefficients))

## By Demand Estimation
stargazer(dep_iv,dep_ols,dep_res,cons_iv,cons_ols,cons_res,comm_iv,comm_ols,comm_res,
          omit=c("bankFactor","dateFactor","Constant"),
          covariate.labels=c("Fed Funds Rate","Deposit Rate","Loan Rate","Branch Count","Geographic Cov.","Salaries","Premises Cost",
                              "Other non-Int. Cost","Total Cost"),
          digits = 2)


stargazer(ins_iv,ins_ols,ins_res,inv_iv,inv_ols,inv_res,
          omit=c("bankFactor","dateFactor","Constant"),
          covariate.labels=c("Price","Salaries","Premises Cost",
                             "Other non-Int. Cost","Total Cost"),
          digits = 2)



# ## First Stage
# stargazer(dep_iv,cons_iv,comm_iv,ins_iv,inv_iv,omit=c("bankFactor","dateFactor","Constant"),
#           covariate.labels=c("Fed Funds Rate","Deposit Rate","Salary per Asset","Premises Cost per Asset",
#                              "Other non-Interest Cost per Asset","Total Cost per Asset"))
# 
# ## Second Stage
# stargazer(dep_res,cons_res,comm_res,ins_res,inv_res,omit=c("bankFactor","dateFactor","Constant"),
#           covariate.labels=c("Interest Rate","Investment Price","Insurance Premium","Number of Branches","Geographic Coverage","Salary per Asset","Premises Cost per Asset"))


##### Elasticities ####

data[,dep_elas:=dep_res$coefficients["deposit_rate"]*(1-deposit_market_share)*deposit_rate]
data[,cons_elas:=cons_res$coefficients["rate"]*(1-consumer_market_share)*consumer_rate]
data[,comm_elas:=comm_res$coefficients["rate"]*(1-commercial_market_share)*commercial_rate]
data[,inv_elas:=inv_res$coefficients["price"]*(1-investment_market_share)*investment_price]

data[,dep_semielas:=dep_res$coefficients["deposit_rate"]*(1-deposit_market_share)/100]
data[,cons_semielas:=cons_res$coefficients["rate"]*(1-consumer_market_share)/100]
data[,comm_semielas:=comm_res$coefficients["rate"]*(1-commercial_market_share)/100]
data[,inv_semielas:=inv_res$coefficients["price"]**(1-investment_market_share)]

