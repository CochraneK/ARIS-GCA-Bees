#!/usr/bin/env Rscript

# Frozen ARIS4C006 secondary-family multiplicity adjustment.
# H1 is not part of this family. H2 + H3 receive Holm FWER correction when
# H3 passes the frozen structural gate and is estimable.

args <- commandArgs(trailingOnly=TRUE)
get_arg <- function(flag) {
  i <- match(flag,args)
  if (is.na(i) || i == length(args)) stop(paste("missing",flag))
  args[[i+1]]
}
h12_path <- get_arg("--h1h2")
h3_path <- get_arg("--h3")
out_path <- get_arg("--out")

h12 <- read.csv(h12_path,stringsAsFactors=FALSE,check.names=FALSE)
h3 <- read.csv(h3_path,stringsAsFactors=FALSE,check.names=FALSE)

h2 <- h12[h12$estimand=="H2_beta2_first_listed",,drop=FALSE]
if (nrow(h2)!=1) stop("expected exactly one H2 row")
if (nrow(h3)!=1 || h3$estimand[[1]]!="H3_beta3_persistence5") stop("expected exactly one H3 row")

praw <- c(H2=h2$p_value_raw[[1]],H3=h3$p_value_raw[[1]])
padj <- p.adjust(praw,method="holm")
out <- data.frame(
  estimand=c("H2_beta2_first_listed","H3_beta3_persistence5"),
  p_value_raw=unname(praw),
  p_value_holm=unname(padj),
  secondary_family_size=2,
  method="Holm",
  stringsAsFactors=FALSE
)
dir.create(dirname(out_path),recursive=TRUE,showWarnings=FALSE)
write.csv(out,out_path,row.names=FALSE)
print(out)
