#!/usr/bin/env Rscript

# ARIS4C006 future-exposure falsification model.
# This is a post-unlock robustness diagnostic, not an alternative primary model.

args <- commandArgs(trailingOnly=TRUE)
get_arg <- function(flag) {
  i <- match(flag,args)
  if (is.na(i) || i == length(args)) stop(paste("missing",flag))
  args[[i+1]]
}
input_csv <- get_arg("--input")
outdir <- get_arg("--outdir")

verify_out <- system2("python",c("code/31_verify_prereg_lock.py","--require-unlock"),stdout=TRUE,stderr=TRUE)
st <- attr(verify_out,"status")
if (!is.null(st) && st != 0) stop(paste(c("LOCKED/INVALID PREREG STATE",verify_out),collapse="\n"))

if (!requireNamespace("fixest",quietly=TRUE)) stop("fixest required")
if (!requireNamespace("jsonlite",quietly=TRUE)) stop("jsonlite required")

d <- read.csv(input_csv,stringsAsFactors=FALSE,check.names=FALSE)
required <- c("listed_position_norm","rel_alpha_rank","future_loao_exposure",
              "work_id","canonical_author_id","field_year_cluster")
miss <- setdiff(required,names(d)); if(length(miss)) stop(paste("missing:",paste(miss,collapse=", ")))
if(nrow(d)==0) stop("empty future placebo frame")

fit <- fixest::feols(
  listed_position_norm ~ rel_alpha_rank + rel_alpha_rank:future_loao_exposure | work_id,
  data=d,
  vcov=~canonical_author_id + work_id + field_year_cluster
)
term <- "rel_alpha_rank:future_loao_exposure"
co <- coef(fit); se <- fixest::se(fit)
if(!term %in% names(co)) stop("future placebo interaction missing")
b <- unname(co[[term]]); s <- unname(se[[term]])
z <- b/s; p <- 2*pnorm(abs(z),lower.tail=FALSE)
res <- data.frame(
  analysis="future_exposure_placebo",
  term=term,estimate=b,std_error=s,
  conf_low=b-1.959963984540054*s,
  conf_high=b+1.959963984540054*s,
  p_value_raw=p,
  rows=nrow(d),
  works=length(unique(d$work_id)),
  stringsAsFactors=FALSE
)
dir.create(outdir,recursive=TRUE,showWarnings=FALSE)
write.csv(res,file.path(outdir,"future_exposure_placebo.csv"),row.names=FALSE)
manifest <- list(
  script="41_future_exposure_placebo.R",
  prereg_integrity_verified=TRUE,
  model="listed_position_norm ~ rel_alpha_rank + rel_alpha_rank:future_loao_exposure | work_id",
  vcov="three-way clustered: canonical_author_id + work_id + field_year_cluster",
  interpretation="falsification/proxy diagnostic only; persistent field regimes can make future exposure correlate with prior outcomes",
  result=unname(split(res,seq_len(nrow(res))))
)
jsonlite::write_json(manifest,file.path(outdir,"manifest.json"),pretty=TRUE,auto_unbox=TRUE)
print(res)
