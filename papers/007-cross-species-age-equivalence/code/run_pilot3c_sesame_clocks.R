#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
if (!(length(args) %in% c(6, 7))) {
  stop("Usage: Rscript run_pilot3c_sesame_clocks.R <idat_dir> <smoke.csv> <traits.csv> <clock2.csv> <clock3.csv> <download_manifest.tsv> [prep_code]")
}

idat_dir <- args[[1]]
smoke_path <- args[[2]]
traits_path <- args[[3]]
clock2_path <- args[[4]]
clock3_path <- args[[5]]
manifest_path <- args[[6]]
prep_code <- if (length(args) >= 7) args[[7]] else "SHCDPB"

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

collapse_probe_ids <- function(ids) {
  vapply(
    strsplit(as.character(ids), "_", fixed=TRUE),
    function(x) x[[1]],
    character(1)
  )
}

species_structural_mask <- function(raw_sdf) {
  base_mask <- as.logical(raw_sdf$mask)
  base_mask[is.na(base_mask)] <- FALSE

  species_sdf <- inferSpecies(raw_sdf)
  species_mask <- as.logical(species_sdf$mask)
  species_mask[is.na(species_mask)] <- FALSE

  added <- species_mask & !base_mask
  unique(collapse_probe_ids(species_sdf$Probe_ID[added]))
}

