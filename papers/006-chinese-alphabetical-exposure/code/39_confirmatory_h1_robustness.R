#!/usr/bin/env Rscript

# ARIS4C006 post-unlock robustness/falsification runner for frozen H1.
# Does not alter the preregistered primary estimand.

args <- commandArgs(trailingOnly=TRUE)
get_arg <- function(flag) {
  i <- match(flag,args)
  if (is.na(i) || i == length(args)) stop(paste("missing",flag))
  args[[i+1]]
}
input_csv <- get_arg("--input")
rolling_csv <- get_arg("--rolling")
outdir <- get_arg("--outdir")

verify_out <- system2("python",c("code/31_verify_prereg_lock.py","--require-unlock"),stdout=TRUE,stderr=TRUE)
st <- attr(verify_out,"status")
if (!is.null(st) && st != 0) stop(paste(c("LOCKED/INVALID PREREG STATE",verify_out),collapse="\n"))

if (!requireNamespace("fixest",quietly=TRUE)) stop("fixest required")
if (!requireNamespace("jsonlite",quietly=TRUE)) stop("jsonlite required")

d <- read.csv(input_csv,stringsAsFactors=FALSE,check.names=FALSE)
roll <- read.csv(rolling_csv,stringsAsFactors=FALSE,check.names=FALSE)
required <- c("listed_position_norm","rel_alpha_rank","loao_exposure","loao_3plus_exposure",
              "team_size","work_id","canonical_author_id","field_year_cluster","field_id","year")
miss <- setdiff(required,names(d)); if(length(miss)) stop(paste("missing:",paste(miss,collapse=", ")))

roll2 <- roll[,c("field_id","target_year","excess_alpha")]
names(roll2) <- c("field_id","year","field_raw_exposure")
d <- merge(d,roll2,by=c("field_id","year"),all.x=TRUE,sort=FALSE)

vc <- ~canonical_author_id + work_id + field_year_cluster
term_primary <- "rel_alpha_rank:loao_exposure"
term_3 <- "rel_alpha_rank:loao_3plus_exposure"

extract <- function(fit,label,term,nrows,nworks) {
  co <- coef(fit); se <- fixest::se(fit)
  if(!term %in% names(co)) stop(paste(label,"term missing"))
  b <- unname(co[[term]]); s <- unname(se[[term]])
  z <- b/s; p <- 2*pnorm(abs(z),lower.tail=FALSE)
  data.frame(
    analysis=label,rows=nrows,works=nworks,term=term,
    estimate=b,std_error=s,conf_low=b-1.959963984540054*s,
    conf_high=b+1.959963984540054*s,p_value_raw=p,
    stringsAsFactors=FALSE
  )
}

fit_interaction <- function(dd,label,exposure_var) {
  if(nrow(dd)==0) stop(paste(label,"empty"))
  form <- as.formula(paste0("listed_position_norm ~ rel_alpha_rank + rel_alpha_rank:",exposure_var," | work_id"))
  fit <- fixest::feols(form,data=dd,vcov=vc)
  term <- paste0("rel_alpha_rank:",exposure_var)
  extract(fit,label,term,nrow(dd),length(unique(dd$work_id)))
}

res <- list()
res[[1]] <- fit_interaction(d,"primary_reference","loao_exposure")
res[[2]] <- fit_interaction(d[d$team_size>=3,],"focal_team_3plus","loao_exposure")
d3 <- d[!is.na(d$loao_3plus_exposure) & d$loao_3plus_D>=50,]
res[[3]] <- fit_interaction(d3,"convention_exposure_3plus","loao_3plus_exposure")
d33 <- d3[d3$team_size>=3,]
res[[4]] <- fit_interaction(d33,"focal_team_3plus_and_convention_3plus","loao_3plus_exposure")

# Low-alphabetization negative control: theoretical zero of ExcessAlpha means
# no excess alphabetical ordering above the chance benchmark.
low <- d[!is.na(d$field_raw_exposure) & d$field_raw_exposure<=0,]
fit_low <- fixest::feols(
  listed_position_norm ~ rel_alpha_rank | work_id,
  data=low, vcov=vc
)
res[[5]] <- extract(
  fit_low,"low_alphabetization_context_slope","rel_alpha_rank",
  nrow(low),length(unique(low$work_id))
)

out <- do.call(rbind,res)
dir.create(outdir,recursive=TRUE,showWarnings=FALSE)
write.csv(out,file.path(outdir,"h1_robustness.csv"),row.names=FALSE)
manifest <- list(
  script="39_confirmatory_h1_robustness.R",
  prereg_integrity_verified=TRUE,
  low_alphabetization_definition="frozen chance-centered diagnostic: field-year raw ExcessAlpha <= 0",
  primary_result_not_redefined=TRUE,
  rows_primary=nrow(d),
  results=unname(split(out,seq_len(nrow(out))))
)
jsonlite::write_json(manifest,file.path(outdir,"manifest.json"),pretty=TRUE,auto_unbox=TRUE)
print(out)
