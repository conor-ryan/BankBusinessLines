loan_demand <- function(r){
  util = exp(5-50*r)
  dem = util/(20+util)
  return(dem)
}

deposit_demand <- function(r){
  util = exp(1 + 200*r)
  dem = util/(20+util)
  return(dem)
}

### Demand for Loans
x = seq(0,0.2,0.01)
y = lapply(x,FUN=loan_demand)
plot(x,y)

### Demand for Deposits
x = seq(0,0.05,0.002)
y = lapply(x,FUN=deposit_demand)
plot(x,y)



mcl = 0.002
mcd = 0.001

profit = function(rl,rd){
  sl = loan_demand(rl)
  sd = deposit_demand(rd)
  sl = min(sl,sd)
  Pi = sl*(rl-mcl) - sd*(rd+mcd)
  return(Pi)
}


### Best Response for Loan Interest Rate
x = seq(0,0.3,0.01)

y = lapply(x,FUN=function(x){profit(x,0.01)})

plot(x,y)




### Best Response for Deposit Interest Rate
x = seq(-0.1,0.1,0.01)

y = lapply(x,FUN=function(x){profit(0.05,x)})

plot(x,y)


#### Maximize Profit ####
obj = function(vec){
  return(-profit(vec[1],vec[2]))
}

optim(c(0.05,0.01),obj)
