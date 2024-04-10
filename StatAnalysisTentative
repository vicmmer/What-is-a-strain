#COMP 383 
#Independent project
#Victoria, Adriana, Anmol, Ali

'''
This R script will incorporate th the statistical analysis implementation for 
our project, it will call upon a .tsv file that will be generated following our
ANI analysis and the fragmentation. Utilizing this string (and others like it)
we will compile them as a data frame and compare the dataframes to measure their
differences with one another (we want as low a p-value as possible to preserve
the diversity of our dataset)
'''
#begin implementation by importing/library-ing all necessary packages 
install.packages("tidyverse")
install.packages("readr")
library("readr")

# Define directory path
ani_directory <- "/Users/leahboger/Desktop/Lgasseri_ANI/"

# Define filenames (Still working out how we can implement this aspect into python)
file_names <- c(""))

# Read and process ANI files
ani_data <- list()
for (file_name in file_names) {
  file_path <- paste0(ani_directory, file_name)
  ani <- readr::read_tsv(file_path, col_names = FALSE)
  ani_data[[file_name]] <- data.frame(ani[, 3])
}

# Calculate lengths of ANI vectors
ani_lengths <- sapply(ani_data, length)

# Combine ANI vectors into a single vector
y <- unlist(ani_data)

# Create strain vector
strains <- rep(c("lgasseri10", "lgasseri53", "lgasseri54", "lgasseri56"), each = 25)

# Perform linear regression
l <- lm(y ~ strains)

# Perform ANOVA
anova_result <- anova(l)

# Perform Shapiro-Wilk test
shapiro_result <- shapiro.test(l$residuals)

# Perform Bartlett's test
bartlett_result <- bartlett.test(l$residuals, strains)

# Perform Kruskal-Wallis test
kruskal_result <- kruskal.test(y ~ strains)

# Perform Tukey's HSD test
tukey_result <- TukeyHSD(aov(y ~ strains), conf.level = 0.95)

# Bootstrap
boot <- sample(y, size = 10000, replace = TRUE)
d <- density(boot)

# Read EMP data
testANI <- read.table(pipe("pbpaste"), sep = "\t", header = TRUE)

# Rename columns
testANI$strain_loc1 <- paste(testANI$X, testANI$X.1)
testANI <- testANI %>% select(strain_loc1, X3329_53, X3329_54, X3329_56, X3513_21, X3559_10, X3559_9)
columns <- paste(names(testANI), as.matrix(testANI[1, ]))
colnames(testANI) <- columns
testANI <- testANI[-1, ]
colnames(testANI)[1] <- "strain_loc1"
testANI <- testANI %>% pivot_longer(-strain_loc1, names_to = "strain_loc2", values_to = "ANI")
testANI$ANI <- as.numeric(testANI$ANI)

# Perform permutation test
emp <- rep(0, nrow(testANI))
for (i in 1:nrow(testANI)) {
  emp[i] <- pemp(testANI$ANI[i], boot, discrete = FALSE)
}
t <- cbind(testANI, emp)
write.csv(t, file = paste0(ani_directory, "Lgasseri_emp.csv"))

# Read EMP data again
t <- read.csv(paste0(ani_directory, "Lgasseri_emp.csv")) %>% select(strain_loc1, strain_loc2, ANI, emp)

# Plot density
library(RColorBrewer)
library(ggplot2)
library(dplyr)

cols <- c("LG1" = "#1B9E77", "LG3" = "#D95F02")
g <- df %>% ggplot(aes(x = boot)) + geom_density(fill = "darkgrey", color = "black") +
  geom_vline(aes(xintercept = 99.9985, color = "LG1"), linewidth = 1) +
  geom_vline(aes(xintercept = 99.9990, color = "LG1"), linewidth = 1) +
  geom_vline(aes(xintercept = 99.9995, color = "LG1"), linewidth = 1) +
  geom_vline(aes(xintercept = 99.9986, color = "LG3"), linewidth = 1) +
  geom_vline(aes(xintercept = 99.9986, color = "LG3"), linewidth = 1) +
  ggtitle("Density plot of ANI values for Lgasseri") + xlab("ANI values(bootstrapped)") + ylab("Density") +
  scale_color_manual(name = "Patients", values = cols)

g + theme_bw()
