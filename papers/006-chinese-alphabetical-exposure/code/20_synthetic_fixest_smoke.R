#!/usr/bin/env Rscript

# ARIS4C006 synthetic-only regression smoke test.
# No real OpenAlex surname/outcome data are read.

set.seed(60062026)

n_work <- 600
authors_pool <- sprintf("A%04d", 1:900)
fields <- sprintf("F%02d", 1:12)
years <- 2011:2025

rows <- vector("list", n_work)
true_beta1 <- 0.18
true_beta2 <- 0.55

for (w in seq_len(n_work)) {
  n <- sample(3:7, 1)
  author <- sample(authors_pool, n, replace=FALSE)
  rel <- seq(0, 1, length.out=n)
  # Random permutation makes author identity independent of rel in expectation.
  rel <- sample(rel, n, replace=FALSE)
  field <- sample(fields, 1)
  year <- sample(years, 1)
  fieldyear <- paste(field, year, sep="_")
  exposure <- runif(1, -0.05, 0.30)
  work_fe <- rnorm(1, sd=0.30)
  eps <- rnorm(n, sd=0.12)
  y <- work_fe + true_beta1*rel + true_beta2*(rel*exposure) + eps
  rows[[w]] <- data.frame(
    y=y,
    rel=rel,
    exposure=exposure,
    author=author,
    work=sprintf("W%04d", w),
    fieldyear=fieldyear,
    stringsAsFactors=FALSE
  )
}
d <- do.call(rbind, rows)

if (!requireNamespace("fixest", quietly=TRUE)) {
  stop("fixest is required")
}

fit <- fixest::feols(
  y ~ rel + rel:exposure | work,
  data=d,
  vcov=~author + work + fieldyear
)

co <- stats::coef(fit)
se <- fixest::se(fit)

if (!"rel:exposure" %in% names(co)) {
  stop("interaction coefficient rel:exposure not estimated")
}

b2 <- unname(co[["rel:exposure"]])
s2 <- unname(se[["rel:exposure"]])
b1 <- unname(co[["rel"]])
s1 <- unname(se[["rel"]])

if (!is.finite(b2) || !is.finite(s2) || s2 <= 0) stop("invalid interaction estimate/SE")
if (abs(b2 - true_beta2) > 0.15) {
  stop(sprintf("synthetic interaction recovery failed: expected %.3f, got %.3f", true_beta2, b2))
}
if (abs(b1 - true_beta1) > 0.08) {
  stop(sprintf("synthetic rel recovery failed: expected %.3f, got %.3f", true_beta1, b1))
}

# Cluster dimensions must all be non-degenerate.
cluster_counts <- c(
  author=length(unique(d$author)),
  work=length(unique(d$work)),
  fieldyear=length(unique(d$fieldyear))
)
if (any(cluster_counts < c(author=100,work=100,fieldyear=30))) stop("cluster dimensions unexpectedly small")

dir.create("data/pilot/model_smoke", recursive=TRUE, showWarnings=FALSE)

json_escape <- function(x) gsub('"','\\\\"',x,fixed=TRUE)
manifest <- sprintf(
'{
  "script": "20_synthetic_fixest_smoke.R",
  "real_outcome_data_used": false,
  "software": "fixest",
  "model": "y ~ rel + rel:exposure | work",
  "vcov": "three-way clustered: author + work + fieldyear",
  "rows": %d,
  "works": %d,
  "authors": %d,
  "fieldyear_clusters": %d,
  "true_beta1": %.8f,
  "estimated_beta1": %.8f,
  "se_beta1": %.8f,
  "true_beta2": %.8f,
  "estimated_beta2": %.8f,
  "se_beta2": %.8f,
  "status": "PASS"
}
',
nrow(d), cluster_counts[["work"]], cluster_counts[["author"]], cluster_counts[["fieldyear"]],
true_beta1,b1,s1,true_beta2,b2,s2)

writeLines(manifest, "data/pilot/model_smoke/manifest.json", useBytes=TRUE)
cat(manifest)
