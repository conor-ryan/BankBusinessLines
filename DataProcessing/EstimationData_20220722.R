rm(list=ls())
library(data.table)
library(ggplot2)
library(stargazer)
# library(ivreg)
setwd("G:/Shared drives/BankBusinessLines")

#### Read in Data ####
data = as.data.table(read.csv("Data/filtered_data.csv"))
data[,date:=as.Date(date)]

vars= names(data)
## Switch NA to 0
for (v in vars){
  data[,temp:=.SD,.SDcol=v]
  data[is.na(temp),c(v):=0]
  data[,temp:=NULL]
}



## Log Price Variables
data[,log_p_deposit:=deposits_p] # Not actually the log price for deposits... 
data[,log_p_propundwrt:=prop_underwriting_p]
data[,log_p_lifeundwrt:=life_underwriting_p]
data[,log_p_annuity:=annuity_p]
data[,log_p_inv:=investment_p]

## Log Quantity Variables
data[,log_q_deposit:=log(deposits_q)]
data[,log_q_propundwrt:=log(prop_underwriting_q)]
data[,log_q_lifeundwrt:=log(life_underwriting_q)]
data[,log_q_annuity:=log(annuity_q)]
data[,log_q_inv:=log(investment_q)]

## Product Offered Flag
data[log_p_deposit==-Inf|log_q_deposit==-Inf|is.na(log_p_deposit)|is.na(log_q_deposit),log_p_deposit:=0]
data[log_p_propundwrt==-Inf|log_q_propundwrt==-Inf|is.na(log_p_propundwrt)|is.na(log_q_propundwrt),log_p_propundwrt:=0]
data[log_p_lifeundwrt==-Inf|log_q_lifeundwrt==-Inf|is.na(log_p_lifeundwrt)|is.na(log_q_lifeundwrt),log_p_lifeundwrt:=0]
data[log_p_annuity==-Inf|log_q_annuity==-Inf|is.na(log_p_annuity)|is.na(log_q_annuity),log_p_annuity:=0]
data[log_p_inv==-Inf|log_q_inv==-Inf|is.na(log_p_inv)|is.na(log_q_inv),log_p_inv:=0]

data[log_p_deposit==-Inf|log_q_deposit==-Inf|is.na(log_p_deposit)|is.na(log_q_deposit),log_q_deposit:=0]
data[log_p_propundwrt==-Inf|log_q_propundwrt==-Inf|is.na(log_p_propundwrt)|is.na(log_q_propundwrt),log_q_propundwrt:=0]
data[log_p_lifeundwrt==-Inf|log_q_lifeundwrt==-Inf|is.na(log_p_lifeundwrt)|is.na(log_q_lifeundwrt),log_q_lifeundwrt:=0]
data[log_p_annuity==-Inf|log_q_annuity==-Inf|is.na(log_p_annuity)|is.na(log_q_annuity),log_q_annuity:=0]
data[log_p_inv==-Inf|log_q_inv==-Inf|is.na(log_p_inv)|is.na(log_q_inv),log_q_inv:=0]

data[,flag_deposit:=as.numeric(log_p_deposit==0&log_q_deposit==0)]
data[,flag_propundwrt:=as.numeric(log_p_propundwrt==0&log_q_propundwrt==0)]
data[,flag_lifeundwrt:=as.numeric(log_p_lifeundwrt==0&log_q_lifeundwrt==0)]
data[,flag_annuity:=as.numeric(log_p_annuity==0&log_q_annuity==0)]
data[,flag_inv:=as.numeric(log_p_inv==0&log_q_inv==0)]

## Cost Dependent Variable
data[,revenue_on_assets:=traditional_revenue+treasury_revenue+lease_nonint_revenue]
data[,cost_dep_var:=(Expense-revenue_on_assets)/1e6]

##Revenue Variables
data[,rev_deposit_tilde:=deposits_p*Assets/1e9]
data[,rev_propundwrt:=prop_underwriting_revenue/1e6]
data[,rev_lifeundwrt:=life_underwriting_revenue/1e6]
data[,rev_annuity:=annuity_revenue/1e6]
data[,rev_inv:=investment_revenue/1e6]



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
data[,bankFactor:=as.factor(Bank_ID)]
data[,dateFactor:=as.factor(date)]

