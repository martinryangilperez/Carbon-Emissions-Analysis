'''
# Carbon Emissions Analysis 

#  Overview  
This project analyzes carbon emissions data from major oil & gas companies over time. The goal is to identify trends, categorize companies based on their emissions levels, and visualize the results.  

# Key Research Question  
1. How have total emissions from major oil & gas companies changed over time?**  

# Methodology  
Data Cleaning: Removed duplicates, handled missing values, and formatted time-series data.  
Categorization: Companies were grouped into Low, Medium, and High emission categories based on quantiles.  
Normalization: Min-Max Scaling was applied to ensure fair comparison between different companies.  
Visualization: A Time-series line chart was created to track emission trends over the years.  

# Findings  
Emissions have generally increased over time, especially since the **mid-20th century.  
High-emission companies show exponential growth, while medium & low emitters have more fluctuations.  
Recent declines in some categories could be linked to policy changes, economic slowdowns, or clean energy adoption.  

# Further Research  
What are the biggest drivers of emission reductions? (Regulations, market shifts, technology investments?)  
How do emissions differ by region? (Comparing policies across different countries.)  
Which companies are transitioning to renewable energy? (Are they actually reducing emissions?)  
'''


import pandas as pd

data = pd.read_csv("C:/Users/marti/Documents/Documets +/UpSkill/Coding/2025/Carbon Projects/emissions_high_granularity.csv")

#Creating the table with these 3 columns
dataQ1 = data[["year","total_emissions_MtCO2e","parent_entity"]]

#Validating the Data

print(dataQ1.head())  # First 5 rows
print(dataQ1.tail())  # Last 5 rows
print("No. Missing Column Values:\n",dataQ1.isnull().sum())  # Count missing values per column
print(dataQ1.duplicated().sum())  # Count duplicate rows
dataQ1 = dataQ1.drop_duplicates()
print(dataQ1.dtypes)
print(dataQ1["parent_entity"].unique())  # See all unique companies
print(dataQ1.describe())  # Summary statistics
dataQ1["year"] = pd.to_datetime(dataQ1["year"], format="%Y")
print(dataQ1["year"].head())  # Verify the conversion


#Creating Bins with a balanced distribution 
quantiles = dataQ1["total_emissions_MtCO2e"].quantile([0, 0.33, 0.66, 1.0]).values
bin_names = ["Low", "Medium", "High"]

dataQ1 = dataQ1.copy()  # Ensures modifications are applied to a full DataFrame
dataQ1.loc[:, "emission_category"] = pd.cut(dataQ1["total_emissions_MtCO2e"], bins=quantiles, labels=bin_names, include_lowest=True) 

#Checking Bins:
print(dataQ1["emission_category"].value_counts())
print(quantiles) # Bin parameters
print(dataQ1[["total_emissions_MtCO2e", "emission_category"]].sample(10)) # Checking a few random rows

#Visualisation
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Group data by year and emission category, summing emissions per category
emissions_by_category = dataQ1.groupby(["year", "emission_category"], observed=True)["total_emissions_MtCO2e"].sum().unstack()

# Apply Min-Max Scaling AFTER aggregation (to keep values between 0-1)
scaler = MinMaxScaler(feature_range=(0, 1))
normalized_emissions = pd.DataFrame(
    scaler.fit_transform(emissions_by_category),  # Normalize across years
    index=emissions_by_category.index,  
    columns=emissions_by_category.columns)  

# Create the plot
plt.figure(figsize=(18, 9))

# Plot each emission category as a separate line
for category in normalized_emissions.columns:
    plt.plot(normalized_emissions.index, normalized_emissions[category], marker="o", linestyle="-", label=category)

# Add labels, title, and legend
plt.xlabel("Year", fontsize=14)
plt.ylabel("Normalized Emissions (0-1 Scale)", fontsize=14)
plt.title("Normalized Emissions Trends by Company Size (Low, Medium, High)", fontsize=16)

# Move legend outside the plot for better readability
plt.legend(title="Emission Category")

plt.grid(True, linestyle="--", alpha=0.7)

# Show & Save the plot
plt.savefig('Matplot_Linechart.png', dpi=300, bbox_inches="tight")
plt.show()
