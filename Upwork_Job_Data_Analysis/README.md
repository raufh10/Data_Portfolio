# Upwork Job Post Data Analysis

## Table of Contents

- [Data Analysis (Jupyter Notebook)](#data-analysis)
- [Project Overview](#project-overview)
- [Features](#features)
- [Repository Structure](#repository-contents)
- [Conclusion and Insights](#conclusion-and-insights)
- [Actionable Insights](#actionable-insights)
- [Questions for Further Research](#questions-for-further-research)
- [Disclaimer](#disclaimer)

## Data Analysis
To access the analysis in the Jupyter Notebook, [click here](analysis/analysis.ipynb).

## Project Overview

**Objective**: Analyzing job postings on Upwork using web scraping and data analysis.

### Methodology

- **Web Scraping Techniques**: Utilize BeautifulSoup4 and Playwright to gather data from Upwork job postings.
- **Data Analysis in Jupyter Notebook**: Conduct an in-depth analysis of the scraped data.

### Goals

My goals for this project are to extract meaningful insights that could aid data analyst freelancers as follows:

- **Job Market Insights**: Understand the current job market on Upwork.
- **In-Demand Skills**: Identify skills most sought after by employers.
- **Rate Insights**: Analyze prevailing rate structures for data analyst roles.

## Features

- **Data Scraping**: Implementation of a beautifulsoup script to scrape job postings from Upwork.
- **Data Cleaning**: Utilization of custom scripts to refine and preprocess the raw data.
- **Data Analysis**: Execution of detailed and exploratory analysis in a Jupyter Notebook for an interactive and reproducible study.
- **Visualization**: Creation of graphs and charts to visually to explore the data and analyze trends.
- **Insights**: Generation of insights and conclusions that could be used to inform freelancers for their job search.

## Repository Contents

- `analysis/` - Contains the Jupyter Notebook that details the data analysis process.
- `etl/` - Includes beautifulsoup script for scraping job data from Upwork. Also contains scripts for cleaning and preprocessing the raw data into presentable json format.
- `output/` - Contains the json file with the job data.
- `README.md` - This file, which acts as a guide for the repository.

## Conclusion and Insights

1. **Skill Popularity:**
The most in-demand tool-based skills in our dataset include Microsoft Excel, Python, SQL, Microsoft Power BI, Google Analytics, R, and Tableau.

2. **Duration & Average Hourly Rate Regression Analysis:**
The analysis yielded an `r` value of -0.16, indicating a weak negative linear relationship between project duration and average hourly rate.

3. **Hourly Rates:**
There is a noticeable trend in hourly rates relative to experience level. On average, the transition from Entry level to Intermediate level sees an approximate increase of $20 in hourly rate. Similarly, moving from Intermediate to Expert level typically results in an additional increase of around $10.

## Actionable Insights

Based on the findings, the following actions are recommended:

1. **Skill Development Focus:**
Prioritize learning tools like Microsoft Excel, Python, SQL, and Microsoft Power BI to align with market demand. Obviously, this is not to say that other tools are not in demand, but rather that these tools are more in demand than others. For example most employers are looking for Microsoft Excel skills, because Microsoft Excel is a very common tool used for dealing with spreadsheet. Similarly, Python is a very popular programming language, and SQL is a very common language used for querying databases. Therefore, it is recommended to focus on these tools to increase the chances of getting freelance jobs.

2. **Project Selection Strategy:**
Given the weak negative relationship between project duration and average hourly rate, it may be beneficial to apply for shorter-duration projects, especially if the aim is to maximize hourly earnings.

3. **Pricing Strategy Based on Experience:**
Adjust pricing strategies to what is appropriate for the experience level or the budget of the employer. For example, if you are an entry level data analyst, you should not be charging the same hourly rate as an expert data analyst. Similarly, if you are an expert data analyst, you should not be charging the same hourly rate as an entry level data analyst. This is because employers are willing to pay more for expert data analysts, and less for entry level data analysts. Therefore, it is also recommended to adjust your hourly rate based on your experience level.

## Questions for Further Research

Intersting questions that could be explored in future research include:

### Project Type Variations

- **Objective:** To investigate how hourly rates and skill requirements vary among different project types.
- **Key Questions:**
  - What are the common project types listed for data analysts (e.g., short-term vs long-term projects, data cleaning vs data visualization)?
  - How does the compensation differ across these project types?

This focused research will provide deeper insights into the dynamics of the data analyst freelance job market.

## Disclaimer

The web scraping script provided in this repository is intended for educational purposes only. The author is not responsible for how this script is used, nor for any code lost or damages caused by this script.
