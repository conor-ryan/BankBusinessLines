rm(list=ls())
library(data.table)
library(ggplot2)
setwd("G:/Shared drives/BankBusinessLines")

#### Relationship Data #### (https://www.ffiec.gov/npw/FinancialReport/DataDownload)

df = as.data.table(read.csv("Data/MarketStructure/CSV_RELATIONSHIPS.CSV"))



# ## Recursive Ownerships that are real data, but we can probably ignore
# df = df[!(ID_RSSD_OFFSPRING==4906584&X.ID_RSSD_PARENT==4901981)]


## Check All Recursive Relationships 
df[,Forward:=paste(X.ID_RSSD_PARENT,ID_RSSD_OFFSPRING,sep="_")]
df[,Reverse:=paste(ID_RSSD_OFFSPRING,X.ID_RSSD_PARENT,sep="_")]
df[,rel_check_id:=ID_RSSD_OFFSPRING+X.ID_RSSD_PARENT]

## Delete all recursive relationships, maybe won't lose much.

df = df[!(Forward%in%df$Reverse)]

# Reducing the mapping to only the controlling shares seems to leave out some important links. 
# df = df[CTRL_IND==1] # Only Controlling Links
df = unique(df[,c("X.ID_RSSD_PARENT","ID_RSSD_OFFSPRING","DT_START","DT_END")])

names(df) = c("PARENT","OFFSPRING","DT_START","DT_END")
df[,linkID:=1:nrow(df)]

continuing_chains = nrow(df)
itr = 1
dfmap = copy(df)
names(dfmap) = c("PARENT","OFFSPRING_1","DT_START_last","DT_END_last","linkID_last")

df_temp = copy(df)
names(df_temp) = paste(names(df_temp),"new",sep="_")


dfmap = dfmap[!PARENT%in%dfmap$OFFSPRING]

## Allow 20 levels deep. There are cycles of recursive relationships that prevent it from converging
while (continuing_chains>0){
  
  
  dfmap = merge(dfmap,df_temp,by.x=paste("OFFSPRING",itr,sep="_"),by.y="PARENT_new",all.x=TRUE,allow.cartesian=TRUE)
  dfmap = dfmap[!( (DT_START_new>DT_END_last | DT_END_new<DT_START_last) & !is.na(OFFSPRING_new) ) ]
  dfmap[DT_END_new>DT_END_last,DT_END_new:=DT_END_last]
  dfmap[DT_START_new<DT_START_last,DT_START_new:=DT_START_last]
  dfmap[!is.na(OFFSPRING_new),linkage_new:= paste(linkID_last,linkID_new,sep="_")]
  
  ## Drop links that are going to be added in the next merge
  if (itr>1){
    dfmap = dfmap[!(!is.na(linkage_last) & linkage_last%in%linkage_new)]
  }
  
  
  ## Drop links that are recursive
  if (itr>=3){
  for (i in (itr-1):1){
    dfmap[,check:=.SD,.SDcol=paste("OFFSPRING",i,sep="_")]
    dfmap = dfmap[! (!is.na(OFFSPRING_new) & OFFSPRING_new==check)]
  }
  }
  
  continuing_chains = nrow(dfmap[!is.na(OFFSPRING_new)])
  unique_remaining_offspring = length(dfmap[!is.na(OFFSPRING_new),unique(OFFSPRING_new)])
  print(paste(continuing_chains,"continuing matches on iteration",itr))
  print(paste(unique_remaining_offspring,"continuing offspring on iteration",itr))
  
  
  names(dfmap) = gsub("_last",paste("_",itr,sep=""),names(dfmap))
  itr = itr + 1
  names(dfmap) = gsub("_new","_last",names(dfmap))
  names(dfmap) = gsub("OFFSPRING_last",paste("OFFSPRING",itr,sep="_"),names(dfmap))
  
}
dfmap[,c(paste("OFFSPRING",itr,sep="_")):=NULL]

itr = itr-1
dfmap[,c("DT_START_last","DT_END_last","linkID_last","linkage_last"):=NULL]
print(itr)
#### Collapse mapping down to map between lowest offspring and highest parent. 
map_cond = NULL
while(itr>1){
  itr = itr-1
  print(paste("Condensing at level",itr))
  cols = c("PARENT",paste(c("OFFSPRING","DT_START","DT_END"),itr,sep="_"))
  dfmap[,offspring_last:=.SD,.SDcol=paste("OFFSPRING",itr,sep="_")]
  map_temp = dfmap[!is.na(offspring_last),.SD,.SDcols=cols]
  names(map_temp) = c("PARENT","OFFSPRING","DT_START","DT_END")
  map_cond = rbind(map_cond,map_temp)
  dfmap[,offspring_last:=NULL]
}
map_cond = unique(map_cond)
save(map_cond,file="Data/MarketStructure/OrgStructure.rData")


#### Create Quarterly Mapping ####
data = as.data.table(read.csv("Data/frdata_refined.csv"))
data[,date:=as.Date(date)]
data[,datenum:=year(date)*10000+month(date)*100+30]

qtr_map = NULL
for (qtr in unique(data$datenum)){
  temp = map_cond[qtr>=DT_START&qtr<=DT_END,c("PARENT","OFFSPRING")]
  temp[,quarter:=qtr]
  qtr_map = rbind(qtr_map,temp)
}
qtr_map = unique(qtr_map)

qtr_map = qtr_map[!OFFSPRING%in%c(2568278)]
qtr_map = qtr_map[!OFFSPRING==3838857&quarter<20151101]
qtr_map = qtr_map[!OFFSPRING==3923614&quarter<20131101]
qtr_map= qtr_map[!(PARENT==2348470&quarter>20180813)]

save(qtr_map,file="Data/MarketStructure/OrgStructureByQuarter.rData")
write.csv(qtr_map,file="Data/MarketStructure/OrgStructureByQuarter.csv",row.names=FALSE)

