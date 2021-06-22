rm(list=ls())
library(data.table)
library(ggplot2)
setwd("G:/Shared drives/BankBusinessLines")



#### Combine CSV File List ####
files = list.files(path="Data/Branches/",pattern = ".csv")
data_full = NULL
for (f in files){
  print(f)
  temp = as.data.table(read.csv(paste("Data/Branches/",f,sep="")))
  names(temp) = toupper(names(temp))
  data_full = rbind(data_full,temp)
  rm(temp)
}
save(data_full,file="Data/Branches/AllBranchData.rData")
load(file="Data/Branches/AllBranchData.rData")
## A unique row is YEAR, branch id (BRNUM), and institution id (CERT)
## Holding Company IDs are RSSDHCR


#### Aggregate Branch Info up to County Level ####
data_full[,branch_count:=1] #Total Count
data_full[,branch_count_full_service:=as.numeric(BRSERTYP<20)] #Full Service Offices

load("Data/MarketStructure/OrgStructureByQuarter.rData")
data_full[,datenum:=YEAR*10000+0330]
data_full = merge(data_full,qtr_map,by.x=c("RSSDHCR","datenum"),by.y=c("OFFSPRING","quarter"),all.x=TRUE)
data_full[is.na(PARENT),PARENT:=RSSDHCR]
data_full[,datenum:=NULL]


branchByCounty = data_full[,lapply(.SD,FUN=sum),by=c("YEAR","PARENT","STNUMBR","CNTYNUMB"),.SDcol=c("branch_count","branch_count_full_service")]


#### Aggregate Nationally with geographic coverage ####
## Read in country 2010 populations
popData = as.data.table(read.csv("Data/OtherData/CountyPopulation_2010_2019.csv"))
popData = popData[COUNTY>0,c("STATE","COUNTY","CENSUS2010POP")] # Drop State Totals
total_population = popData[,sum(CENSUS2010POP)]

branchByCounty = merge(branchByCounty,popData[,c("STATE","COUNTY","CENSUS2010POP")],
                       by.x=c("STNUMBR","CNTYNUMB"),by.y=c("STATE","COUNTY"),all.x=TRUE)

# Sum missing matches, small number in Alaska and Virginia, otherwise outside the US (Guam, etc.)
# For now, ignore these for purposes of national coverage

## Nationally Aggregate, compute coverage
# Drop banks without a holding company
branches = branchByCounty[PARENT>0,lapply(.SD,FUN=sum,na.rm=TRUE),by=c("YEAR","PARENT"),.SDcols=c("branch_count","branch_count_full_service","CENSUS2010POP")]

branches[,geo_coverage:=CENSUS2010POP/total_population]
branches[,CENSUS2010POP:=NULL]
save(branches,file="Data/bankbranches.Rdata")
write.csv(branches,file="Data/bankbranches.csv",row.names=FALSE)

