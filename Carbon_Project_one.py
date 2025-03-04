'''
This Project is to analyse the relevant carbon data and then find create graphics

1. How have total emissions from major oil & gas companies changed over time?
2. Which companies or regions have the highest fugitive methane emissions, and how have they evolved?
3. Is there a correlation between production levels and emissions?
4. How have flaring and venting emissions changed over time, and which companies are the worst offenders?
5. What are the most emission-intensive commodities?

'''

import pandas as pd

data = pd.read_csv("C:/Users/marti/Documents/Documets +/UpSkill/Coding/2025/Carbon Projects/emissions_high_granularity.csv")

#print(data.head())

#1. How have total emissions from major oil & gas companies changed over time?

#Creating the table with these 3 columns
dataQ1 = data[["year","total_emissions_MtCO2e","parent_entity"]]

#Validating the Data
"""
#print(dataQ1.head())  # First 5 rows
#print(dataQ1.tail())  # Last 5 rows
print("No. Missing Column Values:\n",dataQ1.isnull().sum())  # Count missing values per column
print(dataQ1.duplicated().sum())  # Count duplicate rows
dataQ1 = dataQ1.drop_duplicates()
print(dataQ1.dtypes)
print(dataQ1["parent_entity"].unique())  # See all unique companies
print(dataQ1.describe())  # Summary statistics
dataQ1["year"] = pd.to_datetime(dataQ1["year"], format="%Y")
print(dataQ1["year"].head())  # Verify the conversion
"""
'''
#Normalisation for to compare the companies of different sizes 
- This hasn't worked how I intended it to 
- It lead to the narmalised values being summed once put into their bins and turned into the line chart
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
dataQ1["normalized_emissions"] = scaler.fit_transform(dataQ1[["total_emissions_MtCO2e"]])
'''

#Creating Bins for Simpler Visuals

"""
import numpy as np
bins = np.linspace(min(dataQ1["total_emissions_MtCO2e"]),max(dataQ1["total_emissions_MtCO2e"]),4)
bin_names = ["Low","Medium","High"]
dataQ1.loc[:,"emission_category"] = pd.cut(dataQ1["total_emissions_MtCO2e"],bins,labels=bin_names,include_lowest=True)

Number of values in each emission_category:
Low       15777
High         13
Medium        7
"""

#Creating Bins with a more balanced distribution 
quantiles = dataQ1["total_emissions_MtCO2e"].quantile([0, 0.33, 0.66, 1.0]).values
bin_names = ["Low", "Medium", "High"]

dataQ1 = dataQ1.copy()  # Ensures modifications are applied to a full DataFrame
dataQ1.loc[:, "emission_category"] = pd.cut(dataQ1["total_emissions_MtCO2e"], bins=quantiles, labels=bin_names, include_lowest=True) 

"""
#Checking Bins:
print(dataQ1["emission_category"].value_counts())
print(quantiles) # Bin parameters
print(dataQ1[["total_emissions_MtCO2e", "emission_category"]].sample(10)) # Checking a few random rows
"""



#Visualisation
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Group data by year and emission category, summing emissions per category
emissions_by_category = dataQ1.groupby(["year", "emission_category"], observed=True)["total_emissions_MtCO2e"].sum().unstack()
#what does the Observed = true or false mean?

# Apply Min-Max Scaling AFTER aggregation (to keep values between 0-1)
scaler = MinMaxScaler()
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
plt.xlabel("Year")
plt.ylabel("Normalized Emissions (0-1 Scale)")
plt.title("Normalized Emissions Trends by Company Size (Low, Medium, High)")
plt.legend(title="Emission Category")
plt.grid(True)

# Show & Save the plot
plt.savefig('Matplot_Linechart.png')
plt.show()

"""
#emissions_per_year = dataQ1.groupby("year")["total_emissions_MtCO2e"].sum()#  This Tells Plots the Sum of all companies so we can see that trend
plt.figure(figsize=(20, 10))
plt.plot(emissions_per_year.index, emissions_per_year.values, marker="o", linestyle="-", color="b") 

plt.title('How have total emissions from major oil & gas companies changed over time?')

# Add labels and title
plt.xlabel("Year")
plt.ylabel("Total Emissions (MtCO2e)")
#plt.title("Total Carbon Emissions Over Time")
plt.grid(True)

plt.savefig('Matplot_Linechart.png')
plt.show()
"""
