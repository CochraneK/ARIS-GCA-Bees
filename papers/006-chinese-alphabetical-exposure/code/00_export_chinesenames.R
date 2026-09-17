#!/usr/bin/env Rscript

# ARIS4C006 — freeze ChineseNames 2025.8 and derive the population baseline.
# Confirmatory use should run from a clean R environment and retain sessionInfo().

required_version <- "2025.8"
pkg <- "ChineseNames"

if (!requireNamespace(pkg, quietly = TRUE)) {
  install.packages(pkg, repos = "https://cloud.r-project.org")
}

actual_version <- as.character(utils::packageVersion(pkg))
if (actual_version != required_version) {
  stop(sprintf(
    "ChineseNames version mismatch: expected %s, found %s. Pin/install the expected version before confirmatory use.",
    required_version, actual_version
  ))
}

suppressPackageStartupMessages(library(ChineseNames))

dir.create("data/raw/chinesenames_2025.8", recursive = TRUE, showWarnings = FALSE)
dir.create("data/derived", recursive = TRUE, showWarnings = FALSE)
dir.create("data/metadata", recursive = TRUE, showWarnings = FALSE)

# Load all package datasets used or potentially needed by ARIS4C006.
data("familyname", package = "ChineseNames")
data("givenname", package = "ChineseNames")
data("population", package = "ChineseNames")
data("top1000name.prov", package = "ChineseNames")
data("top100name.year", package = "ChineseNames")
data("top50char.year", package = "ChineseNames")

write.csv(familyname,
          "data/raw/chinesenames_2025.8/familyname.csv",
          row.names = FALSE, fileEncoding = "UTF-8")
write.csv(givenname,
          "data/raw/chinesenames_2025.8/givenname.csv",
          row.names = FALSE, fileEncoding = "UTF-8")
write.csv(population,
          "data/raw/chinesenames_2025.8/population.csv",
          row.names = FALSE, fileEncoding = "UTF-8")
write.csv(top1000name.prov,
          "data/raw/chinesenames_2025.8/top1000name_prov.csv",
          row.names = FALSE, fileEncoding = "UTF-8")
write.csv(top100name.year,
          "data/raw/chinesenames_2025.8/top100name_year.csv",
          row.names = FALSE, fileEncoding = "UTF-8")
write.csv(top50char.year,
          "data/raw/chinesenames_2025.8/top50char_year.csv",
          row.names = FALSE, fileEncoding = "UTF-8")

# 26-letter population baseline. Use the count column, not equal A–Z probabilities.
familyname$initial <- tolower(as.character(familyname$initial))

initial_population_n <- aggregate(
  familyname$n.1930_2008,
  by = list(initial = familyname$initial),
  FUN = sum,
  na.rm = TRUE
)
names(initial_population_n)[2] <- "population_n"

initial_surname_count <- aggregate(
  familyname$surname,
  by = list(initial = familyname$initial),
  FUN = length
)
names(initial_surname_count)[2] <- "surname_count"

compound_population_n <- aggregate(
  familyname$n.1930_2008 * as.integer(familyname$compound == 1),
  by = list(initial = familyname$initial),
  FUN = sum,
  na.rm = TRUE
)
names(compound_population_n)[2] <- "compound_surname_population_n"

baseline <- merge(initial_population_n, initial_surname_count, by = "initial", all = TRUE)
baseline <- merge(baseline, compound_population_n, by = "initial", all = TRUE)
baseline$initial_rank <- match(baseline$initial, letters)
baseline$population_share <- baseline$population_n / sum(baseline$population_n, na.rm = TRUE)
baseline$population_ppm <- baseline$population_share * 1e6
baseline <- baseline[order(baseline$initial_rank), c(
  "initial", "initial_rank", "surname_count", "population_n",
  "population_share", "population_ppm", "compound_surname_population_n"
)]

write.csv(baseline,
          "data/derived/chinesenames_initial_population_baseline.csv",
          row.names = FALSE, fileEncoding = "UTF-8")

# Also keep a surname-level frozen analysis table.
surname_baseline <- familyname[, c(
  "surname", "compound", "initial", "initial.rank",
  "n.1930_2008", "ppm.1930_2008", "surname.uniqueness"
)]
write.csv(surname_baseline,
          "data/derived/chinesenames_surname_population_baseline.csv",
          row.names = FALSE, fileEncoding = "UTF-8")

metadata <- c(
  sprintf("package=%s", pkg),
  sprintf("package_version=%s", actual_version),
  sprintf("exported_at=%s", format(Sys.time(), tz = "UTC", usetz = TRUE)),
  "underlying_population_period=1930-2008",
  "warning=Package release year is not the underlying population-data year.",
  "license_check=Verify ChineseNames package/data license and citation requirements before redistribution."
)
writeLines(metadata, "data/metadata/chinesenames_snapshot.txt", useBytes = TRUE)

capture.output(sessionInfo(), file = "data/metadata/R_sessionInfo.txt")

cat("ARIS4C006 ChineseNames baseline written.\n")
print(baseline)
