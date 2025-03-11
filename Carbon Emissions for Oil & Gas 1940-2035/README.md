# Carbon Emissions Analysis

## Overview  
This project analyzes carbon emissions data from major oil & gas companies over time. The goal is to identify trends, categorize companies based on their emissions levels, and visualize the results.  

## Key Research Question  
1. How have total emissions from major oil & gas companies changed over time?  

## Methodology  
- **Data Cleaning:** Removed duplicates, handled missing values, and formatted time-series data.  
- **Categorization:** Companies were grouped into **Low, Medium, and High emission categories** based on quantiles.  
- **Normalization:** Min-Max Scaling was applied to ensure fair comparison between different companies.  
- **Visualization:** A **time-series line chart** was created to track emission trends over the years.  

## Findings  
- Emissions have generally increased over time, especially since the mid-20th century.  
- High-emission companies show exponential growth, while medium and low emitters have more fluctuations.  
- Recent declines in some categories could be linked to policy changes, economic slowdowns, or clean energy adoption.  

## Further Research  
- What are the biggest drivers of emission reductions? (Regulations, market shifts, technology investments?)  
- How do emissions differ by region? (Comparing policies across different countries.)  
- Which companies are transitioning to renewable energy? (Are they actually reducing emissions?)  

## Technologies Used  
- **Python** (Pandas, Matplotlib, NumPy, Scikit-learn)  
- **GitHub** (Version control)  

## How to Run This Project  
1. Clone the repository:  
   ```sh
   git clone https://github.com/martinryangilperez/Carbon-Emissions-Analysis.git
   cd Carbon-Emissions-Analysis
