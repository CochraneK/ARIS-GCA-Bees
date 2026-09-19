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

clock_input_vector <- function(betas, required_probes, species_imputable_ids) {
  values <- setNames(rep(NA_real_, length(required_probes)), required_probes)
  present <- required_probes %in% names(betas)
  if (any(present)) {
    values[present] <- betas[required_probes[present]]
  }
  raw_finite <- is.finite(values)

  # MMC GSE223748 processing represents species-unmappable CpGs as beta=0.5.
  # Apply this only to CpGs newly masked by inferSpecies. Detection/QC missing
  # values remain NA and continue to count against the >=95% gate.
  species_impute <- (
    present &
    !raw_finite &
    required_probes %in% species_imputable_ids
  )
  values[species_impute] <- 0.5

  list(
    values=values,
    present=present,
    raw_finite=raw_finite,
    species_impute=species_impute,
    final_finite=is.finite(values)
  )
}

predict_eta <- function(betas, coefs, species_imputable_ids) {
  intercept <- coefs$beta[coefs$var=="Intercept"]
  if (length(intercept)!=1) stop("Expected one intercept")
  p <- coefs[coefs$var!="Intercept",,drop=FALSE]

  inp <- clock_input_vector(betas, p$var, species_imputable_ids)
  use <- inp$final_finite

  list(
    eta=intercept + sum(inp$values[use] * p$beta[use]),
    n_required=nrow(p),
    n_name_present=sum(inp$present),
    name_coverage=sum(inp$present)/nrow(p),
    n_raw_finite=sum(inp$raw_finite),
    raw_finite_coverage=sum(inp$raw_finite)/nrow(p),
    n_species_imputed=sum(inp$species_impute),
    n_residual_missing=sum(!inp$final_finite),
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
diag_out <- vector("list", nrow(samples))

for (i in seq_len(nrow(samples))) {
  row <- samples[i,]
  gsm <- trimws(as.character(row$geo_accession))
  mf <- manifest[trimws(manifest$geo_accession) == gsm, , drop=FALSE]
  if (nrow(mf) != 2) stop(sprintf("%s: manifest expected two IDAT files, got %d", gsm, nrow(mf)))

  local_names <- trimws(as.character(mf$filename))
  files <- file.path(idat_dir, local_names)
  if (!all(file.exists(files))) {
    stop(sprintf("%s: missing local IDAT(s): %s", gsm, paste(files[!file.exists(files)], collapse=", ")))
  }

  grn <- files[grepl("_Grn\\.idat(\\.gz)?$", files)]
  red <- files[grepl("_Red\\.idat(\\.gz)?$", files)]
  if (length(grn)!=1 || length(red)!=1) stop(sprintf("%s: expected one green and one red IDAT", gsm))
  prefix <- sub("_Grn\\.idat(\\.gz)?$", "", grn)

  message(sprintf("[%d/%d] %s %s age=%s tissue=%s",
    i, nrow(samples), gsm, row$organism, row$age_years, row$tissue_raw))

  raw_sdf <- readIDATpair(prefix)
  species_imputable_ids <- species_structural_mask(raw_sdf)
  prepped_sdf <- prepSesame(raw_sdf, prep="SHCDPB")
  betas <- getBetas(
    prepped_sdf,
    collapseToPfx=TRUE,
    collapseMethod="mean"
  )

  p2 <- predict_eta(betas,c2,species_imputable_ids)
  p3 <- predict_eta(betas,c3,species_imputable_ids)
  all_input <- clock_input_vector(
    betas,
    all_probes,
    species_imputable_ids
  )
  probe_matrix[,i] <- all_input$values

  out[[i]] <- data.frame(
    geo_accession=gsm,
    species=row$organism,
    chronological_age_y=as.numeric(row$age_years),
    tissue=row$tissue_raw,
    sex=row$sex,
    age_confidence=row$age_confidence,
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
    stringsAsFactors=FALSE
  )

  diag_out[[i]] <- data.frame(
    geo_accession=rep(gsm,2),
    species=rep(row$organism,2),
    clock=c("clock2","clock3"),
    n_required=c(p2$n_required,p3$n_required),
    n_name_present=c(p2$n_name_present,p3$n_name_present),
    name_coverage=c(p2$name_coverage,p3$name_coverage),
    n_raw_finite=c(p2$n_raw_finite,p3$n_raw_finite),
    raw_finite_coverage=c(p2$raw_finite_coverage,p3$raw_finite_coverage),
    n_species_imputed=c(p2$n_species_imputed,p3$n_species_imputed),
    n_residual_missing=c(p2$n_residual_missing,p3$n_residual_missing),
    n_clock_input=c(p2$n_used,p3$n_used),
    clock_input_coverage=c(p2$coverage,p3$coverage),
    stringsAsFactors=FALSE
  )
}

pred <- do.call(rbind,out)
diag <- do.call(rbind,diag_out)
write.csv(pred, file.path(out_dir,"molecular_linear_predictors.csv"), row.names=FALSE)
write.csv(diag, file.path(out_dir,"probe_coverage_diagnostics.csv"), row.names=FALSE)

beta_out <- data.frame(probe=rownames(probe_matrix), probe_matrix, check.names=FALSE)
con <- gzfile(file.path(out_dir,"clock_probe_betas.csv.gz"),"wt")
write.csv(beta_out,con,row.names=FALSE)
close(con)

qc <- data.frame(
  metric=c(
    "n_samples",
    "n_unique_clock_probes",
    "min_clock2_name_coverage",
    "median_clock2_name_coverage",
    "min_clock2_raw_finite_coverage",
    "median_clock2_raw_finite_coverage",
    "min_clock2_probe_coverage",
    "median_clock2_probe_coverage",
    "max_clock2_residual_missing",
    "min_clock3_name_coverage",
    "median_clock3_name_coverage",
    "min_clock3_raw_finite_coverage",
    "median_clock3_raw_finite_coverage",
    "min_clock3_probe_coverage",
    "median_clock3_probe_coverage",
    "max_clock3_residual_missing"
  ),
  value=c(
    nrow(pred),
    length(all_probes),
    min(pred$clock2_name_coverage),
    median(pred$clock2_name_coverage),
    min(pred$clock2_raw_finite_coverage),
    median(pred$clock2_raw_finite_coverage),
    min(pred$clock2_probe_coverage),
    median(pred$clock2_probe_coverage),
    max(pred$clock2_n_residual_missing),
    min(pred$clock3_name_coverage),
    median(pred$clock3_name_coverage),
    min(pred$clock3_raw_finite_coverage),
    median(pred$clock3_raw_finite_coverage),
    min(pred$clock3_probe_coverage),
    median(pred$clock3_probe_coverage),
    max(pred$clock3_n_residual_missing)
  )
)
write.csv(qc,file.path(out_dir,"normalization_qc.csv"),row.names=FALSE)
print(qc)
print(diag)

if (any(!is.finite(pred$clock2_eta)) || any(!is.finite(pred$clock3_eta))) {
  stop("Non-finite molecular linear predictor")
}
if (any(pred$clock2_probe_coverage < 0.95) || any(pred$clock3_probe_coverage < 0.95)) {
  stop("Universal-clock CpG coverage below 95% after MMC species-nonmapping convention")
}
