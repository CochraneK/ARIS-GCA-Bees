#!/usr/bin/env Rscript

# ARIS4C007 Pilot 2A4: leave-one-Timepoint-out pairwise Translating Time spline.
#
# This intentionally uses the authors' raw pairwise spline family from Dataset 1
# but evaluates it out of cluster:
#   Cat -> Human: df = 30
#   Mouse -> Human: df = 12
#   Chimpanzee -> Human: df = 12
#
# Every row sharing the held-out biological Timepoint is excluded from fitting.
# Input is Pilot 2's already-aggregated observed-only strict-heldout event table,
# so no Amelia imputation enters this benchmark.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) {
  stop("Usage: build_pilot2_a4_loto.R observed_event_predictions.csv output.csv")
}

input_path <- args[[1]]
output_path <- args[[2]]

raw <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)

# Use one deterministic copy of each paired event key from the A1 rows.
dat <- subset(
  raw,
  strict_heldout == 1 & method == "A1_relative_lifespan"
)

required <- c(
  "source_species_label", "timepoint", "statistics", "sex", "human_phase",
  "source_pcd_days", "observed_human_pcd_days"
)
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop(paste("Missing columns:", paste(missing, collapse = ", ")))
}

df_map <- c(
  "Felis" = 30,
  "Mus musculus" = 12,
  "Pan troglodytes" = 12
)

results <- list()
out_i <- 1

for (species_name in names(df_map)) {
  sp <- dat[dat$source_species_label == species_name, ]
  if (nrow(sp) == 0) next

  target_df <- unname(df_map[[species_name]])
  timepoints <- sort(unique(sp$timepoint))

  for (tp in timepoints) {
    test <- sp[sp$timepoint == tp, ]
    train <- sp[sp$timepoint != tp, ]

    # Authors fit splines in log10 age space. Division by 365 is retained to
    # mirror the published script; the constant shift itself does not affect
    # fold-error evaluation.
    x_train <- log10(train$source_pcd_days / 365)
    y_train <- log10(train$observed_human_pcd_days / 365)
    x_test <- log10(test$source_pcd_days / 365)

    ok_train <- is.finite(x_train) & is.finite(y_train)
    x_train <- x_train[ok_train]
    y_train <- y_train[ok_train]

    if (length(unique(x_train)) <= target_df + 1) {
      # Should not occur for the current dataset, but fail closed per cluster.
      pred_log <- rep(NA_real_, nrow(test))
      fit_ok <- FALSE
      fit_message <- "insufficient_unique_training_x"
      train_unique_x <- length(unique(x_train))
    } else {
      fit_attempt <- try(
        smooth.spline(x_train, y_train, df = target_df),
        silent = TRUE
      )
      if (inherits(fit_attempt, "try-error")) {
        pred_log <- rep(NA_real_, nrow(test))
        fit_ok <- FALSE
        fit_message <- as.character(fit_attempt)
        train_unique_x <- length(unique(x_train))
      } else {
        pred_attempt <- try(predict(fit_attempt, x_test)$y, silent = TRUE)
        if (inherits(pred_attempt, "try-error")) {
          pred_log <- rep(NA_real_, nrow(test))
          fit_ok <- FALSE
          fit_message <- as.character(pred_attempt)
        } else {
          pred_log <- pred_attempt
          fit_ok <- TRUE
          fit_message <- ""
        }
        train_unique_x <- length(unique(x_train))
      }
    }

    predicted_pcd_days <- (10^pred_log) * 365
    observed_pcd_days <- test$observed_human_pcd_days
    abs_log_error <- abs(log10(predicted_pcd_days) - log10(observed_pcd_days))
    fold_error <- 10^abs_log_error

    train_min <- min(x_train, na.rm = TRUE)
    train_max <- max(x_train, na.rm = TRUE)
    extrapolation <- as.integer(x_test < train_min | x_test > train_max)

    block <- data.frame(
      source_species_label = test$source_species_label,
      timepoint = test$timepoint,
      statistics = test$statistics,
      sex = test$sex,
      human_phase = test$human_phase,
      source_pcd_days = test$source_pcd_days,
      observed_human_pcd_days = observed_pcd_days,
      method = "A4_pairwise_spline_LOTO",
      author_pairwise_df = target_df,
      training_event_rows = nrow(train),
      training_unique_timepoints = length(unique(train$timepoint)),
      training_unique_source_ages = train_unique_x,
      extrapolation = extrapolation,
      fit_ok = as.integer(fit_ok),
      fit_message = fit_message,
      predicted_human_pcd_days = predicted_pcd_days,
      absolute_log10_pcd_error = abs_log_error,
      fold_error = fold_error,
      stringsAsFactors = FALSE
    )

    results[[out_i]] <- block
    out_i <- out_i + 1
  }
}

out <- do.call(rbind, results)
dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)
write.csv(out, output_path, row.names = FALSE, quote = TRUE)

cat("A4 LOTO rows:", nrow(out), "\n")
cat("Successful fits:", sum(out$fit_ok == 1), "\n")
cat("Extrapolation rows:", sum(out$extrapolation == 1, na.rm = TRUE), "\n")

for (sp in unique(out$source_species_label)) {
  x <- out[out$source_species_label == sp & out$fit_ok == 1, ]
  cat(
    sp,
    "n=", nrow(x),
    "median_abs_log10_error=", median(x$absolute_log10_pcd_error, na.rm = TRUE),
    "median_fold_error=", median(x$fold_error, na.rm = TRUE),
    "\n"
  )
}
