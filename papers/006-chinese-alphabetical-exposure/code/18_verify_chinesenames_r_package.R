#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: 18_verify_chinesenames_r_package.R <mirror_csv> <outdir>")
}
mirror_path <- args[[1]]
outdir <- args[[2]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

pkg_ver <- as.character(utils::packageVersion("ChineseNames"))
if (pkg_ver != "2025.8") {
  stop(sprintf("Pinned ChineseNames version mismatch: expected 2025.8, got %s", pkg_ver))
}

data("familyname", package = "ChineseNames", envir = environment())
if (!exists("familyname")) stop("familyname dataset not found in installed ChineseNames package")

pkg <- as.data.frame(familyname, stringsAsFactors = FALSE)
mir <- utils::read.csv(mirror_path, fileEncoding = "UTF-8", check.names = FALSE, stringsAsFactors = FALSE)

required <- c(
  "surname", "compound", "initial", "initial.rank",
  "n.1930_2008", "ppm.1930_2008", "surname.uniqueness"
)
missing_pkg <- setdiff(required, names(pkg))
missing_mir <- setdiff(required, names(mir))
if (length(missing_pkg)) stop("Package familyname missing columns: ", paste(missing_pkg, collapse=", "))
if (length(missing_mir)) stop("Mirror familyname missing columns: ", paste(missing_mir, collapse=", "))

pkg2 <- pkg[, required]
mir2 <- mir[, required]

ord_pkg <- order(enc2utf8(pkg2$surname))
ord_mir <- order(enc2utf8(mir2$surname))
pkg2 <- pkg2[ord_pkg, , drop=FALSE]
mir2 <- mir2[ord_mir, , drop=FALSE]
row.names(pkg2) <- NULL
row.names(mir2) <- NULL

if (nrow(pkg2) != 1806L) stop(sprintf("Expected 1806 package surname rows, got %d", nrow(pkg2)))
if (nrow(mir2) != 1806L) stop(sprintf("Expected 1806 mirror surname rows, got %d", nrow(mir2)))

# Normalize numeric types before comparison.
for (nm in c("compound","initial.rank","n.1930_2008","ppm.1930_2008","surname.uniqueness")) {
  pkg2[[nm]] <- as.numeric(pkg2[[nm]])
  mir2[[nm]] <- as.numeric(mir2[[nm]])
}
pkg2$surname <- enc2utf8(as.character(pkg2$surname))
mir2$surname <- enc2utf8(as.character(mir2$surname))
pkg2$initial <- tolower(as.character(pkg2$initial))
mir2$initial <- tolower(as.character(mir2$initial))

char_equal <- identical(pkg2$surname, mir2$surname) && identical(pkg2$initial, mir2$initial)
int_equal <- all(pkg2$compound == mir2$compound) &&
             all(pkg2$initial.rank == mir2$initial.rank) &&
             all(pkg2$n.1930_2008 == mir2$n.1930_2008)
float_diff_ppm <- max(abs(pkg2$ppm.1930_2008 - mir2$ppm.1930_2008), na.rm=TRUE)
float_diff_uni <- max(abs(pkg2$surname.uniqueness - mir2$surname.uniqueness), na.rm=TRUE)
float_equal <- float_diff_ppm < 1e-9 && float_diff_uni < 1e-9

all_equal <- char_equal && int_equal && float_equal

manifest <- list(
  script = "18_verify_chinesenames_r_package.R",
  installed_package_version = pkg_ver,
  expected_package_version = "2025.8",
  package_rows = nrow(pkg2),
  mirror_rows = nrow(mir2),
  required_columns = required,
  exact_character_and_initial_match = char_equal,
  exact_integer_columns_match = int_equal,
  max_abs_ppm_difference = float_diff_ppm,
  max_abs_uniqueness_difference = float_diff_uni,
  all_key_values_match = all_equal,
  package_population_total = sum(pkg2$n.1930_2008),
  mirror_population_total = sum(mir2$n.1930_2008),
  confirmatory_use_allowed = FALSE,
  purpose = "Outcome-blind provenance verification of the ChineseNames 2025.8 population table."
)

json <- function(x, indent=0) {
  # minimal JSON writer avoiding extra package dependencies
  sp <- paste(rep(" ", indent), collapse="")
  if (is.list(x) && is.null(names(x))) {
    return(paste0("[", paste(vapply(x, json, "", indent=indent+2), collapse=", "), "]"))
  }
  if (is.list(x)) {
    parts <- mapply(function(n,v) {
      val <- json(v, indent+2)
      paste0('"', gsub('"','\\\\"',n), '": ', val)
    }, names(x), x, SIMPLIFY=TRUE, USE.NAMES=FALSE)
    return(paste0("{\n", paste0(sp,"  ",parts,collapse=",\n"), "\n", sp, "}"))
  }
  if (is.logical(x)) return(ifelse(x, "true", "false"))
  if (is.numeric(x)) return(format(x, scientific=FALSE, trim=TRUE, digits=16))
  if (is.character(x)) {
    if (length(x)>1) return(paste0("[",paste(sprintf('"%s"',gsub('"','\\\\"',x)),collapse=", "),"]"))
    return(sprintf('"%s"',gsub('"','\\\\"',x)))
  }
  stop("Unsupported JSON type")
}

writeLines(json(manifest), file.path(outdir, "manifest.json"), useBytes=TRUE)
utils::write.csv(pkg2, file.path(outdir, "familyname_from_package.csv"), row.names=FALSE, fileEncoding="UTF-8")

print(manifest)
if (!all_equal) stop("Pinned package familyname values do not match engineering mirror")
