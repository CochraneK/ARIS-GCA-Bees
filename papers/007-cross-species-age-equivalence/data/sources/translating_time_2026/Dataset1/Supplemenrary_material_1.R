### Translating ages across species. This script is part of
### Januel C, Morrow E, Gibson R, Gross A, de Sousa AA, Dames BA, Charvet CJ. Cat brains age like humans: Translating Time shows pet cats live to be natural models for human aging. Biology Open. 2026 May 18:bio-062604.

## libraries
library(dplyr)
library(readxl)
library(tidyverse)
library(Amelia)
library(corrplot)
library(stringi)
library(splines)

### Open table S1 and call it dataset_breed1  ###

# R.version.string: "R version 4.1.1 (2021-08-10); Platform: x86_64-apple-darwin17.0 (64-bit); Running under: macOS 15.7.4"
# sessionInfo(): Amelia_1.8.1 --I have had issues with Amelia, which may have to do with the use of different R versions.

dataset_breed1<-Table_S1 ## call Table_S1 dataset_breed1

dataset_breed1<-as.data.frame(dataset_breed1)
dataset_breed2<-cbind.data.frame(dataset_breed1[ ,1:6])
dim(dataset_breed2)

# Reorganize the data frame. Here, we average by species, time point and sex.
df_subset <- dataset_breed2 %>%
  group_by(Species, Timepoint, Statistics, Sex) %>%
  mutate(row_id = row_number()) %>%
  ungroup()

# Clean invisible characters from column R.
df_subset$Timepoint <- stri_trim_both(
  stri_replace_all_regex(
    df_subset$Timepoint,
    pattern = "[\\p{C}\\x{00A0}\\x{200B}-\\x{200D}\\x{2060}\\x{FEFF}]",
    replacement = ""
  )
)

