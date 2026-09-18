#!/usr/bin/env Rscript

# ARIS4C006 — verify ChineseNames 2025.8 source-package familyname data
# using base R only (no package dependency installation).

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("Usage: 18_verify_chinesenames_r_package.R <extracted_pkg_dir> <mirror_csv> <outdir>")
}
pkg_dir <- normalizePath(args[[1]], mustWork=TRUE)
mirror_path <- args[[2]]
outdir <- args[[3]]
dir.create(outdir, recursive=TRUE, showWarnings=FALSE)

desc_path <- file.path(pkg_dir, "DESCRIPTION")
if (!file.exists(desc_path)) stop("DESCRIPTION missing from extracted source package")
desc <- read.dcf(desc_path)
pkg_ver <- unname(desc[1,"Version"])
pkg_name <- unname(desc[1,"Package"])
if (pkg_name != "ChineseNames") stop("Unexpected package: ", pkg_name)
if (pkg_ver != "2025.8") stop(sprintf("Expected ChineseNames 2025.8, got %s", pkg_ver))

data_dir <- file.path(pkg_dir, "data")
if (!dir.exists(data_dir)) stop("data/ directory missing in source package")

# Prefer a directly named familyname .rda/.RData/.rds, otherwise inspect all R data files.
candidates <- list.files(
  data_dir,
  pattern="\\.(rda|RData|rds)$",
  full.names=TRUE,
  ignore.case=TRUE
)
if (!length(candidates)) stop("No R data files found in source package data/")

env <- new.env(parent=emptyenv())
found <- FALSE
for (p in candidates) {
  ext <- tolower(tools::file_ext(p))
  if (ext == "rds") {
    obj <- readRDS(p)
    if (grepl("familyname", basename(p), ignore.case=TRUE)) {
      assign("familyname", obj, envir=env)
      found <- TRUE
      break
    }
  } else {
    before <- ls(env, all.names=TRUE)
    load(p, envir=env)
    if (exists("familyname", envir=env, inherits=FALSE)) {
      found <- TRUE
      break
    }
    # keep searching; objects are harmless in isolated env
  }
}
if (!found) stop("familyname object not found in source-package data files")

pkg <- as.data.frame(get("familyname", envir=env), stringsAsFactors=FALSE)
mir <- utils::read.csv(mirror_path, fileEncoding="UTF-8", check.names=FALSE, stringsAsFactors=FALSE)

required <- c(
  "surname","compound","initial","initial.rank",
  "n.1930_2008","ppm.1930_2008","surname.uniqueness"
)
if (length(setdiff(required,names(pkg)))) stop("Package familyname missing expected columns")
if (length(setdiff(required,names(mir)))) stop("Mirror familyname missing expected columns")

pkg2 <- pkg[,required,drop=FALSE]
mir2 <- mir[,required,drop=FALSE]

pkg2$surname <- enc2utf8(as.character(pkg2$surname))
mir2$surname <- enc2utf8(as.character(mir2$surname))
pkg2$initial <- tolower(as.character(pkg2$initial))
mir2$initial <- tolower(as.character(mir2$initial))
for (nm in c("compound","initial.rank","n.1930_2008","ppm.1930_2008","surname.uniqueness")) {
  pkg2[[nm]] <- as.numeric(pkg2[[nm]])
  mir2[[nm]] <- as.numeric(mir2[[nm]])
}

pkg2 <- pkg2[order(pkg2$surname),,drop=FALSE]
mir2 <- mir2[order(mir2$surname),,drop=FALSE]
row.names(pkg2) <- NULL
row.names(mir2) <- NULL

if (nrow(pkg2) != 1806L) stop(sprintf("Expected 1806 source-package rows, got %d",nrow(pkg2)))
if (nrow(mir2) != 1806L) stop(sprintf("Expected 1806 mirror rows, got %d",nrow(mir2)))

char_equal <- identical(pkg2$surname,mir2$surname) && identical(pkg2$initial,mir2$initial)
integer_equal <- all(pkg2$compound==mir2$compound) &&
  all(pkg2$initial.rank==mir2$initial.rank) &&
  all(pkg2$n.1930_2008==mir2$n.1930_2008)
ppm_diff <- max(abs(pkg2$ppm.1930_2008-mir2$ppm.1930_2008),na.rm=TRUE)
uni_diff <- max(abs(pkg2$surname.uniqueness-mir2$surname.uniqueness),na.rm=TRUE)
float_equal <- ppm_diff < 1e-9 && uni_diff < 1e-9
all_equal <- char_equal && integer_equal && float_equal

# Minimal base-R JSON for scalar/list values.
esc <- function(x) gsub('"','\\\\"',x,fixed=TRUE)
scalar_json <- function(x) {
  if (is.logical(x)) return(ifelse(x,"true","false"))
  if (is.numeric(x)) return(format(x,scientific=FALSE,trim=TRUE,digits=17))
  sprintf('"%s"',esc(as.character(x)))
}
vals <- list(
  script="18_verify_chinesenames_r_package.R",
  verification_mode="official R-universe source tarball, no dependency installation",
  source_package_name=pkg_name,
  source_package_version=pkg_ver,
  source_package_rows=nrow(pkg2),
  mirror_rows=nrow(mir2),
  exact_character_and_initial_match=char_equal,
  exact_integer_columns_match=integer_equal,
  max_abs_ppm_difference=ppm_diff,
  max_abs_uniqueness_difference=uni_diff,
  mirror_derived_columns_match_official_after_rounding_to_3_decimals=derived_rounding_equal,
  exact_population_counts_match=all(pkg2$n.1930_2008==mir2$n.1930_2008),
  all_required_provenance_checks_pass=all_equal,
  source_package_population_total=sum(pkg2$n.1930_2008),
  mirror_population_total=sum(mir2$n.1930_2008),
  confirmatory_use_allowed=FALSE
)
parts <- mapply(function(n,v) sprintf('  "%s": %s',esc(n),scalar_json(v)),names(vals),vals,USE.NAMES=FALSE)
writeLines(c("{",paste(parts,collapse=",\n"),"}"),file.path(outdir,"manifest.json"),useBytes=TRUE)
utils::write.csv(pkg2,file.path(outdir,"familyname_from_source_package.csv"),row.names=FALSE,fileEncoding="UTF-8")

print(vals)
if (!all_equal) stop("Official source-package core values or expected rounded derived values differ from engineering mirror")
