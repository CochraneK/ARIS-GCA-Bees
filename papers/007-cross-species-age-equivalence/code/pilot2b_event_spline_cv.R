# ARIS4C007 Pilot 2B
# Author-style smooth-spline age translation with leave-one-timepoint-out CV.
#
# Januel et al. 2026 use smooth.spline on log10 post-conception ages:
# - cat -> human: df = 30
# - mouse -> human: df = 12
# - chimpanzee -> human: df = 12
#
# This script preserves those df choices but evaluates them out-of-sample by
# removing all rows sharing the held-out Timepoint before fitting.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("Usage: Rscript pilot2b_event_spline_cv.R input.csv output.csv diagnostics.csv")
}

input_path <- args[[1]]
output_path <- args[[2]]
diag_path <- args[[3]]

d <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)

required <- c(
  "source_species", "timepoint",
  "source_observed_pcd_days", "human_observed_pcd_days"
)
missing <- setdiff(required, colnames(d))
if (length(missing) > 0) {
  stop(paste("Missing columns:", paste(missing, collapse = ", ")))
}

df_target <- c(
  "Felis catus" = 30,
  "Mus musculus" = 12,
  "Pan troglodytes" = 12
)

d$A4_event_spline_predicted_human_pcd_y <- NA_real_
d$A4_event_spline_log10_error <- NA_real_
d$A4_event_spline_df_used <- NA_real_

diagnostics <- data.frame(
  source_species = character(),
  target_df = numeric(),
  full_fit_df_used = numeric(),
  n_rows = integer(),
  n_unique_timepoints = integer(),
  n_unique_source_ages = integer(),
  full_fit_r_squared_log10 = numeric(),
  stringsAsFactors = FALSE
)

safe_df <- function(target, x) {
  n_unique <- length(unique(x[is.finite(x)]))
  # smooth.spline requires enough unique x values; preserve the paper's target
  # df whenever possible and otherwise fail softly to n_unique - 1.
  max(2, min(target, n_unique - 1))
}

for (sp in names(df_target)) {
  idx_sp <- which(d$source_species == sp)
  if (length(idx_sp) == 0) next

  s <- d[idx_sp, , drop = FALSE]
  x_all <- log10(s$source_observed_pcd_days / 365.25)
  y_all <- log10(s$human_observed_pcd_days / 365.25)
  ok_all <- is.finite(x_all) & is.finite(y_all)

  df_full <- safe_df(df_target[[sp]], x_all[ok_all])
  full_fit <- smooth.spline(
    x_all[ok_all],
    y_all[ok_all],
    df = df_full
  )
  full_pred <- predict(full_fit, x_all[ok_all])$y
  rss <- sum((y_all[ok_all] - full_pred)^2)
  tss <- sum((y_all[ok_all] - mean(y_all[ok_all]))^2)
  r2 <- if (tss > 0) 1 - rss / tss else NA_real_

  diagnostics <- rbind(
    diagnostics,
    data.frame(
      source_species = sp,
      target_df = df_target[[sp]],
      full_fit_df_used = df_full,
      n_rows = sum(ok_all),
      n_unique_timepoints = length(unique(s$timepoint[ok_all])),
      n_unique_source_ages = length(unique(x_all[ok_all])),
      full_fit_r_squared_log10 = r2,
      stringsAsFactors = FALSE
    )
  )

  for (tp in unique(s$timepoint)) {
    local_test <- which(s$timepoint == tp)
    local_train <- which(s$timepoint != tp)

    x_train <- log10(s$source_observed_pcd_days[local_train] / 365.25)
    y_train <- log10(s$human_observed_pcd_days[local_train] / 365.25)
    keep <- is.finite(x_train) & is.finite(y_train)
    x_train <- x_train[keep]
    y_train <- y_train[keep]

    if (length(unique(x_train)) < 4) next

    df_use <- safe_df(df_target[[sp]], x_train)
    fit <- tryCatch(
      smooth.spline(x_train, y_train, df = df_use),
      error = function(e) NULL
    )
    if (is.null(fit)) next

    x_test <- log10(s$source_observed_pcd_days[local_test] / 365.25)
    y_test <- log10(s$human_observed_pcd_days[local_test] / 365.25)
    pred <- predict(fit, x_test)$y

    global_rows <- idx_sp[local_test]
    d$A4_event_spline_predicted_human_pcd_y[global_rows] <- 10^pred
    d$A4_event_spline_log10_error[global_rows] <- pred - y_test
    d$A4_event_spline_df_used[global_rows] <- df_use
  }
}

write.csv(d, output_path, row.names = FALSE, na = "")
write.csv(diagnostics, diag_path, row.names = FALSE, na = "")

if (any(is.na(d$A4_event_spline_log10_error))) {
  cat("WARNING: missing A4 predictions:",
      sum(is.na(d$A4_event_spline_log10_error)), "\n")
}
print(diagnostics)