# Pivot the dataset, which restructures the dataset.
pivoted_data <- df_subset %>%
  group_by(Timepoint, Statistics, Species, Sex) %>%
  summarise(mean_PCD = mean(PCD, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(
    names_from = Species,
    values_from = mean_PCD
  )

## Plot observations in humans versus cats
plot(pivoted_data$Felis, pivoted_data$`Homo sapiens`, col="cornflowerblue",
     log="xy", pch=16)
length(na.omit(pivoted_data$Felis))

## Plot observations in chimpanzees versus humans
plot(pivoted_data$`Pan troglodytes`, pivoted_data$`Homo sapiens`, col="cornflowerblue",
     log="xy", pch=16)

## Organize the data
pivoted_data$Statistics<-as.numeric(pivoted_data$Statistics)

pivoted_data1<-cbind.data.frame(pivoted_data$Timepoint, pivoted_data$Statistics, pivoted_data$Sex,
                               log10(pivoted_data$Felis), 
                                log10(pivoted_data$`Homo sapiens`),
                                log10(pivoted_data$`Mus musculus`), 
                                log10(pivoted_data$`Pan troglodytes`))
colnames(pivoted_data1)<-c("Timepoint", "Statistics",  "Sex",
                           "Cat", "Homo", "Mouse", "Chimp") 
pivoted_data1$Statistics<-as.numeric(pivoted_data1$Statistics)

head(pivoted_data1) ## take a lookg at the data
## Quantify the number of NAs per row
pivoted_data1$na <- apply(pivoted_data1[ ,4:7], 1, function(x) sum(is.na(x)))
pivoted_data1$na<-as.numeric(pivoted_data1$na)
hist(pivoted_data1$na)
head(pivoted_data1)

## Filter the dataset based on NAs
pivoted_data1<-subset(pivoted_data1, na<3)
pivoted_data1$na<-NULL
head(pivoted_data1)

## Make sure sex selective traits are sex selective
pivoted_data1 <- pivoted_data1 %>%
  filter(!(Timepoint == "Female First reproduction (sex selective)" & Sex == "Male+Female"))

pivoted_data1 <- pivoted_data1 %>%
  filter(!(Timepoint == "Female Sexual maturity is reached (sex selective)" & Sex == "Male+Female"))

pivoted_data1 <- pivoted_data1 %>%
  filter(!(Timepoint == "Male Sexual maturity is reached (sex selective)" & Sex == "Male+Female"))

## Make sure that the variable is numeric
pivoted_data1$Statistics<-as.character(pivoted_data1$Statistics) ## CHANGE CHARACTER AS NUMERIC
#clean_data<-pivoted_data1

## Bound the possible ages for the generation of age translations
bounds1 <- matrix(c(
  4, log10(0.001), log10(30*365+65),   # Cat
  5, log10(0.001), log10(122.5*365+270),  # Homo
  6, log10(0.001), log10(4.0*365+18.5),  # Mouse
  7, log10(0.001), log10(68*365+243)    # Chimp
), ncol = 3, byrow = TRUE)

pivoted_data1$Timepoint<-as.character(pivoted_data1$Timepoint)
pivoted_data1$Statistics<-as.character(pivoted_data1$Statistics)

## Impute the data using Amelia
set.seed(123)
pivoted_data1<-as.data.frame(pivoted_data1)

head(pivoted_data1)
tryCatch({
  imputed_data1 <- amelia(pivoted_data1, m = 10, idvars = c("Timepoint", "Sex", "Statistics"), parallel = "no",  
                          bounds = bounds1,
                          )
}, error = function(e) {
  cat("Amelia crashed:", conditionMessage(e), "\n")
})

summary(imputed_data1)
imputed_data1$imputations$imp1

## find the correlation with highest correlation coefficient
for (i in 1:10) {
completed_data1<-imputed_data1$imputations[[i]]
cor_matrix1 <- cor(completed_data1[ ,4:7], use = "complete.obs", method = "pearson")
hist(cor_matrix1)
print(i)
print(min(cor_matrix1))
}
## select an imputed dataset:
completed_data1<-imputed_data1$imputations[[10]]

completed_data1$Statistics<-pivoted_data1$Statistics
pivoted_data1$Statistics<-as.character(pivoted_data1$Statistics)
  
averaged_df <- completed_data1 %>%
  group_by(Timepoint, Statistics, Sex) %>%
  summarize(across(where(is.numeric), ~ mean(.x, na.rm = TRUE)), .groups = "drop")

averaged_df_raw <- pivoted_data1 %>%
  group_by(Timepoint, Statistics, Sex) %>%
  summarize(across(where(is.numeric), ~ mean(.x, na.rm = TRUE)), .groups = "drop")

## Open Table S2 to look at breakdown of data and call it table S2 ##
head(Table_S2) 

## show different kinds of data (Figure 1)
head(Table_S2); colnames(Table_S2)
Table_S2$Cat<-as.numeric(Table_S2$Cat)
Table_S2$Homo<-as.numeric(Table_S2$Homo)

plot(10^Table_S2$Cat/365, 10^Table_S2$Homo/365, log="xy", 
     col="cornflowerblue", pch=16, xlab="Cat (years post-conception)",
  ylab="Human (years post-conception)", cex=1.5, cex.lab=1.5, cex.axis=1.5)
MRI<-subset(Table_S2, MRI_this_study==1)
head(MRI); dim(MRI)
points(10^MRI$Cat/365, 10^MRI$Homo/365, col="darkred", cex=1.5, pch=16)
Disease<-subset(Table_S2, Disease==1)
head(MRI); dim(MRI)
points(10^Disease$Cat/365, 10^Disease$Homo/365, col="rosybrown2", cex=1.5, pch=16)
Bone<-subset(Table_S2, Bone_ossification==1)
points(10^Bone$Cat/365, 10^Bone$Homo/365, col="plum4", pch=16, cex=1.5,)
Behavior<-subset(Table_S2, `Behavioral milestones`==1)
points(10^Behavior$Cat/365, 10^Behavior$Homo/365, col="palegreen3", cex=1.5, pch=16)
Anatomy<-subset(Table_S2, `Abrupt anatomical changes (not ossification)`==1)
points(10^Anatomy$Cat/365, 10^Anatomy$Homo/365, col="antiquewhite4", cex=1.5, pch=16)
Blood_work<-subset(Table_S2, `Blood work`==1)
points(10^Blood_work$Cat/365, 10^Blood_work$Homo/365, col="deepskyblue4", cex=1.5, pch=16)
legend("bottomright", legend=c("MRI", "Diseases", 
                            "Bone ossification", "Behavioral milestones",
                            "Anatomy", "Blood work"), 
       col=c("darkred", "rosybrown2", 
             "plum4", "palegreen3", "antiquewhite4", "deepskyblue4"), 
       pch=16, bty="n", pt.cex=1.25, cex=0.5)


# Boxplot (Figure 1)
options(scipen = 999)
boxplot(10^averaged_df_raw$Mouse/365, 10^averaged_df_raw$Cat/365, 
        10^averaged_df_raw$Chimp/365, 10^averaged_df_raw$Homo/365, log="y", 
        cex.axis=1.6, cex.lab = 1.6, ylab="Age of observations in years",
        col=c("grey", "cornflowerblue", "plum4", "darkred"))

#plot(10^averaged_df$Cat/365, 10^averaged_df$Homo/365, log="xy", col="cornflowerblue", pch=16)

### compare humans versus cats
plot(10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365, log="xy", col="cornflowerblue", pch=16,
     xlab="Cats (years post-conception)", ylab="Human (years post-conception)",
     cex.lab=1.5, cex.axis=1.5)
head(averaged_df_raw)
c1<-cbind.data.frame(10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365)
c1<-na.omit(c1)
df<-smooth.spline(log10(c1[ ,1]), log10(c1[ ,2]), df=30)
x<-c(10, 16, 1, 65/365, 30/365, 365)
lines(10^df$x, 10^df$y, col="cornflowerblue", lwd=2)
ABC<-as.data.frame(predict(df, log10(x)))
abline(h=10^ABC$y, col="cornflowerblue", lty=2)
abline(v=x, col="cornflowerblue", lty=2)

## Relative amount of data in dataset (Figure 1)
pie<-c(7.356076759,	1.918976546,	24.41364606,	4.371002132,	2.23880597,
       11.08742004,	4.690831557,	19.7228145,	100*39/938, 100*0.255689424)
labels<-c("Blood work", "MRI", "Bone ossification", "Tooth eruption",
          "Disease", "Behavioral milestone", "Transcription", "Anatomical changes",
          "Neurogenesis", "Other")
bg_colors <- c("cornflowerblue", "antiquewhite3", "pink4", "steelblue", 
               "plum3", "grey", 
               "plum4", "antiquewhite4", "plum2", "pink4", "pink2", "grey")
pie(pie, labels=labels)

#############################################################################

########### Compare age translations with and without cat MRI data (Figure S1)

#############################################################################

dev.off()
plot(10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365, log="xy", col="darkred", pch=16,
     xlab="Cats (years post-conception)", ylab="Human (years post-conception)",
     cex.lab=1.5, cex.axis=1.5)

MRI <- paste(c("interthalamic adhesion", "normalized whole brain volume \\(nWBV\\)"), collapse = "|")

# Filter out the matching rows
df_no_mri <- averaged_df_raw %>%
  filter(!stringr::str_detect(Timepoint, MRI))
dim(df_no_mri); dim(averaged_df_raw)

points(10^df_no_mri$Cat/365, 10^df_no_mri$Homo/365, col="cornflowerblue", pch=16)
d1<-cbind.data.frame(10^df_no_mri$Cat/365, 10^df_no_mri$Homo/365)
d1<-na.omit(d1)

df_nomri<-smooth.spline(log10(d1[ ,1]), log10(d1[ ,2]), df=30)

###################################################################

### Calculate the % of variance explained by the model
# Extract fitted values from the smooth spline,  Ensure predictions are made correctly
fitted_values <- predict(df_nomri, log10(d1[ ,1]))$y
log_observed_values <- log10(d1[, 2])

# Calculate residuals
residuals <- log_observed_values - fitted_values

# Calculate residual sum of squares
rss <- sum(residuals^2)

# Calculate total sum of squares
mean_y <- mean(log_observed_values)
tss <- sum((log_observed_values - mean_y)^2)

# Calculate R-squared
r_squared <- 1 - (rss / tss)
r_squared

##### We fit prediction intervals (original smooth spline with spar = 0.9)
da <- smooth.spline(log10(d1[, 1]), log10(d1[, 2]), spar = 0.9)
original_predictions <- predict(da, log10(d1[, 1]))

# Calculate residuals for observation variability (model error)
residuals <- log10(d1[, 2]) - original_predictions$y
residual_sd <- sd(residuals)  # Standard deviation of residuals for prediction error

# Set up bootstrap parameters
set.seed(123)  # For reproducibility
n_bootstrap <- 1000  # Number of bootstrap samples
x_vals <- log10(d1[, 1])  # x values in log scale for prediction
bootstrap_predictions <- matrix(NA, nrow = length(x_vals), ncol = n_bootstrap)

# Bootstrap loop
for (i in 1:n_bootstrap) {
  # Resample the data with replacement
  boot_indices <- sample(seq_along(d1[, 1]), replace = TRUE)
  H1_boot <- d1[boot_indices, ]
  
  # Fit a smooth spline to the bootstrap sample
  da_boot <- smooth.spline(log10(H1_boot[, 1]), log10(H1_boot[, 2]), spar = 0.9)
  
  # Predict using the bootstrap spline
  boot_prediction <- predict(da_boot, x_vals)$y
  
  # Add random noise to capture observation variability
  bootstrap_predictions[, i] <- boot_prediction + rnorm(length(x_vals), mean = 0, sd = residual_sd)
}

# Calculate ±1 Standard Error Interval from bootstrap predictions
standard_error <- apply(bootstrap_predictions, 1, sd)
se_lower_bound <- original_predictions$y - standard_error
se_upper_bound <- original_predictions$y + standard_error

# Calculate the 95% Prediction Interval from bootstrap predictions
lower_bound_95 <- apply(bootstrap_predictions, 1, quantile, probs = 0.025)
upper_bound_95 <- apply(bootstrap_predictions, 1, quantile, probs = 0.975)

# Sort values for plotting
sorted_indices <- order(original_predictions$x)
sorted_x <- original_predictions$x[sorted_indices]
sorted_y <- original_predictions$y[sorted_indices]
sorted_se_upper <- se_upper_bound[sorted_indices]
sorted_se_lower <- se_lower_bound[sorted_indices]
sorted_upper_95 <- upper_bound_95[sorted_indices]
sorted_lower_95 <- lower_bound_95[sorted_indices]

# Add the original smooth spline line
lines(10^sorted_x, 10^sorted_y, col = "black", lwd = 2)

# Add the ±1 SE interval band (narrower)
polygon(c(10^sorted_x, rev(10^sorted_x)), c(10^sorted_se_upper, rev(10^sorted_se_lower)), 
        col = rgb(0, 0, 1, alpha = 0.2), border = NA)  # Light blue shading for ±1 SE

##################################################################
### Plots to compare data in humans versus cats
plot(10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365,
     col="cornflowerblue", pch=16, xlim=c(0.03, 50), ylim=c(0.03, 100), log="xy",
   xlab="Cat (years post-conception)",  cex.lab=1.75, cex.axis=1.75, 
     ylab="Human (years post-conception)")
with(averaged_df_raw, {
  ok <- !is.na(Cat) & !is.na(Homo)
  x <- Cat[ok]
  y <- Homo[ok]
  fit <- smooth.spline(x, y, df = 10)
  x<-c(15/365, 30/365, 65/365, 0.5, 1, 5, 8, 15)
  A<-predict(fit, log10(x*365))$y
  abline(h=10^A/365, lty=2)
  Age<-predict(fit, x)$y
  print(10^A/365)
  abline(v=x, lty=2)
  lines(10^fit$x/365, 10^fit$y/365, col = "cornflowerblue", lwd = 2)
})

## Figure 7. Plot chimpanzee versus cat data
options(scipen = 999)
plot(10^averaged_df_raw$Chimp/365, 10^averaged_df_raw$Cat/365, 
     col="darkgrey", pch=16,  log="xy", ylim=c(0.04, 18), xlim=c(0.17, 50),
     xlab="Chimpanzee (years post-conception)", 
     ylab="Cat (years post-conception)", cex.lab=1.75, cex.axis=1.75)  #log="xy", 
with(averaged_df_raw, {
  ok <- !is.na(Chimp) & !is.na(Cat)
  x <- Chimp[ok]
  y <- Cat[ok]
  fit <- smooth.spline(x, y, df = 12)
  x<-c(243/365, 10, 35)
  A<-predict(fit, log10(x*365))$y
  abline(h=10^A/365, lty=2)
  Age<-predict(fit, x)$y
  print(10^A/365)
  abline(v=x, lty=2)
  lines(10^fit$x/365, 10^fit$y/365, col = "black", lwd = 2)
})

### Figure 7. Plot mouse versus cat data
options(scipen = 999)
plot(10^averaged_df_raw$Mouse/365, 10^averaged_df_raw$Cat/365, 
     col="darkgrey", pch=16,  log="xy", 
     ylab="Cat (years post-conception)", 
     xlab="Mouse (years post-conception)", cex.lab=1.75, cex.axis=1.75)  #log="xy", 
with(averaged_df_raw, {
  ok <- !is.na(Mouse) & !is.na(Cat)
  x <- Mouse[ok]
  y <- Cat[ok]
  fit <- smooth.spline(x, y, df = 12)
  x<-c(18.5/365, 0.5, 1, 1.5)
  A<-predict(fit, log10(x*365))$y
  abline(h=10^A/365, lty=2)
  Age<-predict(fit, x)$y
  print(10^A/365)
  abline(v=x, lty=2)
  lines(10^fit$x/365, 10^fit$y/365, col = "black", lwd = 2)
})

### Plot mouse versus human data
options(scipen = 999)
plot(10^averaged_df_raw$Mouse/365, 10^averaged_df_raw$Homo/365, 
     col="darkgrey", pch=16,  log="xy", 
     xlab="Mouse (years post-conception)", 
     ylab="Human (years post-conception)", cex.lab=1.75, cex.axis=1.75)  #log="xy", 
with(averaged_df_raw, {
  ok <- !is.na(Mouse) & !is.na(Homo)
  x <- Mouse[ok]
  y <- Homo[ok]
  fit <- smooth.spline(x, y, df = 12)
  x<-c(18.5/365, 1, 1.5)
  A<-predict(fit, log10(x*365))$y
  abline(h=10^A/365, lty=2)
  Age<-predict(fit, x)$y
  print(10^A/365)
  abline(v=x, lty=2)
  lines(10^fit$x/365, 10^fit$y/365, col = "black", lwd = 2)
})

### Plot chimpanzee versus human data
options(scipen = 999)
plot(10^averaged_df_raw$Chimp/365, 10^averaged_df_raw$Homo/365, 
     col="darkgrey", pch=16,  log="xy", xlim=c(0.08, 100), ylim=c(0.08, 100),
     ylab="Human (years post-conception)", cex.lab=1.75, cex.axis=1.75,
     xlab="Chimpanzee (years post-conception)", cex.lab=1.5, cex.axis=1.5)  #log="xy", 
with(averaged_df_raw, {
  ok <- !is.na(Chimp) & !is.na(Homo)
  x <- Chimp[ok]
  y <- Homo[ok]
  fit <- smooth.spline(x, y, df = 12)
  x<-c(243/365, 10, 40)
  A<-predict(fit, log10(x*365))$y
  abline(h=10^A/365, lty=2)
  Age<-predict(fit, x)$y
  print(10^A/365)
  abline(v=x, lty=2)
  lines(10^fit$x/365, 10^fit$y/365, col = "black", lwd = 2)
})

summary(imputed_data1)
weights<-c(0.5309168, 0.2046908, 0.5831557, 0.4413646)
barplot(weights, col=c("cornflowerblue", "darkred", "grey", "plum4"),
        ylim=c(0, 1), cex.lab=3, cex.axis=3)

## create a variable
events<-averaged_df[ ,4:7]

####################################################################################
############################ Use PCA to denoise the data ############################ 
#####################################################################################

# 1. Scale the data
numeric_data <- events[, sapply(events, is.numeric)]
scaled_data <- scale(numeric_data)
scaled_center <- attr(scaled_data, "scaled:center")
scaled_scale <- attr(scaled_data, "scaled:scale")

# 2. PCA
pca <- prcomp(scaled_data, center = TRUE, scale. = TRUE)

# 3. Dimensionality reduction + denoising
reduced <- pca$x[, 1:2] %*% t(pca$rotation[, 1:2])  # back to scaled space (approx)

# 4. Inverse scale: from scaled back to original numeric values
denoised_matrix <- sweep(reduced, 2, scaled_scale, "*")
denoised_matrix <- sweep(denoised_matrix, 2, scaled_center, "+")

# 5. Convert to data frame
denoised_df <- as.data.frame(denoised_matrix)

## compare denoised with non-denoised
plot(averaged_df$Cat, averaged_df$Homo)
plot(denoised_df$Cat, denoised_df$Homo)

## Compare imputed versus observed values
plot(10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365, cex=0.5, xlab="Age in years cats",
     ylab="Age in years Humans", log="xy", cex.lab=2.5, cex.axis=2.5)
points(10^denoised_df$Cat/365, 10^denoised_df$Homo/365, col="grey", cex=0.75, pch=16)
points (10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365, col="cornflowerblue", pch=16)

averaged_df1<-cbind.data.frame(averaged_df[ ,1:3], denoised_df)

######## Compute an event scale
head(averaged_df1)
Event_scale <- as.data.frame(apply(averaged_df1[ ,4:7], 1, function(row) {
  not_na <- !is.na(row)
  sum(row[not_na] * weights[not_na]) / sum(weights[not_na])
}))

## Visualize distribution of observations before transforming it into an event scale
head(Event_scale)
colnames(Event_scale)<-c("Event_scale")
hist(Event_scale$Event_scale)

## Generate the event scale
Event_scale$Event_scale<-as.numeric(Event_scale$Event_scale)
min<-min(Event_scale$Event_scale, na.rm=TRUE)
max<-max(Event_scale$Event_scale, na.rm=TRUE)
Event_scale1<-(Event_scale$Event_scale-min)/(max-min)
Event_scale1<-as.data.frame(Event_scale1)

compare<-cbind(Event_scale1, averaged_df_raw)
compare1<-cbind(Event_scale1, averaged_df)

## plot data versus event scale
options(scipen = 100)
plot(Event_scale1[ ,1], 10^averaged_df_raw$Homo/365, log="y", ylab="Age in years post-conception",
     xlab="Event scale", cex=1.5, pch=16, cex.axis=1.1)
points(Event_scale1[ ,1], 10^averaged_df_raw$Chimp/365, col="purple", pch=16, cex=1.1)
points(Event_scale1[ ,1], 10^averaged_df_raw$Mouse/365, col="red", pch=16, cex=1.1)
points(Event_scale1[ ,1], 10^averaged_df_raw$Cat/365, col="cornflowerblue", pch=16, cex=1.1)

dim(Event_scale1)
plot(Event_scale1[ ,1], 10^averaged_df_raw$Homo/365)
points(Event_scale1[ ,1], 10^averaged_df_raw$Chimp/365, col="purple")
points(Event_scale1[ ,1], 10^averaged_df_raw$Mouse/365, col="red")
points(Event_scale1[ ,1], 10^averaged_df_raw$Cat/365, col="gold")

##### make more plots to visualize the data
colnames(averaged_df_raw)
head(averaged_df_raw)
df_transformed <- as.data.frame(10^averaged_df_raw[ ,4:7])

head(df_transformed)
plot(df_transformed$Cat, df_transformed$Homo)

# Add the event scale as a new column
df_transformed$EventScale <- Event_scale1[,1]

# Move EventScale to the first column (optional but tidy)
df_transformed <- df_transformed %>%
  relocate(EventScale)

# Convert from wide to long format
df_long <- df_transformed %>%
  pivot_longer(
    cols = -EventScale,
    names_to = "Species",
    values_to = "Value"
  )

## fit a general linear model
str(df_long)

df_long$square<-df_long$EventScale^2
df_long$cube<-df_long$EventScale^3
df_long$quatro<-df_long$EventScale^4

## Get min and max of EventScale
range_vals <- range(df_long$EventScale, na.rm = TRUE)

## Fit a smooth spline
fit_spline <- lm(log10(Value) ~ Species * ns(EventScale, df = 5), data = df_long, na.action = na.exclude)

summary(fit_spline)  ## summary of model
df_long$Predicted <- predict(fit_spline)

head(df_long) ## take a look at the data

## Plot the output of the model
species_colors <- c(
  "Homo" = "darkred",
  "Chimp" = "plum4",
  "Cat" = "cornflowerblue",
  "Mouse" = "black"
)

## Check if there are other species and assign a default color if needed
all_species <- unique(df_long$Species)
missing_species <- setdiff(all_species, names(species_colors))
if (length(missing_species) > 0) {
  # Assign remaining species a default color (e.g., grey)
  default_colors <- rep("grey", length(missing_species))
  names(default_colors) <- missing_species
  species_colors <- c(species_colors, default_colors)
}

## Map species to colors
point_colors <- species_colors[df_long$Species]
point_colors

head(df_long)
## Plot predicted values
plot(df_long$EventScale, 10^df_long$Predicted/365, 
     xlab = "Event Scale", ylab = "Predicted / log10(Value)", pch=16, log="y",
     col = point_colors, main = "Predicted vs log10(Value) by Species",
     xlim=c(0, 1.1))
points(df_long$EventScale, df_long$Value/365, col = point_colors, cex=0.6)

df_long$years<-df_long$Value/365
df_long1<-cbind.data.frame(df_long$EventScale, df_long$Species, 10^df_long$Predicted/365, df_long$Value/365)

## plot predicted and observed values
plot(df_long$EventScale, 10^df_long$Predicted/365, 
     xlab = "Event Scale", ylab = "Predicted / log10(Value)", pch=16,
     col = point_colors, main = "Predicted vs log10(Value) by Species")
points(df_long$EventScale, df_long$Value/365, col = point_colors, cex=0.75)
legend("topleft", legend = names(species_colors), col = species_colors, pch = 16, title = "Species", cex=0.75)

########################################################################

### Compare predicted values from the model with observations (Figure S2)

########################################################################
## organize the data
df1<-cbind.data.frame(df_long$EventScale, df_long$Species, df_long$Predicted)
head(df1)
colnames(df1)<-c("Eventscale", "Species", "Predicted")

## pivot the data
matched_df <- df1 %>%
  pivot_wider(
    names_from = Species,      # Column with "cat" or "human"
    values_from = Predicted  # Column with the numbers
  )
head(matched_df) ## take a look at the data

### Compare cats with humans
plot(10^matched_df$Cat/365, 10^matched_df$Homo/365, xlim=c(0.02, 20), ylim=c(0.02, 100), 
     log="xy", col="darkred", pch=16, cex=1.5, xlab="Cats (years post-conception)", 
     ylab="Human (years post-conception)", cex.lab=1.25, cex.axis=1.25)
points(10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365, col="cornflowerblue", pch=16)

### Calculate the % of variance explained by the model
head(averaged_df_raw)
d1_total<-cbind.data.frame(10^averaged_df_raw$Cat/365, 10^averaged_df_raw$Homo/365)
d1_total<-na.omit(d1_total)
df_total1<-smooth.spline(log10(d1_total[ ,1]), log10(d1_total[ ,2]), df=30)

fitted_values <- predict(df_total1, log10(d1_total[ ,1]))$y
log_observed_values <- log10(d1_total[, 2])

# Calculate residuals
residuals <- log_observed_values - fitted_values

# Calculate residual sum of squares
rss <- sum(residuals^2)

# Calculate total sum of squares
mean_y <- mean(log_observed_values)
tss <- sum((log_observed_values - mean_y)^2)

# Calculate R-squared
r_squared <- 1 - (rss / tss)
r_squared

# Fit the original smooth spline with spar = 0.9
da <- smooth.spline(log10(d1_total[, 1]), log10(d1_total[, 2]), spar = 0.9)
original_predictions <- predict(da, log10(d1_total[, 1]))
dim(d1_total)
# Calculate residuals for observation variability (model error)
residuals <- log10(d1_total[, 2]) - original_predictions$y
residual_sd <- sd(residuals)  # Standard deviation of residuals for prediction error
# Set up bootstrap parameters
set.seed(123)  # For reproducibility
n_bootstrap <- 1000  # Number of bootstrap samples
x_vals <- log10(d1[, 1])  # x values in log scale for prediction
bootstrap_predictions <- matrix(NA, nrow = length(x_vals), ncol = n_bootstrap)

# Bootstrap loop
for (i in 1:n_bootstrap) {
  # Resample the data with replacement
  boot_indices <- sample(seq_along(d1[, 1]), replace = TRUE)
  H1_boot <- d1[boot_indices, ]
  
  # Fit a smooth spline to the bootstrap sample
  da_boot <- smooth.spline(log10(H1_boot[, 1]), log10(H1_boot[, 2]), spar = 0.9)
  
  # Predict using the bootstrap spline
  boot_prediction <- predict(da_boot, x_vals)$y
  
  # Add random noise to capture observation variability
  bootstrap_predictions[, i] <- boot_prediction + rnorm(length(x_vals), mean = 0, sd = residual_sd)
}

# Calculate ±1 Standard Error Interval from bootstrap predictions
standard_error <- apply(bootstrap_predictions, 1, sd)
se_lower_bound <- original_predictions$y - standard_error
se_upper_bound <- original_predictions$y + standard_error

# Calculate the 95% Prediction Interval from bootstrap predictions
lower_bound_95 <- apply(bootstrap_predictions, 1, quantile, probs = 0.025)
upper_bound_95 <- apply(bootstrap_predictions, 1, quantile, probs = 0.975)

# Sort values for plotting
sorted_indices <- order(original_predictions$x)
sorted_x <- original_predictions$x[sorted_indices]
sorted_y <- original_predictions$y[sorted_indices]
sorted_se_upper <- se_upper_bound[sorted_indices]
sorted_se_lower <- se_lower_bound[sorted_indices]
sorted_upper_95 <- upper_bound_95[sorted_indices]
sorted_lower_95 <- lower_bound_95[sorted_indices]

# Add the original smooth spline line
lines(10^sorted_x, 10^sorted_y, col = "black", lwd = 2)

# Add the ±1 SE interval band (narrower)
polygon(c(10^sorted_x, rev(10^sorted_x)), c(10^sorted_se_upper, rev(10^sorted_se_lower)), 
        col = rgb(0, 0, 1, alpha = 0.25),  border = NA)  # Light blue shading for ±1 SE


