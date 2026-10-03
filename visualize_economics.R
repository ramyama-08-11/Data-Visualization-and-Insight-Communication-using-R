library(ggplot2)
library(dplyr)
library(lubridate)
library(scales)

# Create output directory
output_dir <- file.path(getwd(), "output")
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Publicly available US economic trends dataset from ggplot2 package
# Source: ggplot2::economics
# Description: Monthly economic indicators from 1967-2015

econ <- ggplot2::economics %>%
  mutate(
    year = as.integer(format(date, "%Y")),
    month = month(date, label = TRUE),
    unemploy_thousands = unemploy / 1000,
    population_millions = pop / 1000000
  )

# Plot 1: long-term trend in unemployment and household savings
plot1 <- ggplot(econ, aes(x = date)) +
  geom_line(aes(y = unemploy_thousands, color = "Unemployed persons"), linewidth = 1.1) +
  geom_line(aes(y = psavert * 10, color = "Savings rate x10"), linewidth = 1.1, linetype = "dashed") +
  scale_y_continuous(
    name = "Unemployed persons (thousands)",
    sec.axis = sec_axis(~ . / 10, name = "Savings rate (%)")
  ) +
  scale_color_manual(values = c("Unemployed persons" = "#1f77b4", "Savings rate x10" = "#d62728")) +
  labs(
    title = "Economic Stress and Household Savings Trends",
    subtitle = "US unemployment compared with personal savings rate, 1967–2015",
    x = "Year",
    y = "Unemployed persons (thousands)",
    color = "Series"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 16),
    legend.position = "bottom",
    axis.title.y.right = element_text(color = "#d62728")
  )

ggsave(file.path(output_dir, "plot1_economic_trends.png"), plot1, width = 10, height = 6, dpi = 300)

# Plot 2: scatter plot of unemployment duration against savings rate
plot2 <- ggplot(econ, aes(x = uempmed, y = psavert, color = year)) +
  geom_point(size = 2.2, alpha = 0.8) +
  scale_color_gradient(low = "#a6d96a", high = "#1f77b4") +
  labs(
    title = "Unemployment Duration vs. Savings Rate",
    subtitle = "Higher duration of unemployment is associated with lower savings behavior",
    x = "Median duration of unemployment (weeks)",
    y = "Personal savings rate (%)",
    color = "Year"
  ) +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 16))

ggsave(file.path(output_dir, "plot2_scatter_unemployment_vs_savings.png"), plot2, width = 10, height = 6, dpi = 300)

# Plot 3: histogram of unemployment distribution
plot3 <- ggplot(econ, aes(x = unemploy_thousands)) +
  geom_histogram(binwidth = 0.35, fill = "#2ca02c", color = "white") +
  labs(
    title = "Distribution of Monthly Unemployment Levels",
    subtitle = "Histogram of annual unemployment volume in thousands",
    x = "Unemployed persons (thousands)",
    y = "Frequency"
  ) +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 16))

ggsave(file.path(output_dir, "plot3_histogram_unemployment.png"), plot3, width = 10, height = 6, dpi = 300)

# Plot 4: average unemployment by decade
plot4_data <- econ %>%
  mutate(decade = floor(year / 10) * 10) %>%
  group_by(decade) %>%
  summarise(avg_unemployment = mean(unemploy_thousands, na.rm = TRUE), .groups = "drop")

plot4 <- ggplot(plot4_data, aes(x = factor(decade), y = avg_unemployment, fill = avg_unemployment)) +
  geom_col(width = 0.7) +
  scale_fill_gradient(low = "#ccebc5", high = "#2b8cbe") +
  labs(
    title = "Average Unemployment by Decade",
    subtitle = "Mean unemployment levels across major economic periods",
    x = "Decade",
    y = "Average unemployed persons (thousands)",
    fill = "Avg. unemployed"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 16),
    legend.position = "right"
  )

ggsave(file.path(output_dir, "plot4_bar_unemployment_by_decade.png"), plot4, width = 10, height = 6, dpi = 300)

# Plot 5: population growth over time
plot5 <- ggplot(econ, aes(x = date, y = population_millions)) +
  geom_line(color = "#6a3d9a", linewidth = 1.1) +
  labs(
    title = "US Population Growth Over Time",
    subtitle = "Population trend from 1967 to 2015",
    x = "Year",
    y = "Population (millions)"
  ) +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 16))

ggsave(file.path(output_dir, "plot5_population_growth.png"), plot5, width = 10, height = 6, dpi = 300)

# Output summary information for report generation
cat("Generated plots in:", output_dir, "\n")
cat("Rows:", nrow(econ), "\n")
cat("Columns:", paste(names(econ), collapse = ", "), "\n")
