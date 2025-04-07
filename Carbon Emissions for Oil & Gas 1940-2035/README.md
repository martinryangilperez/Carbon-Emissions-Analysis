# Carbon Emissions Analysis for Oil & Gas (1940–2035)

## Product Overview

### Vision
To empower climate-conscious stakeholders with transparent insights into historical and future oil & gas carbon emissions, enabling more informed decisions for environmental impact and policy development.

### Mission
To create a reproducible, data-driven tool that visualizes and analyzes emissions data from 1940 to 2035 — identifying top emitters, emission trends, and opportunities for intervention in the oil & gas sector.

### Strategy
- Use publicly available datasets to analyze emissions patterns over time.
- Visualize trends clearly using Python and data visualization libraries.
- Structure the project with a product-thinking mindset (vision, PRD, user stories, iteration).
- Allow for future integration with machine learning models and scenario testing.

## 📊 Product Requirements Document (PRD)

### Goals
- Analyze oil & gas CO₂ emissions from 1940 to 2035.
- Identify top-emitting countries and companies over time.
- Visualize emission trends and anomalies.

### User Stories
- **As a policymaker**, I want to track emissions across decades to design better carbon legislation.
- **As a sustainability analyst**, I want to compare emissions by company to inform ESG decisions.
- **As a student or researcher**, I want clear visualizations to understand how fossil fuel emissions evolved.

### Features
- Time series analysis of global and regional CO₂ emissions.
- Bar charts comparing emissions between companies or regions.
- Initial prediction extension to 2035 based on available historical trends.
- Highlighting the “worst offenders” in each category.

## 📁 Dataset Description

- **Source**: BP Statistical Review of World Energy
- **Variables**: Year, Country/Company, CO₂ Emissions (Million tonnes)
- **Timeframe**: 1940–2035 (past and projected)
- **Cleaning Steps**: Removed missing values, unified units, and normalised categories for consistency

## Technologies Used  
- **Python** (Pandas, Matplotlib, NumPy, Scikit-learn)  
- **GitHub** (Version control)  

## 🔁 Future Development & Experiments

- Introduce clustering or outlier detection for emission intensities
- Add interactive dashboards (e.g. using Plotly or Streamlit)
- Hypothetical scenarios:
  - “If Company X reduced emissions by 25%, how would global totals shift?”
  - “What policy measures could realistically reduce the top 10 emitters' footprints?”

## 🧠 Learnings & Product Thinking

- Practised applying product principles to a technical project
- Learned how to write user stories and think in terms of goals, not just outputs
- Gained experience building reusable templates for analysis and iterating based on findings


## How to Run This Project  
1. Clone the repository:  
   ```sh
   git clone https://github.com/martinryangilperez/Carbon-Emissions-Analysis.git
   cd Carbon-Emissions-Analysis
