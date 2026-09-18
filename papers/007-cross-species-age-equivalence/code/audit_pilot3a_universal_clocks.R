#!/usr/bin/env Rscript
# ARIS4C007 Pilot 3A: universal mammalian clock implementation parity audit.
#
# This script does NOT vendor or modify MammalMethylClock source. CI downloads
# the tagged upstream release, sources its released transformation function in
# place, and records only hashes/numeric audit outputs.
#
# Authoritative comparator: Lu et al. 2023 MMC v3.0.0 reference implementation.

args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 8) {
  stop(paste(
    "Usage: Rscript audit_pilot3a_universal_clocks.R",
    "mydata.rds mmc_clock2.csv mmc_clock3.csv zoller_universal.csv",
    "package_extract_dir package_transform_source out_dir provenance.tsv"
  ))
}

mydata_path <- args[[1]]
mmc_clock2_path <- args[[2]]
mmc_clock3_path <- args[[3]]
zoller_coef_path <- args[[4]]
package_dir <- args[[5]]
package_transform_source <- args[[6]]
out_dir <- args[[7]]
prov_path <- args[[8]]
dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)

norm_var <- function(x) {
  x <- as.character(x)
  x[x == "(Intercept)"] <- "Intercept"
  x
}

max_abs <- function(x, y) {
  z <- abs(as.numeric(x) - as.numeric(y))
  if (all(is.na(z))) return(NA_real_)
  max(z, na.rm=TRUE)
}

median_abs <- function(x, y) {
  z <- abs(as.numeric(x) - as.numeric(y))
  if (all(is.na(z))) return(NA_real_)
  median(z, na.rm=TRUE)
}

compare_coefficients <- function(a, b, a_name, b_name) {
  a$var <- norm_var(a$var)
  b$var <- norm_var(b$var)
  colnames(a)[2] <- "coef_a"
  colnames(b)[2] <- "coef_b"
  m <- merge(a, b, by="var", all=TRUE)
  m$missing_a <- is.na(m$coef_a)
  m$missing_b <- is.na(m$coef_b)
  m$abs_diff <- abs(m$coef_a - m$coef_b)
  m$source_a <- a_name
  m$source_b <- b_name
  m
}

weighted_predict <- function(coefs, dat_meth0) {
  coefs$var <- norm_var(coefs$var)
  intercept <- coefs$coef[coefs$var == "Intercept"]
  if (length(intercept) != 1) stop("Expected exactly one intercept")
  cpg <- coefs$var[coefs$var != "Intercept"]
  beta <- coefs$coef[coefs$var != "Intercept"]
  idx <- match(cpg, dat_meth0$CGid)
  if (any(is.na(idx))) {
    stop(paste("Missing CpGs:", paste(head(cpg[is.na(idx)], 20), collapse=", ")))
  }
  X <- as.matrix(dat_meth0[idx, -1, drop=FALSE])
  storage.mode(X) <- "double"
  as.numeric(intercept + colSums(X * beta))
}

# ---------------- Upstream official example bundle ----------------
myinput <- readRDS(mydata_path)
if (length(myinput) < 4) stop("Unexpected mydata_GitHub.Rds structure")

info0 <- as.data.frame(myinput[[1]])
dat_meth0 <- as.data.frame(myinput[[2]], check.names=FALSE)
anage <- as.data.frame(myinput[[3]])
glmnet_list <- myinput[[4]]

needed_traits <- c(
  "SpeciesLatinName", "GestationTimeInYears", "averagedMaturity.yrs", "maxAge"
)
if (!all(needed_traits %in% colnames(anage))) stop("AnAge fields missing")
info <- merge(
  info0,
  anage[, needed_traits],
  by="SpeciesLatinName"
)

# Reproduce the published MYMAX sensitivity assumption exactly.
info$HighmaxAge <- 1.3 * info$maxAge
info$HighmaxAge[info$SpeciesLatinName == "Homo sapiens"] <-
  info$maxAge[info$SpeciesLatinName == "Homo sapiens"]
info$HighmaxAge[info$SpeciesLatinName == "Mus musculus"] <-
  info$maxAge[info$SpeciesLatinName == "Mus musculus"]

