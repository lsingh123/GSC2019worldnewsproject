library(venneuler)
ia = read.csv("data/ia_sources.csv"); head(ia)
mc = read.csv("data/mc_sources.csv"); head(mc)
wd = read.csv("data/wd_sources.csv")
ink = read.csv("data/inkdrop_sources.csv")
ia = ia$URL
m <- as.matrix(data.frame(C1=c1,C2=c2,C3=c3,C4=c4))
