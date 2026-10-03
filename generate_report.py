from docx import Document
from docx.shared import Inches
from pathlib import Path

root = Path(__file__).resolve().parent
output_dir = root / 'output'
report_path = root / 'Data_Visualization_Report.docx'

doc = Document()
doc.add_heading('Week 2: Data Visualization and Insight Communication using R', 0)

doc.add_paragraph('This report uses the US economic dataset from ggplot2 to illustrate patterns in unemployment, savings behavior, and population growth. The goal is to translate raw economic indicators into meaningful visual narratives that support decision-making and make trends easier to interpret for both technical and non-technical readers.')

# Section 1
section = doc.add_heading('1. Dataset Overview', level=1)
doc.add_paragraph('The selected dataset is the econometrics-style economic indicators dataset contained in the ggplot2 package. It covers monthly US economic data from 1967 to 2015. The main variables used in this analysis include unemployment, median duration of unemployment, personal savings rate, and population.')
doc.add_paragraph('Key takeaway: The dataset is suitable for time-series, comparative, and distribution-based visualizations because it captures both long-term structural changes and short-term fluctuations in economic conditions.')

# Insert code snippet
code_block = '''
# R code for loading the dataset and preparing variables
library(ggplot2)
library(dplyr)
library(lubridate)

econ <- ggplot2::economics %>%
  mutate(
    year = as.integer(format(date, "%Y")),
    unemploy_thousands = unemploy / 1000,
    population_millions = pop / 1000000
  )
'''
para = doc.add_paragraph()
run = para.add_run('R code snippet:\n')
run.bold = True
for line in code_block.strip().splitlines():
    doc.add_paragraph(line, style='List Bullet')

# Section 2
section = doc.add_heading('2. Visualizations and Insights', level=1)

def add_figure(title, image_name, commentary):
    doc.add_heading(title, level=2)
    doc.add_paragraph(commentary)
    image_path = output_dir / image_name
    if image_path.exists():
        doc.add_picture(str(image_path), width=Inches(6.5))
    else:
        doc.add_paragraph(f'Image not found: {image_path.name}')

add_figure(
    'Figure 1: Economic Stress and Household Savings Trends',
    'plot1_economic_trends.png',
    'This line chart compares unemployment levels with the personal savings rate. It shows how periods of elevated unemployment often coincide with changes in consumer confidence and financial behavior. The chart helps readers understand that employment pressure and savings behavior move together in a complex but meaningful way over time.'
)

add_figure(
    'Figure 2: Unemployment Duration vs. Savings Rate',
    'plot2_scatter_unemployment_vs_savings.png',
    'The scatter plot explores whether longer unemployment spells are associated with reduced household savings. The pattern suggests that economic uncertainty can influence household financial decisions, making this a strong exploratory visualization for behavioral analysis.'
)

add_figure(
    'Figure 3: Distribution of Monthly Unemployment Levels',
    'plot3_histogram_unemployment.png',
    'The histogram highlights the spread of monthly unemployment levels. It reveals whether unemployment values are concentrated around a typical range or spread across multiple levels. This supports a clearer understanding of volatility and the frequency of downturn periods.'
)

add_figure(
    'Figure 4: Average Unemployment by Decade',
    'plot4_bar_unemployment_by_decade.png',
    'The bar chart summarizes average unemployment by decade and makes macroeconomic shifts easier to compare. It is especially useful for non-technical audiences because it converts the trend into a simple comparison between time periods.'
)

add_figure(
    'Figure 5: US Population Growth Over Time',
    'plot5_population_growth.png',
    'This time-series plot shows the steady increase in population across the period. It provides context for economic indicators by demonstrating that employment and savings trends are occurring within a growing national population, which affects labor supply and economic demand.'
)

# Section 3
section = doc.add_heading('3. Overall Interpretation', level=1)
doc.add_paragraph('The visualizations show that unemployment, savings behavior, and population trends are not isolated data points—they are connected parts of a broader economic story. In times of weak labor demand, households often reduce financial flexibility, while population expansion continues to shape long-term consumption and labor market dynamics.')
doc.add_paragraph('The use of multiple chart types was intentional. Line charts communicate temporal patterns, scatter plots reveal relationships between variables, histograms expose distribution, and bar charts simplify comparative interpretation. Together, they provide a balanced communication strategy for data-driven storytelling.')

# Section 4
section = doc.add_heading('4. Conclusion', level=1)
doc.add_paragraph('This project demonstrates how R and ggplot2 can transform data into clear, insightful visual stories. The charts are easy to interpret and effective for highlighting both trends and anomalies in economic data. The report therefore satisfies the goal of communicating insights through dynamic and informative visualization.')

# Final insertion of code snippets for the bar and line chart examples
code_block_2 = '''
# Example ggplot code for one chart
plot <- ggplot(econ, aes(x = date, y = unemploy_thousands)) +
  geom_line(color = "#1f77b4", linewidth = 1.1) +
  labs(title = "Unemployment Trend", x = "Year", y = "Unemployed persons (thousands)") +
  theme_minimal()

ggsave("output/unemployment_trend.png", plot, width = 10, height = 6, dpi = 300)
'''
doc.add_paragraph('Example R code used to generate a chart:')
for line in code_block_2.strip().splitlines():
    p = doc.add_paragraph()
    p.add_run(line)
    p.style = 'Intense Quote'

# Save document
try:
    doc.save(report_path)
    print(f'Report saved to {report_path}')
except Exception as exc:
    print(f'Error saving report: {exc}')