# Construct methylation matrix exactly as the reference script.
all_vars <- unique(unlist(lapply(glmnet_list[1:3], function(x) as.character(x$var))))
all_cpg <- setdiff(norm_var(all_vars), "Intercept")
keep <- dat_meth0$CGid %in% all_cpg
dm0 <- dat_meth0[keep, , drop=FALSE]
dm <- as.data.frame(t(dm0[, -1, drop=FALSE]), check.names=FALSE)
colnames(dm) <- dm0$CGid
dm$Basename <- rownames(dm)
dm$Intercept <- 1
info <- merge(info, dm, by="Basename")

beta_names <- c("beta_clock1", "beta_clock2", "beta_clock3")
y_names <- c("Y.pred1", "Y.pred2", "Y.pred3")
for (k in 1:3) {
  g <- as.data.frame(glmnet_list[[k]])
  g$var <- norm_var(g$var)
  b <- as.numeric(g[[beta_names[k]]])
  X <- as.matrix(info[, as.character(g$var), drop=FALSE])
  storage.mode(X) <- "double"
  info[[y_names[k]]] <- as.numeric(X %*% b)
}

# Official reference inverse transformations.
official_clock2 <- function(y, max_age, gestation) {
  rel <- exp(-exp(-y))
  rel * (max_age + gestation) - gestation
}

official_clock3 <- function(y, maturity, gestation) {
  m <- 5 * (gestation / maturity)^0.38
  reladult <- ifelse(y < 0, m * exp(y), m * (y + 1))
  reladult * (maturity + gestation) - gestation
}

info$OfficialClock1_corrected <- exp(info$Y.pred1) - 2
# Reproduce literal v3.0.0 script line after the for loop, where k remains 3.
info$OfficialScriptClock1_literal <- exp(info$Y.pred3) - 2
info$OfficialClock2 <- official_clock2(
  info$Y.pred2, info$HighmaxAge, info$GestationTimeInYears
)
info$OfficialClock3 <- official_clock3(
  info$Y.pred3, info$averagedMaturity.yrs, info$GestationTimeInYears
)

# ---------------- Coefficient parity ----------------
c2 <- read.csv(mmc_clock2_path, stringsAsFactors=FALSE, check.names=FALSE)
c3 <- read.csv(mmc_clock3_path, stringsAsFactors=FALSE, check.names=FALSE)
z <- read.csv(zoller_coef_path, stringsAsFactors=FALSE, check.names=FALSE)

mmc2 <- data.frame(var=c2$var, coef=as.numeric(c2$beta_clock2))
mmc3 <- data.frame(var=c3$var, coef=as.numeric(c3$beta_clock3))
z2 <- data.frame(
  var=z$var,
  coef=as.numeric(z[["Coef.Universal2_RelativeAge"]])
)
z3 <- data.frame(
  var=z$var,
  coef=as.numeric(z[["Coef.Universal3_Age.LogLinearRelAdult"]])
)
z2 <- z2[!is.na(z2$coef), , drop=FALSE]
z3 <- z3[!is.na(z3$coef), , drop=FALSE]

cmp2 <- compare_coefficients(
  mmc2, z2, "MMC_v3.0.0_clock2", "MammalMethylClock_v1.1.0_Universal2"
)
cmp3 <- compare_coefficients(
  mmc3, z3, "MMC_v3.0.0_clock3", "MammalMethylClock_v1.1.0_Universal3"
)
cmp2$clock <- "Clock2"
cmp3$clock <- "Clock3"
write.csv(
  rbind(cmp2, cmp3),
  file.path(out_dir, "coefficient_parity.csv"),
  row.names=FALSE
)

# Independent linear predictors from the MammalMethylClock coefficient table.
info$ZollerY2 <- weighted_predict(z2, dat_meth0)
info$ZollerY3 <- weighted_predict(z3, dat_meth0)

# weighted_predict follows sample columns in dat_meth0; align by Basename.
z_sample_names <- colnames(dat_meth0)[-1]
z_pred <- data.frame(
  Basename=z_sample_names,
  ZollerY2=weighted_predict(z2, dat_meth0),
  ZollerY3=weighted_predict(z3, dat_meth0),
  stringsAsFactors=FALSE
)
info <- merge(
  info[, !colnames(info) %in% c("ZollerY2","ZollerY3"), drop=FALSE],
  z_pred,
  by="Basename",
  all.x=TRUE
)

# ---------------- Release-package transformation audit ----------------
pkg_env <- new.env(parent=baseenv())
sys.source(package_transform_source, envir=pkg_env)
if (!exists("fun_llinreladult.inv", envir=pkg_env, inherits=FALSE)) {
  stop("Release package did not expose fun_llinreladult.inv in located source")
}
pkg_inv <- get("fun_llinreladult.inv", envir=pkg_env)
info$PackageClock3_transform <- pkg_inv(
  info$Y.pred3,
  info$averagedMaturity.yrs,
  info$GestationTimeInYears
)

