rm(list=ls())
library(data.table)
library(ggplot2)
library(stargazer)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
data = as.data.table(read.csv("Data/filtered_data.csv"))
vars= names(data)
## Switch NA to 0
for (v in vars){
  data[,temp:=.SD,.SDcol=v]
  data[is.na(temp),c(v):=0]
  data[,temp:=NULL]
}


# data[,return_on_assets:=(Net_Income+Expense)/Assets]

data[,product_revenue:=prop_underwriting_revenue+life_underwriting_revenue+annuity_revenue+investment_revenue]
data[,revenue_on_assets:=traditional_revenue+treasury_revenue+lease_nonint_revenue]
data[,return_on_assets:=revenue_on_assets/(traditional_q+treasury_q)]


data[,total_revenue_captured:=product_revenue+revenue_on_assets+deposit_revenue]
data[,Expense_adj:=total_revenue_captured-Net_Income]




data[,test:=total_revenue_captured/(Net_Income+Expense)]
data[,summary(test)]
data[,hist(test)]

data[,test2:=othernonint_revenue/total_revenue_captured]
data[,summary(test2)]








### Construct Market Shares
q_vars = names(data)[grepl("_q",names(data))]

for (v in q_vars){
  mkt_var = gsub("_q","_sh",v)
  data[,c(mkt_var):=.SD/sum(.SD,na.rm=TRUE),by="date",.SDcol=v]
}














### Investigative Plots

for (v in q_vars){
  mkt_var = gsub("_q","_sh",v)
  p_var = gsub("_q","_p",v)
  data[,share_temp:=.SD,.SDcol=mkt_var]
  data[,q_temp:=.SD,.SDcol=v]
  data[,p_temp:=.SD,.SDcol=p_var]
  
  print(v)
  print(data[share_temp>0.02,sum(share_temp),by="date"])
  plot = ggplot(data[share_temp>0.01]) + aes(x=q_temp,y=p_temp) + geom_point() + ggtitle(v)
  print(plot)
  
  
  data[,share_temp:=NULL]
  data[,q_temp:=NULL]
  data[,p_temp:=NULL]
}


data[deposits_sh>1e8,plot(deposits_q,deposits_p)]
data[,plot(prop_underwriting_q,prop_underwriting_p)]


fry = as.data.table(read.csv("Data/frdata.csv"))

### Check Other Non Interest Revenue
vars =c("TEXT8562","BHCK8562")


df = fry[RSSD9001==1070345,.SD,.SDcols=c("RSSD9001","RSSD9999",vars)]


other = df[,list(total_income=sum(BHCK8562,na.rm=TRUE)),by="TEXT8562"]
setkey(other,total_income)

data = merge(data,df,by.x=c("Bank_ID","date"),by.y=c("RSSD9001","RSSD9999"),all.x=TRUE)

### Insurance Income Variables
## Annuity Sales - C887
## Underwriting Revenue - C386
### -> Subset of this revenue comes from premiums: C243
## Life Insurance Value Appreciation (?) - C014
## Other Revenue (Premiums included?) - C387


## Annuity and Mutual Fund Sale & Servicing -  8431
## Credit-related insurance premiums - C242


### Insurance Quantity Variables
## Property/Casuality assets underwritten - C244
## Life and Health assets underwritten - C248
## Life Insurance Assets - K201, K202, K270

vars =c("BHCKC887","BHCKC386","BHCKC014","BHCKC387","BHCK4070","BHCKB570", "BHCK8431","BHCKC242", "BHCKC243","BHCKB983","BHCKB988","BHCKC244","BHCKC245","BHCKC246","BHCKC247","BHCKB992","BHCKC248","BHCKC249","BHCKC250", "BHCKK201","BHCKK202","BHCKK270")


df = fry[RSSD9999%in%c("20160331","20170331","20180331","20190331"),.SD,.SDcols=c("RSSD9001","RSSD9999",vars)]



df[,life_ins_assets:=BHCKK201+BHCKK202+BHCKK270+BHCKB570]
df[,life_ins_sh:=life_ins_assets/sum(life_ins_assets)]


df[,life_ins_uw_sh:=BHCKC249/sum(BHCKC249)]

df[,prop_ins_uw_sh:=BHCKC244/sum(BHCKC244)]
df[,tot_undw_netincome:=BHCKC246+BHCKC250]

df[,income_meas1:=BHCKC887+BHCKC014+BHCK4070+BHCKC386+BHCK8431-BHCKB983]
df[,income_meas1:=BHCK4070+BHCKC014+BHCKC887+BHCKC242+BHCKC243+BHCK8431-BHCKB983]
df[,inc_to_asset:=income_meas1/life_ins_assets]


setkey(df,life_ins_sh)
df[life_ins_sh>0.005]
df[,plot(life_ins_assets,income_meas1)]
df[,cor(life_ins_assets,income_meas1)]



test = df[BHCKC248>10*BHCKC244]
setkey(test,ins_assets)



df[,plot(ins_assets,ins_revenue)]

df[,plot(BHCKC248 ,BHCKC243 )]


#### Property and Life Insurance Panel for Big Insurers
vars =c("BHCKC244","BHCKC245","BHCKC246","BHCKC248","BHCKC249","BHCKC250")


df = fry[RSSD9999%in%c("20160331","20170331","20180331","20190331"),.SD,.SDcols=c("RSSD9001","RSSD9999",vars)]
## Switch NA to 0
for (v in vars){
  df[,temp:=.SD,.SDcol=v]
  df[is.na(temp),c(v):=0]
  df[,temp:=NULL]
}

df[,life_ins_uw_sh:=BHCKC249/sum(BHCKC249),by="RSSD9999"]
df[,prop_ins_uw_sh:=BHCKC244/sum(BHCKC244),by="RSSD9999"]


df[,life_eq_prem:=BHCKC250 /BHCKC249 ]
df[,life_as_prem:=BHCKC250 /BHCKC248 ]
df[,prop_eq_prem:=BHCKC246 /BHCKC245 ]
df[,prop_as_prem:=BHCKC246 /BHCKC244 ]

df = df[RSSD9001%in%c(1120754 ,1447376,1951350 ,1025309,1562859 , 1098303,1073757,1039502,1025309)]

setkey(df,RSSD9001,RSSD9999)
