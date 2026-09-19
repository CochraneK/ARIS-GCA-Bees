#!/usr/bin/env Rscript

# ARIS4C006 locked confirmatory H1/H2 execution.
# Refuses to run unless preregistration lock exists and BOTH machine-readable
# gate files explicitly set confirmatory_outcomes_unlocked=true.

args <- commandArgs(trailingOnly=TRUE)
get_arg <- function(flag) {
  i <- match(flag, args)
  if (is.na(i) || i == length(args)) stop(paste("missing", flag))
  args[[i+1]]
}

input_csv <- get_arg("--input")
outdir <- get_arg("--outdir")

if (!requireNamespace("fixest", quietly=TRUE)) stop("fixest is required")
if (!requireNamespace("jsonlite", quietly=TRUE)) stop("jsonlite is required")
if (!dir.exists("process")) stop("run from papers/006-chinese-alphabetical-exposure")

lock_path <- file.path("process", "PREREGISTRATION_LOCK.json")
if (!file.exists(lock_path)) stop("LOCKED: PREREGISTRATION_LOCK.json missing")
lock <- jsonlite::fromJSON(lock_path)
gates <- jsonlite::fromJSON(file.path("process", "DESIGN_GATES.json"))
spec <- jsonlite::fromJSON(file.path("process", "ANALYSIS_SPEC.json"))

if (!isTRUE(gates$confirmatory_outcomes_unlocked)) stop("LOCKED: DESIGN_GATES not unlocked")
if (!isTRUE(spec$confirmatory_outcomes_unlocked)) stop("LOCKED: ANALYSIS_SPEC not unlocked")
if (!identical(spec$primary_model$primary_estimand, "beta2")) stop("spec drift: primary estimand")
expected_cluster <- c("canonical_author_id","work_id","primary_field_x_year")
if (!identical(as.character(spec$primary_model$inference$cluster), expected_cluster)) {
  stop("spec drift: cluster rule")
}

d <- read.csv(input_csv, stringsAsFactors=FALSE, check.names=FALSE)
required <- c(
  "listed_position_norm","first_listed","rel_alpha_rank","loao_exposure",
  "work_id","canonical_author_id","field_year_cluster"
)
missing_cols <- setdiff(required, names(d))
if (length(missing_cols)) stop(paste("missing columns:", paste(missing_cols, collapse=", ")))
if (nrow(d) == 0) stop("empty confirmatory frame")

fit_h1 <- fixest::feols(
  listed_position_norm ~ rel_alpha_rank + rel_alpha_rank:loao_exposure | work_id,
  data=d,
  vcov=~canonical_author_id + work_id + field_year_cluster
)

fit_h2 <- fixest::feols(
  first_listed ~ rel_alpha_rank + rel_alpha_rank:loao_exposure | work_id,
  data=d,
  vcov=~canonical_author_id + work_id + field_year_cluster
)

term <- "rel_alpha_rank:loao_exposure"

extract_term <- function(fit, label) {
  co <- stats::coef(fit)
  se <- fixest::se(fit)
  if (!term %in% names(co)) stop(paste(label, "missing interaction term"))
  b <- unname(co[[term]])
  s <- unname(se[[term]])
  z <- b/s
  p <- 2*stats::pnorm(abs(z), lower.tail=FALSE)
  data.frame(
    estimand=label,
    term=term,
    estimate=b,
    std_error=s,
    conf_low=b-1.959963984540054*s,
    conf_high=b+1.959963984540054*s,
    p_value_raw=p,
    stringsAsFactors=FALSE
  )
}

res <- rbind(
  extract_term(fit_h1, "H1_beta2_listed_position"),
  extract_term(fit_h2, "H2_beta2_first_listed")
)

dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
write.csv(res, file.path(outdir, "confirmatory_h1_h2.csv"), row.names=FALSE)

cluster_counts <- list(
  canonical_authors=length(unique(d$canonical_author_id)),
  works=length(unique(d$work_id)),
  field_year_clusters=length(unique(d$field_year_cluster))
)

manifest <- list(
  script="30_confirmatory_h1_h2.R",
  prereg_lock_label=lock$lock_label,
  prereg_lock_sha256=lock$combined_sha256,
  confirmatory_unlock_verified=TRUE,
  rows=nrow(d),
  works=cluster_counts$works,
  canonical_authors=cluster_counts$canonical_authors,
  field_year_clusters=cluster_counts$field_year_clusters,
  primary_model="listed_position_norm ~ rel_alpha_rank + rel_alpha_rank:loao_exposure | work_id",
  secondary1_model="first_listed ~ rel_alpha_rank + rel_alpha_rank:loao_exposure | work_id",
  vcov="three-way clustered: canonical_author_id + work_id + field_year_cluster",
  primary_test="two-sided alpha=0.05",
  secondary_multiplicity_note="H2 raw p-value stored here; Holm adjustment is applied jointly with frozen H3 after H3 execution.",
  results=unname(split(res, seq_len(nrow(res))))
)
jsonlite::write_json(manifest, file.path(outdir, "manifest.json"), pretty=TRUE, auto_unbox=TRUE)
print(res)