# A direct implementation of the formula documented above that package function.
documented_clock3 <- function(y, maturity, gestation) {
  m <- 5 * (gestation / maturity)^0.38
  reladult <- ifelse(y < 0, m * exp(y), m * y + m)
  (maturity + gestation) * reladult - gestation
}
info$DocumentedClock3_transform <- documented_clock3(
  info$Y.pred3,
  info$averagedMaturity.yrs,
  info$GestationTimeInYears
)

# Keep outputs bounded: no methylation beta matrix is written out.
prediction_cols <- intersect(c(
  "Basename", "SpeciesLatinName", "MammalNumberHorvath", "Age", "Tissue",
  "GestationTimeInYears", "averagedMaturity.yrs", "maxAge", "HighmaxAge",
  "Y.pred1", "Y.pred2", "Y.pred3", "ZollerY2", "ZollerY3",
  "OfficialClock1_corrected", "OfficialScriptClock1_literal",
  "OfficialClock2", "OfficialClock3",
  "PackageClock3_transform", "DocumentedClock3_transform"
), colnames(info))
write.csv(
  info[, prediction_cols, drop=FALSE],
  file.path(out_dir, "example_predictions.csv"),
  row.names=FALSE
)

# ---------------- Metrics ----------------
metric <- data.frame(
  metric=character(),
  value=character(),
  detail=character(),
  stringsAsFactors=FALSE
)
add_metric <- function(name, value, detail="") {
  metric[nrow(metric)+1, ] <<- c(name, as.character(value), detail)
}

add_metric("n_example_samples", nrow(info))
add_metric("n_example_species", length(unique(info$SpeciesLatinName)),
           paste(sort(unique(info$SpeciesLatinName)), collapse="; "))
add_metric("clock2_mmc_coeff_n", nrow(mmc2))
add_metric("clock2_zoller_coeff_n", nrow(z2))
add_metric("clock2_coeff_missing_mmc", sum(cmp2$missing_a))
add_metric("clock2_coeff_missing_zoller", sum(cmp2$missing_b))
add_metric("clock2_coeff_max_abs_diff", max(cmp2$abs_diff, na.rm=TRUE))
add_metric("clock3_mmc_coeff_n", nrow(mmc3))
add_metric("clock3_zoller_coeff_n", nrow(z3))
add_metric("clock3_coeff_missing_mmc", sum(cmp3$missing_a))
add_metric("clock3_coeff_missing_zoller", sum(cmp3$missing_b))
add_metric("clock3_coeff_max_abs_diff", max(cmp3$abs_diff, na.rm=TRUE))
add_metric("clock2_linear_predictor_max_abs_diff",
           max_abs(info$Y.pred2, info$ZollerY2))
add_metric("clock3_linear_predictor_max_abs_diff",
           max_abs(info$Y.pred3, info$ZollerY3))
add_metric("clock3_documented_vs_official_max_abs_year_diff",
           max_abs(info$DocumentedClock3_transform, info$OfficialClock3))
add_metric("clock3_release_function_vs_official_max_abs_year_diff",
           max_abs(info$PackageClock3_transform, info$OfficialClock3))
add_metric("clock3_release_function_vs_official_median_abs_year_diff",
           median_abs(info$PackageClock3_transform, info$OfficialClock3))
add_metric("clock1_literal_script_vs_corrected_max_abs_year_diff",
           max_abs(info$OfficialScriptClock1_literal, info$OfficialClock1_corrected),
           "Reference v3.0.0 script uses y.name[k] after loop; k=3.")
add_metric("clock2_example_median_abs_error_years",
           median(abs(info$OfficialClock2 - info$Age), na.rm=TRUE))
add_metric("clock3_example_median_abs_error_years",
           median(abs(info$OfficialClock3 - info$Age), na.rm=TRUE))
add_metric("release_transform_source", package_transform_source)
add_metric("package_extract_dir", package_dir)
write.csv(metric, file.path(out_dir, "audit_metrics.csv"), row.names=FALSE)

# Preserve upstream provenance assembled by shell.
if (file.exists(prov_path)) {
  file.copy(prov_path, file.path(out_dir, "upstream_provenance.tsv"), overwrite=TRUE)
}

print(metric)