data = data[,.SD,.SDcols=names(data)[grepl("rev_|log_|flag_|cost_dep_var|FEDFUNDS|VIX|bankFactor|dateFactor",names(data))]]


f = as.formula(paste("~-1+",paste(names(data),collapse="+")))

X = model.matrix(f,data=data)
save(X,file="Data/GMMSample.RData")
write.csv(X,file="Data/GMMSample.csv",row.names=FALSE)

labels = colSums(X[X[,'flag_deposit']==0,])
paste(names(labels)[labels>0],collapse = "' , '")

labels = colSums(X[X[,'flag_propundwrt']==0,])
paste(names(labels)[labels>0],collapse = "' , '")

labels = colSums(X[X[,'flag_lifeundwrt']==0,])
paste(names(labels)[labels>0],collapse = "' , '")

labels = colSums(X[X[,'flag_annuity']==0,])
paste(names(labels)[labels>0],collapse = "' , '")

labels = colSums(X[X[,'flag_inv']==0,])
paste(names(labels)[labels>0],collapse = "' , '")



test = X[X[,'flag_propundwrt']==0,c('log_p_propundwrt',
            'bankFactor1036967' , 'bankFactor1037003' , 'bankFactor1068191' , 'bankFactor1070345' ,
            'bankFactor1073757' , 'bankFactor1074156' , 'bankFactor1120754' , 'bankFactor1245415' , 'bankFactor1275216' ,
            'bankFactor1562859' , 'bankFactor1951350' , 'bankFactor2380443' , 'bankFactor3242838' , 'bankFactor3587146' ,
            'bankFactor5006575' ,
             'dateFactor2016-09-30' , 'dateFactor2016-12-31' , 'dateFactor2017-03-31' ,
            'dateFactor2017-06-30' , 'dateFactor2017-09-30' , 'dateFactor2017-12-31' , 'dateFactor2018-03-31' ,
            'dateFactor2018-06-30' , 'dateFactor2018-09-30' , 'dateFactor2018-12-31' , 'dateFactor2019-03-31' ,
            'dateFactor2019-06-30' , 'dateFactor2019-09-30' , 'dateFactor2019-12-31' , 'dateFactor2020-03-31' ,
            'dateFactor2020-06-30' , 'dateFactor2020-09-30' , 'dateFactor2020-12-31')]

test = t(test)%*%test

E = eigen(test)

test = X[,c('rev_deposit_tilde','rev_propundwrt','rev_lifeundwrt','rev_annuity','rev_inv')]

test = t(test)%*%test

E = eigen(test)




fs = data[,lm(log_p_deposit~-1+FEDFUNDS + bankFactor + dateFactor)]
data[,iv_var:=predict(fs)]
res = data[,lm(log_q_deposit~-1+iv_var+bankFactor+dateFactor)]
summary(res)
length(res$coefficients)










# data[,return_on_assets:=(Net_Income+Expense)/Assets]

data[,product_revenue:=prop_underwriting_revenue+life_underwriting_revenue+annuity_revenue+investment_revenue]

data[,return_on_assets:=revenue_on_assets/(traditional_q+treasury_q)]


data[,total_revenue_captured:=product_revenue+revenue_on_assets+deposit_revenue]
data[,Expense_adj:=total_revenue_captured*Expense/(Net_Income+Expense)]


data[,ret_mean:=mean(return_on_assets),by="Bank_ID"]
data[,asset_rev_adj:=(traditional_q+treasury_q)*(return_on_assets+deposits_p)]

data[,asset_exp_adj:=(traditional_q+treasury_q)*(deposits_p)]

reg = data[,lm(Expense~asset_exp_adj+prop_underwriting_revenue+life_underwriting_revenue +annuity_revenue+investment_revenue + as.factor(Bank_ID) + as.factor(date)) ]
summary(reg)


reg=data[,lm(dep_var~asset_exp_adj +annuity_revenue+investment_revenue) ]
summary(reg)

data[,pred_expenses:=predict(reg)]

data[,cost_pred:=(return_on_assets-deposits_p)*(1-1/4)*Assets_adj]# + annuity_p*(1-1/4)*annuity_q+investment_p*(1-1/4)*investment_q]



data[,t:=as.numeric(date)]
data[,t2:=t^2]
data[,summary(lm(return_on_assets~as.factor(Bank_ID)+t+t2))]
data[,summary(lm(return_on_assets~as.factor(date)))]


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
