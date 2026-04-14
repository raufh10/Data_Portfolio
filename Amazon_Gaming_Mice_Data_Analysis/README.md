# Amazon Bestseller PC Gaming Mice Analysis

## Table of Contents

- [Data Analysis (Jupyter Notebook)](#data-analysis)
- [Project Overview](#project-overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Key Takeaways Summary](#key-takeaways-summary)
- [Actionable Insights](#actionable-insights)
- [Questions for Further Research](#questions-for-further-research)
- [Disclaimer](#disclaimer)

## Data Analysis
To access the analysis in the Jupyter Notebook, [click here](analysis/analysis.ipynb).

## Project Overview

**Objective**: Investigate the market for PC gaming mice by analyzing Amazon's Bestseller list.

### Methodology

- **Web Scraping Techniques**: Utilize BeautifulSoup4 and Playwright to extract data from Amazon's Bestseller list, specifically focusing on PC gaming mice.
- **Data Analysis in Jupyter Notebook**: Perform detailed analysis on the gathered data.

### Goals

The main goals of this project are to provide valuable insights to businesses and individuals interested in the PC gaming mice market:

- **Market Trends**: Gain a comprehensive understanding of the current trends in the PC gaming mice segment on Amazon.
- **Pricing Patterns**: Analyze and interpret the pricing strategies and patterns for top-rated gaming mice.
- **Product Features Analysis**: Identify and evaluate the key features that make these gaming mice popular among consumers.

This project aims to deliver actionable insights that can guide purchase in the niche of PC gaming mice.

## Features

- **Web Scraping**: A Python script that utilizes Beautiful Soup and playwright to extract data from Amazon's Bestseller page for gaming mice.
- **Data Cleaning**: Processing the raw data to prepare it for analysis, including handling missing values and normalizing data formats.
- **Data Analysis**: Using Python, particularly pandas , to analyze the data, supplemented by Jupyter Notebook for documentation and step-by-step explanation.
- **Visualization**: Generating visualizations using Matplotlib and Seaborn to represent the data graphically.

## Repository Structure

- `etl/` - Contains the web scraping script to collect data from Amazon. Also contains scripts to process the raw data.
- `analysis/` - Jupyter Notebooks with the exploratory data analysis and visualizations.
- `output/` - Contains processed data collected from Amazon.
- `README.md` - The guide and documentation for this repository.

## Key Takeaways Summary

1. **Data Overview:**
   - Initial dataset: 100 rows, 48 columns, many null values, no duplicates.
   - Post-cleanup: 87 rows, 10 columns.

2. **Market Analysis:**
   - Average price: $48.63.
   - Average rating: 4.5.
   - Price range: $5.99 to $148.99.
   - Most popular color: Black.

3. **Cluster Analysis:**
   - Four product clusters based on rankings and prices.

4. **Brand Analysis:**
   - Razer and Logitech: Wide range in price and quality.
   - Trueque and Redragon: Primarily low-priced options.
   - Corsair, despite fewer products, has a significant price spread.
   - Logitech's products are generally high-ranking and fall into either high or low price categories.

5. **Rating Analysis:**
   - Ratings mostly around 4.5 to 4.6.
   - Logitech: Higher ratings.
   - Razer: Wide range in ratings.

6. **Scatter Plot Insights:**
   - Higher-priced products often have ratings above 4.6.
   - No other significant patterns.

## Actionable Insights

Based on the findings, the following actions are recommended:

1. **Budget Planning:**
    - With an average price of $48.63 and a range from $5.99 to $148.99, set a budget that aligns with this spectrum. High-end mice can go up to $148.99, while budget options are available from as low as $5.99.
2. **Focus on Popular Brands for Quality and Price Range:**
    - Consider Razer and Logitech for a wide variety of choices in terms of price and quality.
    - Look at Trueque and Redragon for more budget-friendly options.
3. **Rating as a Quality Indicator:**
    - Prioritize mice with ratings around 4.5 to 4.6 for reliable quality.
    - Logitech generally offers higher-rated products, suggesting customer satisfaction.
4. **Price-to-Quality Correlation:**
    - Since higher-priced products often have ratings above 4.6, investing more could lead to better quality and user satisfaction.

## Questions for Further Research

### Price Sensitivity Analysis

- **Objective:** To investigate how price changes influence consumer buying behavior in the gaming mice segment.
- **Key Questions:**
  - What is the price elasticity of demand for gaming mice?
  - How does the introduction of budget-friendly models by premium brands affect the overall market?

This research will provide valuable insights into the price sensitivity of consumers in the gaming mice market.

## Disclaimer

The web scraping script provided in this repository is intended for educational purposes only. The author is not responsible for how this script is used, nor for any code lost or damages caused by this script.
