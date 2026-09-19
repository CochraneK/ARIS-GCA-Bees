#!/usr/bin/env Rscript

# ARIS4C006 locked confirmatory H3 execution.
# Requires prereg lock + matching external unlock + paper status analysis/manuscript.

args <- commandArgs(trailingOnly=TRUE)
get_arg <- function(flag) {
  i <- match(flag, args)
  if (is.na(i) || i == length(args)) stop(paste("missing", flag))
  args[[i+1]]
}
input_csv <- get_arg("--input")
outdir <- get_arg("--outdir")

verify_out <- system2(
  "python",
  c("code/31_verify_prereg_lock.py","--require-unlock"),
  stdout=TRUE, stderr=TRUE
)
st <- attr(verify_out,"status")
if (!is.null(st) && st != 0) stop(paste(c("LOCKED/INVALID PREREG STATE",verify_out),collapse="\n"))

if (!requireNamespace("fixest", quietly=TRUE)) stop("fixest is required")
if (!requireNamespace("jsonlite", quietly=TRUE)) stop("jsonlite is required")

lock <- jsonlite::fromJSON(file.path("process","PREREGISTRATION_LOCK.json"))
spec <- jsonlite::fromJSON(file.path("process","ANALYSIS_SPEC.json"))

d <- read.csv(input_csv, stringsAsFactors=FALSE, check.names=FALSE)
required <- c(
  "persistence5","surname_initial_rank_norm","mean_early_exposure",
  "entry_year","entry_primary_field","entry_work_count","entry_field_year_cluster"
)
miss <- setdiff(required,names(d))
if (length(miss)) stop(paste("missing columns:",paste(miss,collapse=", ")))
if (nrow(d) == 0) stop("empty H3 frame")

# Spec integrity checks.
h3 <- spec$downstream_longitudinal$model
if (!identical(h3$primary_estimand,"beta3")) stop("spec drift: H3 primary estimand")
if (!identical(h3$entry_work_count_transform,"log1p")) stop("spec drift: H3 work-count transform")
if (!identical(h3$vcov_cluster,"entry_primary_field_x_entry_year")) stop("spec drift: H3 cluster")

d$entry_year <- as.factor(d$entry_year)
d$entry_primary_field <- as.factor(d$entry_primary_field)

fit <- fixest::feglm(
  persistence5 ~ surname_initial_rank_norm * mean_early_exposure + log1p(entry_work_count) |
    entry_year + entry_primary_field,
  data=d,
  family="binomial",
  vcov=~entry_field_year_cluster
)

term <- "surname_initial_rank_norm:mean_early_exposure"
co <- stats::coef(fit)
se <- fixest::se(fit)
if (!term %in% names(co)) stop("H3 interaction term missing")
b <- unname(co[[term]])
s <- unname(se[[term]])
z <- b/s
p <- 2*stats::pnorm(abs(z),lower.tail=FALSE)

res <- data.frame(
  estimand="H3_beta3_persistence5",
  term=term,
  estimate=b,
  std_error=s,
  conf_low=b-1.959963984540054*s,
  conf_high=b+1.959963984540054*s,
  p_value_raw=p,
  stringsAsFactors=FALSE
)

dir.create(outdir,recursive=TRUE,showWarnings=FALSE)
write.csv(res,file.path(outdir,"confirmatory_h3.csv"),row.names=FALSE)

manifest <- list(
  script="37_confirmatory_h3.R",
  prereg_lock_label=lock$lock_label,
  prereg_lock_sha256=lock$combined_sha256,
  confirmatory_unlock_verified=TRUE,
  rows=nrow(d),
  entry_years=length(unique(d$entry_year)),
  entry_fields=length(unique(d$entry_primary_field)),
  field_year_clusters=length(unique(d$entry_field_year_cluster)),
  model="logit Persistence5 ~ InitialRankNorm * MeanEarlyExposure + EntryYearFE + EntryPrimaryFieldFE + log1p(EntryWorkCount)",
  vcov="clustered by EntryPrimaryField x EntryYear",
  test="two-sided",
  secondary_multiplicity_note="Raw H3 p-value is Holm-adjusted jointly with frozen H2 by code/38_secondary_holm.R.",
  results=unname(split(res,seq_len(nrow(res))))
)
jsonlite::write_json(manifest,file.path(outdir,"manifest.json"),pretty=TRUE,auto_unbox=TRUE)
print(res)
