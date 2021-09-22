rm(list=ls())
library(data.table)
library(ggplot2)
library(stargazer)
library(xtable)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
load("Data/EstimationSample.RData")

## Variable Adjustments
data[,total_deposits:=total_deposits/1e6]
data[,new_consumer_loans:=new_consumer_loans/1e6]
data[,new_commercial_loans:=new_commercial_loans/1e6]
data[,insurance_assets:=insurance_assets/1e6]
data[,investment_quantity:=investment_quantity/1e6]

data[,salary_per_asset:=salary_per_asset*1e3]
data[,premises_per_asset:=premises_per_asset*1e3]
data[,other_per_asset:=other_per_asset*1e3]
data[,total_per_asset:=total_per_asset*1e3]

data[,salaries:=salaries/1e3]
data[,premises_cost:=premises_cost/1e3]

data[,deposit_rate:=deposit_rate*100]
data[,consumer_rate:=consumer_rate*100]
data[,commercial_rate:=commercial_rate*100]

data[insurance_assets<10,insurance_price:=NA]
#### Table 1 #####

table1 = NULL
var_list = c("total_deposits","deposit_market_share","deposit_rate",
             "new_consumer_loans","consumer_market_share","consumer_rate",
             "new_commercial_loans","commercial_market_share","commercial_rate",
             "insurance_assets","insurance_market_share","insurance_price")

var_list = c("total_deposits","new_consumer_loans","new_commercial_loans","insurance_assets","investment_quantity",
             "deposit_rate","consumer_rate","commercial_rate","insurance_price","investment_price",
             "salaries","premises_cost",
             "salary_per_asset","premises_per_asset","other_per_asset","total_per_asset",
             "branch_count","geo_coverage")

var_list_clean = c("Total Deposits (billions)",
             "Consumer Loans Issued (billions)",
             "Commercial Loans Issued (billions)",
             "Insured Assets (billions)","Underwriting Activity (billions)",
             "Deposit Interest Rate","Cons. Loan Interest Rate","Comm. Interest Rate","Ins. Premium","I Bank Fee",
             "Salary (thousands)","Building Costs (thousands)",
             "Salary per Asset($/million)","Building Cost per Asset ($/million)",
             "Non Interest Costs per Asset ($/million)","Total Costs per Asset ($/million)",
             "Number of Branches","Geographic Coverage")
# var_list_clean = var_list



for (i in 1:length(var_list)){
  var = var_list[i]
  data[,tempvar:=.SD,.SDcol=var]
  data[tempvar==Inf|tempvar==-Inf,tempvar:=NA]
  temp = data[,list(N = sum(!is.na(tempvar)),
                    mean=mean(tempvar,na.rm=TRUE),
                    p10 = quantile(tempvar,prob=0.1,na.rm=TRUE),
                    median = quantile(tempvar,prob=0.5,na.rm=TRUE),
                    p90 = quantile(tempvar,prob=0.9,na.rm=TRUE),
                    p99 = quantile(tempvar,prob=0.99,na.rm=TRUE)),.SDcol=var]
  temp[,variable:=var_list_clean[i]]
  # if (i==1){
  #   temp[,sample:="Full Sample"]
  # }else{
  #   temp[,sample:=" "]
  # }
  table1 = rbind(table1,temp)
  rm(temp)
  data[,tempvar:=NULL]
  
}

# for (i in 1:length(var_list)){
#   var = var_list[i]
#   est_sample[,tempvar:=.SD,.SDcol=var]
#   est_sample[tempvar==Inf|tempvar==-Inf,tempvar:=NA]
#   temp = est_sample[,list(mean=mean(tempvar,na.rm=TRUE),
#                     p10 = quantile(tempvar,prob=0.1,na.rm=TRUE),
#                     median = quantile(tempvar,prob=0.5,na.rm=TRUE),
#                     p90 = quantile(tempvar,prob=0.9,na.rm=TRUE),
#                     p99 = quantile(tempvar,prob=0.99,na.rm=TRUE)),.SDcol=var]
#   temp[,variable:=var_list_clean[i]]
#   # if (i==1){
#   #   temp[,sample:="Estimation Sample"]
#   # }else{
#   #   temp[,sample:=" "]
#   #   }
#   table1 = rbind(table1,temp)
#   rm(temp)
#   est_sample[,tempvar:=NULL]
#   
# }
table1 = as.data.frame(table1)
table1 = table1[,c("variable","N", "mean","p10","median","p90","p99")]

print.xtable(xtable(table1),include.rownames=FALSE)


##### Correlation Within Banks #####
vars = c("deposit_market_share","consumer_market_share","commercial_market_share",
         "insurance_market_share","investment_market_share")

corr_est_banks = matrix(0,nrow=length(vars),ncol=length(vars))
rownames(corr_est_banks) = c("Deposits","Consumer Loans","Commercial Loans","Insurance","Investment")
colnames(corr_est_banks) = c("Deposits","Consumer Loans","Commercial Loans","Insurance","Investment")

for (i in 1:length(vars)){
  for (j in 1:i){
    data[,tempvar_i:=.SD,.SDcol=vars[i]]
    data[,tempvar_j:=.SD,.SDcol=vars[j]]
    c = data[!is.na(tempvar_i)&!is.na(tempvar_j),cor(tempvar_i,tempvar_j)]
    corr_est_banks[j,i] = c
    corr_est_banks[i,j] = c
  }
}

print.xtable(xtable(corr_est_banks))
