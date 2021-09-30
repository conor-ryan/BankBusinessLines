rm(list=ls())
library(data.table)
library(ggplot2)
library(stargazer)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
load(file="Data/EstimationSample.RData")


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

