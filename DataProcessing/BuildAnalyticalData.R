rm(list=ls())
library(data.table)
library(ggplot2)
library(stargazer)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
data = as.data.table(read.csv("Data/filtered_data.csv"))
data[,date:=as.Date(date)]
data[,year:=as.numeric(format(date,"%Y"))]
data[,X:=NULL]


## Bank Characteristics 

data[,salary_per_asset:=salaries/total_assets]
data[,premises_per_asset:=premises_cost/total_assets]
data[,other_per_asset:=other_cost/total_assets]
data[,total_per_asset:=total_cost/total_assets]

# data[,insurance_price:=insurance_price*100]
# data[,investment_price:=investment_price*100]

#Drop the banks(quarters) that report 0 assets or 0 costs
data = data[!is.na(total_assets)&total_assets>0]
data = data[!is.na(total_cost)&total_cost>0]

## Market Share as Percentage
data[,deposit_market_share:=deposit_market_share/100]
data[,consumer_market_share:=consumer_market_share/100]
data[,commercial_market_share:=commercial_market_share/100]
data[,insurance_market_share:=insurance_market_share/100]


# ### By Quarter Quantities
# byQuarter = data[insurance_assets>0,list(total_assets = sum(total_assets,na.rm=TRUE)/1e6,
#                                          total_deposits=sum(total_deposits,na.rm=TRUE)/1e6,
#                                          new_cons_loans=sum(new_consumer_loans,na.rm=TRUE)/1e6,
#                                          new_comm_loans=sum(new_commercial_loans,na.rm=TRUE)/1e6,
#                                          insured_assets=sum(insurance_assets,na.rm=TRUE)/1e6),
#                  by=c("date")]



