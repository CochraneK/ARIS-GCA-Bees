#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 6) {
  stop("Usage: Rscript run_pilot3c_sesame_clocks.R <idat_dir> <smoke.csv> <traits.csv> <clock2.csv> <clock3.csv> <download_manifest.tsv>")
}

idat_dir <- args[[1]]
smoke_path <- args[[2]]
traits_path <- args[[3]]
clock2_path <- args[[4]]
clock3_path <- args[[5]]
manifest_path <- args[[6]]

suppressPackageStartupMessages({
  library(sesame)
  library(sesameData)
})

sesameDataCache()

smoke <- read.csv(smoke_path, stringsAsFactors=FALSE, check.names=FALSE)
traits <- read.csv(traits_path, stringsAsFactors=FALSE, check.names=FALSE)
clock2 <- read.csv(clock2_path, stringsAsFactors=FALSE, check.names=FALSE)
clock3 <- read.csv(clock3_path, stringsAsFactors=FALSE, check.names=FALSE)
manifest <- read.delim(manifest_path, stringsAsFactors=FALSE, check.names=FALSE)

coef_map <- function(tab, beta_col) {
  x <- tab[, c("var", beta_col)]
  colnames(x) <- c("var", "beta")
  x <- x[is.finite(x$beta), , drop=FALSE]
  x
}

c2 <- coef_map(clock2, "beta_clock2")
c3 <- coef_map(clock3, "beta_clock3")

predict_eta <- function(betas, coefs) {
  intercept <- coefs$beta[coefs$var == "Intercept"]
  if (length(intercept) != 1) stop("expected one Intercept")
  probes <- coefs[coefs$var != "Intercept", , drop=FALSE]
  present <- probes$var %in% names(betas)
  finite <- present
  finite[present] <- is.finite(betas[probes$var[present]])
  use <- present & finite
  coverage <- sum(use) / nrow(probes)
  eta <- intercept + sum(betas[probes$var[use]] * probes$beta[use])
  list(eta=eta, coverage=coverage, n_required=nrow(probes), n_used=sum(use))
}

clock2_age <- function(eta, highmax, gestation) {
  rel <- exp(-exp(-eta))
  age <- rel * (highmax + gestation) - gestation
  c(relative_age=rel, predicted_age_y=age)
}

clock3_age <- function(eta, maturity, gestation) {
  m1 <- 5 * (gestation/maturity)^0.38
  reladult <- ifelse(eta < 0, (exp(eta)-1)*m1 + m1, eta*m1 + m1)
  age <- reladult * (maturity + gestation) - gestation
  c(relative_adult_age=reladult, predicted_age_y=age, m1=m1)
}

out <- list()
for (i in seq_len(nrow(smoke))) {
  row <- smoke[i,]
  gsm <- trimws(as.character(row$geo_accession))
  mf <- manifest[trimws(manifest$geo_accession) == gsm, , drop=FALSE]
  if (nrow(mf) != 2) stop(sprintf("%s: manifest expected 2 IDAT files, got %d", gsm, nrow(mf)))

  local_names <- trimws(as.character(mf$filename))
  files <- file.path(idat_dir, local_names)
  if (!all(file.exists(files))) {
    missing <- files[!file.exists(files)]
    stop(sprintf("%s: missing local IDAT(s): %s", gsm, paste(missing, collapse=", ")))
  }

  grn <- files[grepl("_Grn\\.idat(\\.gz)?$", files)]
  red <- files[grepl("_Red\\.idat(\\.gz)?$", files)]
  if (length(grn) != 1 || length(red) != 1) {
    stop(sprintf("%s: expected one green and one red IDAT", gsm))
  }
  prefix <- sub("_Grn\\.idat(\\.gz)?$", "", grn)
  message("Processing ", gsm, " ", row$organism, " age=", row$age_years)

  betas <- openSesame(prefix, prep="SHCDPB", collapseToPfx=TRUE)
  tr <- traits[traits$species == row$organism, , drop=FALSE]
  if (nrow(tr) != 1) stop(sprintf("%s: trait row count %d", row$organism, nrow(tr)))

  p2 <- predict_eta(betas, c2)
  p3 <- predict_eta(betas, c3)
  a2 <- clock2_age(p2$eta, tr$clock2_highmax_y, tr$gestation_y)
  a3 <- clock3_age(p3$eta, tr$maturity_y, tr$gestation_y)

  out[[length(out)+1]] <- data.frame(
    geo_accession=gsm,
    species=row$organism,
    chronological_age_y=as.numeric(row$age_years),
    tissue=row$tissue_raw,
    pan_clock_training=row$pan_clock_training,
    beta_n=length(betas),
    clock2_n_required=p2$n_required,
    clock2_n_used=p2$n_used,
    clock2_probe_coverage=p2$coverage,
    clock2_eta=p2$eta,
    clock2_relative_age=a2[["relative_age"]],
    clock2_predicted_age_y=a2[["predicted_age_y"]],
    clock3_n_required=p3$n_required,
    clock3_n_used=p3$n_used,
    clock3_probe_coverage=p3$coverage,
    clock3_eta=p3$eta,
    clock3_relative_adult_age=a3[["relative_adult_age"]],
    clock3_m1=a3[["m1"]],
    clock3_predicted_age_y=a3[["predicted_age_y"]],
    stringsAsFactors=FALSE
  )
}

res <- do.call(rbind, out)
write.csv(res, "pilot3c_predictions.csv", row.names=FALSE)

summary <- data.frame(
  metric=c(
    "n_samples",
    "min_clock2_probe_coverage",
    "min_clock3_probe_coverage",
    "median_abs_error_clock2_y",
    "median_abs_error_clock3_y",
    "cor_clock2_chron_age",
    "cor_clock3_chron_age"
  ),
  value=c(
    nrow(res),
    min(res$clock2_probe_coverage),
    min(res$clock3_probe_coverage),
    median(abs(res$clock2_predicted_age_y-res$chronological_age_y)),
    median(abs(res$clock3_predicted_age_y-res$chronological_age_y)),
    cor(res$clock2_predicted_age_y,res$chronological_age_y,use="complete.obs"),
    cor(res$clock3_predicted_age_y,res$chronological_age_y,use="complete.obs")
  )
)
write.csv(summary, "pilot3c_summary.csv", row.names=FALSE)
print(res)
print(summary)

if (any(res$clock2_probe_coverage < 0.95) || any(res$clock3_probe_coverage < 0.95)) {
  stop("Universal-clock CpG coverage below 95% in one or more samples")
}
