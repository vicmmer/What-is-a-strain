#COMP 383 
#Independent project: What is a Strain? Short Read Group
#Victoria, Adriana, Anmol, Ali

'''
This R script will incorporate th the statistical analysis implementation for 
our project, it will call upon a .tsv file that will be generated following our
ANI analysis and the fragmentation. Utilizing this string (and others like it)
we will compile them as a data frame and compare the dataframes to measure their
differences with one another (we want as low a p-value as possible to preserve
the diversity of our dataset)

Please refer to the github for specific direction regarding all steps prior to 
this stage that will allow you to generate a total of three (3) tsv files.
One labled mixed.tsv, and then two others corresponding to each strain and 
labelled by the SRA accession number. For the statistical test portion of this
analysis, the mixed.tsv file will be utilized.
'''
#begin implementation by importing/library-ing all necessary packages 

library(readr)
library(dplyr)
library(ggplot2)

#statistical analysis of the MIXED.tsv file generated, do before#

# Read in all your TSV files
file_path_mixed <- "/cloud/project/mixed.tsv"  # Replace with your actual file path
file_path_strain1 <- "/cloud/project/SRR26772099.tsv" # Replace with your actual file path
file_path_strain2 <- "/cloud/project/SRR26772116.tsv" # Replace with your actual file path

ani_data1 <- read_tsv(file_path_mixed, col_names = FALSE)

#Convert X1 and X2 to factors
ani_data$X1 <- factor(ani_data$X1)
ani_data$X2 <- factor(ani_data$X2)

# Run linear regression
l <- lm(ani_data1$X3 ~ ani_data1$X2)

# Perform ANOVA on residuals
anova_resid <- anova(l)
p_value_anova_resid <- anova_resid$"Pr(>F)"[1]
print(p_value_anova_resid)

# Shapiro-Wilk test on residuals
shapiro_resid <- shapiro.test(l$residuals)
p_value_shapiro_resid <- shapiro_resid$p.value
print(p_value_shapiro_resid)

# Bartlett's test comparing residuals to factor
bartlett_resid_factor <-  bartlett.test(l$resid, ani_data1$X2)
p_value_bartlett <- bartlett_resid_factor$p.value
print(p_value_bartlett)

# Kruskal-Wallis test comparing ANI values to factor variable
kruskal_test_result <- kruskal.test(ani_data1$X3 ~ ani_data1$X2)
p_value_kruskal <- kruskal_test_result$p.value
print(p_value_kruskal)

###########
##Boot-strapped analysis to generate density plots##
# Read the two strain TSV files (the mixed.tsv file has already been read)
# Set file path to your respective working directory containing your files

file_path_strain1 <- "/cloud/project/SRR26772099.tsv" # Replace with your actual file path
file_path_strain2 <- "/cloud/project/SRR26772116.tsv" # Replace with your actual file path

ani_data1 <- read_tsv(file_path_mixed, col_names = FALSE)
ani_data2 <- read_tsv(file_path_strain1, col_names = FALSE)
ani_data3 <- read_tsv(file_path_strain2, col_names = FALSE)

# Combine ANI values into a single vector
ani_values <- c(ani_data2$X3, ani_data3$X3)

# Bootstrap resampling
bootstrapped_ani <- replicate(10000, sample(ani_values, replace = TRUE))

# Convert bootstrapped_ani matrix to a data frame
boot_df <- as.data.frame(bootstrapped_ani)

# Melt the data frame to long format for ggplot
boot_df_long <- reshape2::melt(boot_df)

# Plot density of bootstrapped ANI values
ggplot(boot_df_long, aes(x = value)) +
  geom_density(fill = "gray", alpha = 0.5) +
  labs(title = "Density Plot of Bootstrapped ANI Values", x = "ANI Values", y = "Density") +
  theme_minimal()

#Raw non-bootstrapped analysis, use only to compare strain ANI similarities rudimentarily###

# Combine the ANI values into a single dataset
ani_values <- bind_rows(
  data.frame(ANI = ani_data1$X3, Source = "Mixed"),
  data.frame(ANI = ani_data2$X3, Source = "SRR26772099"),
  data.frame(ANI = ani_data3$X3, Source = "SRR26772116")
)

# Plot the density of ANI values
ggplot(ani_values, aes(x = ANI, fill = Source)) +
  geom_density(alpha = 0.25) +
  labs(title = "Density Plot of ANI Values", x = "ANI Values", y = "Density") +
  theme_minimal()