predict_eta <- function(betas, coefs, species_imputable_ids) {
  intercept <- coefs$beta[coefs$var == "Intercept"]
  if (length(intercept) != 1) stop("expected one Intercept")

  probes <- coefs[coefs$var != "Intercept", , drop=FALSE]
  values <- setNames(rep(NA_real_, nrow(probes)), probes$var)

  present <- probes$var %in% names(betas)
  if (any(present)) {
    values[present] <- betas[probes$var[present]]
  }
  raw_finite <- is.finite(values)

  # MMC GSE223748 processing states that a CpG that does not map to the
  # inferred species is represented as beta=0.5. Reproduce only that
  # structural non-mapping convention here. NAs caused by pOOBAH / other QC
  # remain missing and therefore continue to count against the >=95% gate.
  species_impute <- (
    present &
    !raw_finite &
    probes$var %in% species_imputable_ids
  )
  values[species_impute] <- 0.5

  final_finite <- is.finite(values)
  eta <- intercept + sum(values[final_finite] * probes$beta[final_finite])

  list(
    eta=eta,
    name_coverage=sum(present) / nrow(probes),
    raw_finite_coverage=sum(raw_finite) / nrow(probes),
    coverage=sum(final_finite) / nrow(probes),
    n_required=nrow(probes),
    n_name_present=sum(present),
    n_raw_finite=sum(raw_finite),
    n_species_imputed=sum(species_impute),
    n_residual_missing=sum(!final_finite),
    n_used=sum(final_finite)
  )
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
diag_out <- list()

for (i in seq_len(nrow(smoke))) {
  row <- smoke[i,]
  gsm <- trimws(as.character(row$geo_accession))
  mf <- manifest[trimws(manifest$geo_accession) == gsm, , drop=FALSE]
  if (nrow(mf) != 2) {
    stop(sprintf("%s: manifest expected 2 IDAT files, got %d", gsm, nrow(mf)))
  }

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

  raw_sdf <- readIDATpair(prefix)
  species_imputable_ids <- species_structural_mask(raw_sdf)
  prepped_sdf <- prepSesame(raw_sdf, prep=prep_code)
  betas <- getBetas(prepped_sdf, collapseToPfx=TRUE)

  tr <- traits[traits$species == row$organism, , drop=FALSE]
  if (nrow(tr) != 1) {
    stop(sprintf("%s: trait row count %d", row$organism, nrow(tr)))
  }

  p2 <- predict_eta(betas, c2, species_imputable_ids)
  p3 <- predict_eta(betas, c3, species_imputable_ids)
  a2 <- clock2_age(p2$eta, tr$clock2_highmax_y, tr$gestation_y)
  a3 <- clock3_age(p3$eta, tr$maturity_y, tr$gestation_y)

  out[[length(out)+1]] <- data.frame(
    geo_accession=gsm,
    species=row$organism,
    chronological_age_y=as.numeric(row$age_years),
    tissue=row$tissue_raw,
    pan_clock_training=row$pan_clock_training,
    beta_n=length(betas),
    species_structural_mask_n=length(species_imputable_ids),
    clock2_n_required=p2$n_required,
    clock2_n_name_present=p2$n_name_present,
    clock2_name_coverage=p2$name_coverage,
    clock2_n_raw_finite=p2$n_raw_finite,
    clock2_raw_finite_coverage=p2$raw_finite_coverage,
    clock2_n_species_imputed=p2$n_species_imputed,
    clock2_n_residual_missing=p2$n_residual_missing,
    clock2_n_used=p2$n_used,
    clock2_probe_coverage=p2$coverage,
    clock2_eta=p2$eta,
    clock2_relative_age=a2[["relative_age"]],
    clock2_predicted_age_y=a2[["predicted_age_y"]],
    clock3_n_required=p3$n_required,
    clock3_n_name_present=p3$n_name_present,
    clock3_name_coverage=p3$name_coverage,
    clock3_n_raw_finite=p3$n_raw_finite,
    clock3_raw_finite_coverage=p3$raw_finite_coverage,
    clock3_n_species_imputed=p3$n_species_imputed,
    clock3_n_residual_missing=p3$n_residual_missing,
    clock3_n_used=p3$n_used,
    clock3_probe_coverage=p3$coverage,
    clock3_eta=p3$eta,
    clock3_relative_adult_age=a3[["relative_adult_age"]],
    clock3_m1=a3[["m1"]],
    clock3_predicted_age_y=a3[["predicted_age_y"]],
    stringsAsFactors=FALSE
  )

  diag_out[[length(diag_out)+1]] <- data.frame(
    geo_accession=rep(gsm, 2),
    species=rep(row$organism, 2),
    clock=c("clock2", "clock3"),
    n_required=c(p2$n_required, p3$n_required),
    n_name_present=c(p2$n_name_present, p3$n_name_present),
    name_coverage=c(p2$name_coverage, p3$name_coverage),
    n_raw_finite=c(p2$n_raw_finite, p3$n_raw_finite),
    raw_finite_coverage=c(p2$raw_finite_coverage, p3$raw_finite_coverage),
    n_species_imputed=c(p2$n_species_imputed, p3$n_species_imputed),
    n_residual_missing=c(p2$n_residual_missing, p3$n_residual_missing),
    n_clock_input=c(p2$n_used, p3$n_used),
    clock_input_coverage=c(p2$coverage, p3$coverage),
    stringsAsFactors=FALSE
  )
}

res <- do.call(rbind, out)
diag <- do.call(rbind, diag_out)
write.csv(res, "pilot3c_predictions.csv", row.names=FALSE)
write.csv(diag, "pilot3c_probe_coverage_diagnostics.csv", row.names=FALSE)

summary <- data.frame(
  metric=c(
    "n_samples",
    "min_clock2_name_coverage",
    "min_clock3_name_coverage",
    "min_clock2_raw_finite_coverage",
    "min_clock3_raw_finite_coverage",
    "min_clock2_probe_coverage",
    "min_clock3_probe_coverage",
    "max_clock2_residual_missing",
    "max_clock3_residual_missing",
    "median_abs_error_clock2_y",
    "median_abs_error_clock3_y",
    "cor_clock2_chron_age",
    "cor_clock3_chron_age"
  ),
  value=c(
    nrow(res),
    min(res$clock2_name_coverage),
    min(res$clock3_name_coverage),
    min(res$clock2_raw_finite_coverage),
    min(res$clock3_raw_finite_coverage),
    min(res$clock2_probe_coverage),
    min(res$clock3_probe_coverage),
    max(res$clock2_n_residual_missing),
    max(res$clock3_n_residual_missing),
    median(abs(res$clock2_predicted_age_y-res$chronological_age_y)),
    median(abs(res$clock3_predicted_age_y-res$chronological_age_y)),
    cor(res$clock2_predicted_age_y,res$chronological_age_y,use="complete.obs"),
    cor(res$clock3_predicted_age_y,res$chronological_age_y,use="complete.obs")
  )
)
write.csv(summary, "pilot3c_summary.csv", row.names=FALSE)

cat(
  paste(
    "Clock-input convention:",
    prep_code,
    "observed betas plus beta=0.5 only for CpGs newly masked by",
    "SeSAMe species inference; pOOBAH/QC missingness remains missing.\n"
  )
)
print(res)
print(diag)
print(summary)

if (
  any(res$clock2_probe_coverage < 0.95) ||
  any(res$clock3_probe_coverage < 0.95)
) {
  stop("Universal-clock CpG coverage below 95% after MMC species-nonmapping convention")
}