#### Selection: Top 20, in any market in any quarter #####
firms = c()
for (var in c("deposit_market_share","consumer_market_share","commercial_market_share","insurance_market_share","investment_market_share")){
  data[,share:=.SD,.SDcol=var]
  data[,temp_rank:=rank(-share,ties.method="average"),by="date"]
  firms_prod = data[share>0&temp_rank<=30,unique(RSSD9001)]
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

vix = as.data.table(read.csv("Data/OtherData/VIXCLS.csv"))
vix[,DATE:=as.Date(DATE,format="%m/%d/%y")]
macro = merge(vix,ffrate,by="DATE",all=TRUE)

## Need to convert beginning of quarter dates to end of quarter dates
quarter_map = macro[,"DATE"]
setkey(quarter_map,DATE)
quarter_map[,index:=1:nrow(quarter_map)]
quarter_ends = copy(quarter_map)
quarter_ends[,index:=index-1]
names(quarter_ends) = c("date_end","index_end")
quarter_map = merge(quarter_map,quarter_ends,by.x="index",by.y="index_end")
quarter_map[,date_end:=date_end-1]
quarter_map[,index:=NULL]

## Merge FF rate data into main data
macro = merge(macro,quarter_map,by="DATE")
data = merge(data,macro[,c("date_end","FEDFUNDS","VIX")],by.x="date",by.y="date_end",all.x=TRUE)


#### Some additional Variable Edits ####
data[,bankFactor:=as.factor(RSSD9001)]
data[,dateFactor:=as.factor(date)]


save(data,file="Data/FullSample.RData")
write.csv(data,file="Data/FullSample.csv")

data[,r_dep:=deposit_rate]
data[,r_cons:=consumer_rate]
data[,r_comm:=commercial_rate]
data[,p_inv:=investment_price]
data[,p_ins:=insurance_price]

data[,q_dep:=total_deposits]
# data[,q_cons:=new_consumer_loans]
# data[,q_comm:=new_commercial_loans]
data[,q_cons:=consumer_loans]
data[,q_comm:=commercial_loans]
data[,q_inv:=investment_quantity]
data[,q_ins:=insurance_assets]

data[,s_dep:=deposit_market_share]
data[,s_cons:=consumer_market_share]
data[,s_comm:=commercial_market_share]
data[,s_inv:=investment_market_share]
data[,s_ins:=insurance_market_share]

data[,L_comm:=commercial_loans]
data[,L_cons:=consumer_loans]


#### Exploration of Identification Issues
# data[,total_cost:=0.2*total_cost]


#### GMM Sample ####
covariates = c("bankFactor","dateFactor","branch_count","geo_coverage","salary_per_asset","premises_per_asset")
instruments = c("FEDFUNDS")
gmm_sample = data[date>"2016-06-01",.SD,.SDcols = c("date","RSSD9001","total_cost",names(data)[grepl("^(r|p|q|s|L)_",names(data))],covariates,instruments)]

## Need to verify that this assumption is okay 
gmm_sample[is.na(branch_count),branch_count:=0]
gmm_sample[is.na(geo_coverage),geo_coverage:=0]


for (var in c("dep","cons","comm","inv","ins")){
  qvar = paste("q",var,sep="_")
  svar = paste("s",var,sep="_")
  rvar = paste("r",var,sep="_")
  pvar = paste("p",var,sep="_")
  gmm_sample[,temp:=.SD,.SDcol=qvar]
  gmm_sample[is.na(temp),c(qvar):=0]
  gmm_sample[is.na(temp),c(svar):=0]
  
  if (var%in%c("inv","ins")){
    gmm_sample[is.na(temp)|temp==0,c(pvar):=0]
  }else{
    gmm_sample[is.na(temp)|temp==0,c(rvar):=0]
  }
  gmm_sample[,temp:=NULL]
}

## Drop a few observations where insurance price isn't defined. Why isn't it defined? Also an issue with consumer rates
gmm_sample = gmm_sample[!is.na(p_ins)&!is.na(r_cons)]


## Drop banks that don't have any deposits. Going to need to figure out how they fit in.
gmm_sample = gmm_sample[q_dep>0]

## Create Outside option Share for Deposits
gmm_sample[,s_dep_0:=1-sum(s_dep),by="date"]

### Set up for Regression
gmm_sample[,bankFactor:=as.character(RSSD9001)]
gmm_sample[,dateFactor:=as.character(date)]

# Exogenous Covariates
X = model.matrix(~r_dep+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset,data=gmm_sample)
X_wo_r = model.matrix(~bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset,data=gmm_sample)
test = solve(t(X)%*%X)




# Instruments
Z = model.matrix(~-1+bankFactor*FEDFUNDS+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset,data=gmm_sample)
C = cor(Z)
diag(C) = 0.0
which(C>0.99,arr.ind=TRUE)

Z = Z[,-which(colnames(Z)%in%c("bankFactor1032473:FEDFUNDS","bankFactor2648693:FEDFUNDS",
                               "bankFactor1070804:FEDFUNDS","bankFactor5005998:FEDFUNDS",
                               "dateFactor2020-09-30"))] # Drop fixed effects for single period banks
test = solve(t(Z)%*%Z)

## Check regression equation
Y = gmm_sample[,r_dep]
# beta = solve(t(Z)%*%Z)%*%t(Y%*%Z)
# residuals = Y - Z%*%beta

# ## IV Solution for Simulation Testing
Y = gmm_sample[,log(s_dep) - log(s_dep_0)]
Sxy = Y%*%Z
Sxz = t(Z)%*%X
Szz = t(Z)%*%Z

beta = solve(t(Sxz)%*%solve(Szz)%*%Sxz)%*%t(Sxz)%*%solve(Szz)%*%t(Sxy)
residuals = Y - X%*%beta
moments = t(residuals)%*%Z
moments%*%solve(Szz)%*%t(moments)
# 
gmm_sample[,dep_var:=log(s_dep) - log(s_dep_0)]
dep_iv = gmm_sample[,lm(r_dep~+bankFactor*FEDFUNDS+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)]
gmm_sample[,deposit_rate_iv:=predict(dep_iv)]
dep_res = gmm_sample[,lm(dep_var~deposit_rate_iv+bankFactor+dateFactor+branch_count+geo_coverage+salary_per_asset+premises_per_asset)]
summary(dep_res)
# 
# ## IV Moments at Solution
# mom = t(dep_res$residuals%*%Z)

gmm_sample[,c(covariates,instruments,"deposit_rate_iv"):=NULL]


save(gmm_sample,file="Data/GMMSample.RData")
write.csv(gmm_sample,file="Data/GMMSample.csv",row.names=FALSE)
write.csv(X_wo_r,file="Data/ExogenousDemandCovariates.csv",row.names=FALSE)
write.csv(Z,file="Data/DemandInstruments.csv",row.names=FALSE)

gmm_sample[,revenue:=r_cons*L_cons + r_comm*L_comm + p_inv*q_inv + p_ins*q_ins-r_dep*q_dep]
gmm_sample[,margin:=(revenue-total_cost)/total_cost]
gmm_sample[,plot(q_dep,margin)]
