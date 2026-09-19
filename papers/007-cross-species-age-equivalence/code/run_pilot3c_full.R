#!/usr/bin/env Rscript
# ARIS4C007 Pilot 3C full molecular preprocessing.
#
# Responsibility boundary:
#   raw IDAT -> SeSAMe normalized betas -> Universal Clock 2/3 linear predictors
#
# This script deliberately does NOT apply life-history inverse transformations.
# Those are applied downstream so molecular signal and age-coordinate assumptions
# remain auditable as separate layers.

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 6) {
  stop("Usage: Rscript run_pilot3c_full.R <idat_dir> <samples.csv> <clock2.csv> <clock3.csv> <out_dir> <download_manifest.tsv>")
}

idat_dir <- args[[1]]
sample_path <- args[[2]]
clock2_path <- args[[3]]
clock3_path <- args[[4]]
out_dir <- args[[5]]
manifest_path <- args[[6]]
dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)

suppressPackageStartupMessages({
  library(sesame)
  library(sesameData)
})

sesameDataCache()

samples <- read.csv(sample_path, stringsAsFactors=FALSE, check.names=FALSE)
clock2 <- read.csv(clock2_path, stringsAsFactors=FALSE, check.names=FALSE)
clock3 <- read.csv(clock3_path, stringsAsFactors=FALSE, check.names=FALSE)
manifest <- read.delim(manifest_path, stringsAsFactors=FALSE, check.names=FALSE)

coef_map <- function(tab, beta_col) {
  x <- tab[, c("var", beta_col)]
  colnames(x) <- c("var","beta")
  x <- x[is.finite(x$beta),,drop=FALSE]
  x
}
c2 <- coef_map(clock2, "beta_clock2")
c3 <- coef_map(clock3, "beta_clock3")

probe2 <- c2$var[c2$var != "Intercept"]
probe3 <- c3$var[c3$var != "Intercept"]
all_probes <- sort(unique(c(probe2, probe3)))

predict_eta <- function(betas, coefs) {
  intercept <- coefs$beta[coefs$var=="Intercept"]
  if (length(intercept)!=1) stop("Expected one intercept")
  p <- coefs[coefs$var!="Intercept",,drop=FALSE]
  idx <- match(p$var, names(betas))
  present <- !is.na(idx)
  finite <- present
  finite[present] <- is.finite(betas[idx[present]])
  use <- present & finite
  list(
    eta=intercept + sum(betas[idx[use]] * p$beta[use]),
    n_required=nrow(p),
    n_used=sum(use),
    coverage=sum(use)/nrow(p)
  )
}

probe_matrix <- matrix(
  NA_real_,
  nrow=length(all_probes),
  ncol=nrow(samples),
  dimnames=list(all_probes, samples$geo_accession)
)

out <- vector("list", nrow(samples))
for (i in seq_len(nrow(samples))) {
  row <- samples[i,]
  gsm <- trimws(as.character(row$geo_accession))
  mf <- manifest[trimws(manifest$geo_accession) == gsm, , drop=FALSE]
  if (nrow(mf) != 2) stop(sprintf("%s: manifest expected two IDAT files, got %d", gsm, nrow(mf)))

  local_names <- sub("\\.gz$", "", mf$filename)
  files <- file.path(idat_dir, local_names)
  if (!all(file.exists(files))) {
    stop(sprintf("%s: missing local IDAT(s): %s", gsm, paste(files[!file.exists(files)], collapse=", ")))
  }

  grn <- files[grepl("_Grn\\.idat$", files)]
  red <- files[grepl("_Red\\.idat$", files)]
  if (length(grn)!=1 || length(red)!=1) stop(sprintf("%s: expected one green and one red IDAT", gsm))
  prefix <- sub("_Grn\\.idat$", "", grn)

  message(sprintf("[%d/%d] %s %s age=%s tissue=%s",
    i, nrow(samples), gsm, row$organism, row$age_years, row$tissue_raw))

  betas <- openSesame(
    prefix,
    prep="SHCDPB",
    collapseToPfx=TRUE,
    collapseMethod="mean"
  )

  p2 <- predict_eta(betas,c2)
  p3 <- predict_eta(betas,c3)

  idx <- match(all_probes, names(betas))
  ok <- !is.na(idx)
  probe_matrix[ok,i] <- betas[idx[ok]]

  out[[i]] <- data.frame(
    geo_accession=gsm,
    species=row$organism,
    chronological_age_y=as.numeric(row$age_years),
    tissue=row$tissue_raw,
    sex=row$sex,
    age_confidence=row$age_confidence,
    pan_clock_training=row$pan_clock_training,
    beta_n=length(betas),
    clock2_n_required=p2$n_required,
    clock2_n_used=p2$n_used,
    clock2_probe_coverage=p2$coverage,
    clock2_eta=p2$eta,
    clock3_n_required=p3$n_required,
    clock3_n_used=p3$n_used,
    clock3_probe_coverage=p3$coverage,
    clock3_eta=p3$eta,
    stringsAsFactors=FALSE
  )
}

pred <- do.call(rbind,out)
write.csv(pred, file.path(out_dir,"molecular_linear_predictors.csv"), row.names=FALSE)

beta_out <- data.frame(probe=rownames(probe_matrix), probe_matrix, check.names=FALSE)
con <- gzfile(file.path(out_dir,"clock_probe_betas.csv.gz"),"wt")
write.csv(beta_out,con,row.names=FALSE)
close(con)

qc <- data.frame(
  metric=c(
    "n_samples",
    "n_unique_clock_probes",
    "min_clock2_probe_coverage",
    "median_clock2_probe_coverage",
    "min_clock3_probe_coverage",
    "median_clock3_probe_coverage"
  ),
  value=c(
    nrow(pred),
    length(all_probes),
    min(pred$clock2_probe_coverage),
    median(pred$clock2_probe_coverage),
    min(pred$clock3_probe_coverage),
    median(pred$clock3_probe_coverage)
  )
)
write.csv(qc,file.path(out_dir,"normalization_qc.csv"),row.names=FALSE)
print(qc)

if (any(!is.finite(pred$clock2_eta)) || any(!is.finite(pred$clock3_eta))) {
  stop("Non-finite molecular linear predictor")
}
if (any(pred$clock2_probe_coverage < 0.95) || any(pred$clock3_probe_coverage < 0.95)) {
  stop("Universal-clock CpG coverage below 95%")
}
