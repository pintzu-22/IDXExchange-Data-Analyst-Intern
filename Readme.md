# California Residential Real Estate Market Analysis

## Project Overview

This project analyzes California residential real estate market trends using CRMLS listing and sold data from January 2024 through June 2026.

The project focuses on data cleaning, feature engineering, market trend analysis, competitive analysis, and interactive Tableau dashboard development. The final deliverables include two Tableau workbooks, a one-page market intelligence report, and a five-minute dashboard presentation.

The analysis allows users to explore market conditions by city, county, ZIP code, and property subtype.

---

## Project Objectives

The main objectives of this project are to:

- Analyze monthly residential real estate pricing trends
- Evaluate changes in days on market and seller pricing performance
- Compare new listings with closed sales
- Analyze geographic differences across California markets
- Identify leading listing agents and brokerages
- Build interactive Tableau dashboards for market intelligence
- Summarize key findings in a one-page market report

---

## Data

The analysis uses monthly CRMLS residential listing and sold datasets covering:

**January 2024 – June 2026**

Two primary datasets were used:

- **List data** – active/new residential listings
- **Sold data** – completed residential transactions

The datasets were cleaned and prepared before being used for analysis and Tableau visualization.

---

## Data Preparation & Cleaning

Data preparation was performed in Python using pandas in VS Code and Jupyter Notebook. Monthly CRMLS listing and sold files were combined, standardized, validated, and prepared for downstream analysis.

Key cleaning and validation steps included:

- Standardized date fields and converted them to datetime format
- Converted Y/N indicator fields into boolean values
- Removed or flagged invalid records where price, living area, or days on market were less than or equal to zero
- Checked chronological consistency across listing, contract, and closing dates
- Created data-quality flags including:
  - `listing_after_close_flag`
  - `purchase_after_close_flag`
  - `negative_timeline_flag`
- Validated geographic information and flagged:
  - Missing coordinates
  - Zero latitude or longitude values
  - Out-of-state records
- Identified and reviewed duplicate transactions
- Removed columns with more than 90% missing values
- Filtered the final analytical datasets to residential properties
- Standardized fields used across listing and sold datasets for Tableau analysis

After cleaning, the analytical datasets contained approximately:

- **447,769 sold records**
- **615,316 listing records**

---

## Feature Engineering

New analytical variables were created in Python to support market trend and transaction analysis.

### Sold Data Features

- `price_ratio`
- `close_to_original_list_ratio`
- `price_per_sqft`
- `days_on_market`
- `year`
- `month`
- `Yrmo`
- Sale transaction identifiers

### Listing Data Features

- `year`
- `month`
- `Yrmo`
- Source year-month fields
- Listing-level identifiers used for distinct listing counts

These engineered features were used to calculate pricing trends, market activity metrics, and Tableau KPIs.
---

## Outlier Detection

The IQR method was used to identify extreme values while preserving the original records for quality review.

Outlier detection was applied to key numerical variables including:

- Close Price
- List Price
- Living Area
- Days on Market

For each variable, the first quartile (Q1), third quartile (Q3), and interquartile range (IQR) were calculated. Records outside the standard 1.5 × IQR boundaries were flagged.

An `any_iqr_outlier_flag` was created to identify records containing at least one IQR-based outlier.

Both flagged and filtered versions of the datasets were retained so that data-quality decisions remained transparent and reproducible.

---
## Technical Workflow

1. Imported monthly CRMLS listing and sold datasets into Python
2. Combined monthly files into consolidated listing and sold datasets
3. Standardized schemas, dates, categorical fields, and data types
4. Performed data-quality and logical consistency checks
5. Created validation flags for invalid dates and geographic records
6. Engineered analytical features for pricing and transaction analysis
7. Applied IQR-based outlier detection
8. Generated cleaned and filtered analytical datasets
9. Connected processed datasets to Tableau
10. Built interactive market and competitive analysis dashboards
11. Summarized findings in an Orange County Market Intelligence Report

---

## Tableau Dashboards

### Market Analysis

The Market Analysis workbook includes:

- Monthly Median Close Price
- Average Days on Market
- Close-to-Original-List Price Ratio
- New Listings
- Closed Sales
- Market Activity & Momentum

Users can filter the dashboards by:

- City
- County
- ZIP Code
- Property Subtype

## Competitive Analysis

The Competitive Analysis workbook includes:

- Top 100 Listing Agents by Sales Volume and Units Sold
- Top 100 Listing Offices by Sales Volume and Units Sold
- Median Close Price by ZIP Code
- Homes Sold by ZIP Code
- Listing Office Market Positioning

### Listing Office Market Positioning

The Listing Office Market Positioning dashboard compares listing offices based on **units sold** and **median close price**. Median reference lines divide the view into four positioning quadrants, helping identify high-volume market leaders, premium-focused offices, and smaller niche competitors.

The dashboard is filterable by **city, county, ZIP code, and property subtype**, allowing users to evaluate how brokerage positioning changes across different market segments.

---

## Orange County Market Intelligence Report

The one-page market intelligence report focuses on **Orange County, California**.

Key findings for June 2026 include:

- **Median Close Price:** $1.16M, up 5.45% YoY
- **Average Days on Market:** 24 days
- **Closed Sales:** 1,645, up 11.83% YoY
- **New Listings:** 2,085, up 70.07% YoY
- **Median Price per Sq Ft:** $664.86
- **Close-to-Original-List Price Ratio:** 98.96%
- **Sales-to-New-Listings Ratio:** 78.9%

Market leadership was led by **Cesi Pagano** among listing agents and **First Team Real Estate** among listing offices. :contentReference[oaicite:0]{index=0}

---

## Key Insights

1. **Home prices remained resilient.**  
   Orange County's median close price reached $1.16M in June 2026, representing a 5.45% year-over-year increase.

2. **New supply grew substantially faster than closed sales.**  
   New listings increased 70.07% year over year, compared with an 11.83% increase in closed sales.

3. **Buyer conditions became slightly less competitive.**  
   Average days on market increased to 24 days, while homes sold at 98.96% of their original asking price.

4. **Market leadership was consistent across volume and units.**  
   Cesi Pagano ranked first among listing agents by both sales volume and units sold, while First Team Real Estate ranked first among listing offices in both categories. :contentReference[oaicite:1]{index=1}

---

## Tools & Technologies

- Python
- pandas
- NumPy
- Jupyter Notebook
- Tableau
- VS Code
- Git
- GitHub

---