'''
# Carbon Emissions Analysis 

#  Overview  
This project analyzes carbon emissions data from major oil & gas companies over time. The goal is to identify trends, categorize companies based on their emissions levels, and visualize the results.  

# Key Research Question  
How have total emissions from major oil & gas companies changed over time, and what trends can we predict for the future?**  

# Methodology  
Data Cleaning: Removed duplicates, handled missing values, and formatted time-series data.  
Categorization: Companies were grouped into Low, Medium, and High emission categories based on quantiles.  
Normalization: Min-Max Scaling was applied to ensure fair comparison between different companies.  
Visualization: A Time-series line chart was created to track emission trends over the years.  

# Findings  
Recent declines in some categories could be linked to policy changes, economic slowdowns, or clean energy adoption. 
Emissions have generally increased over time, especially since the **mid-20th century.  
Our forecast suggests High-emission companies show exponential growth, while medium & low emitters have more fluctuations.  


# Further Research  
What are the biggest drivers of emission reductions? (Regulations, market shifts, technology investments?)  
How do emissions differ by region? (Comparing policies across different countries.)  
Which companies are transitioning to renewable energy? (Are they actually reducing emissions?)  
'''

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

data = pd.read_csv("C:/Users/marti/Documents/Documets +/UpSkill/Coding/2025/Carbon Projects/emissions_high_granularity.csv")

#---------- Creating a Function to Validate the Data ----------
def validate_data(df):
    """
    Performs basic validation checks on the dataset:
    - Prints first & last 5 rows
    - Checks for missing values
    - Checks for duplicate entries
    - Displays column data types
    - Lists unique company names
    - Provides summary statistics
    """
    print("----- DATA VALIDATION REPORT -----")
    
    print("\n First 5 Rows:")
    print(df.head())
    
    print("\n Last 5 Rows:")
    print(df.tail())

    print("\n Missing Values Count:")
    print(df.isnull().sum())

    print("\n Duplicate Rows:", df.duplicated().sum())

    print("\n Data Types:")
    print(df.dtypes)

    print("\n Unique Parent Entities (Sample):")
    print(df["parent_entity"].unique()[:10])  # Display only first 10 unique entities for brevity

    print("\n Summary Statistics:")
    print(df.describe())

    print("\n----- Validation Complete! -----")


# Convert 'year' to datetime format
data["year"] = pd.to_datetime(data["year"], format="%Y")

#Creating the table with these 3 columns
dataQ1 = data[["year","total_emissions_MtCO2e","parent_entity"]].copy()

# Call the validation function
validate_data(data)

dataQ1 = data[data["year"].dt.year >= 1940].copy()

# Creating Bins for Emission Categories
quantiles = dataQ1["total_emissions_MtCO2e"].quantile([0, 0.33, 0.66, 1.0]).values
bin_names = ["Low", "Medium", "High"]

dataQ1["emission_category"] = pd.cut(dataQ1["total_emissions_MtCO2e"], bins=quantiles, labels=bin_names, include_lowest=True)


#Checking Bins:
print(dataQ1["emission_category"].value_counts())
print(quantiles) # Bin parameters
print(dataQ1[["total_emissions_MtCO2e", "emission_category"]].sample(10)) # Checking a few random rows

# Group data by Year and Emission Category
emissions_by_category = dataQ1.groupby(["year", "emission_category"])["total_emissions_MtCO2e"].sum().unstack()

#---------- Visualisation ----------

# Apply Min-Max Normalization for each category separately
scaler = MinMaxScaler(feature_range=(0, 1))
normalized_emissions = pd.DataFrame(scaler.fit_transform(emissions_by_category), index=emissions_by_category.index, columns=emissions_by_category.columns)

#---------- Forecast emissions for each category separately ----------
forecasts = {}

for category in bin_names:
    if category in normalized_emissions.columns:
        print(f"\nTraining ARIMA for {category} Emissions...")

        # Extract time series for the category
        category_series = normalized_emissions[category].dropna()

        # Train ARIMA model on all available data
        train = category_series  

        # Fit ARIMA model with a simpler order to prevent instability
        model = ARIMA(train, order=(5,2,1))  # Reduced complexity
        model_fit = model.fit()

        # Forecast emissions for the next 13 years
        forecast_steps = 13
        forecast = model_fit.get_forecast(steps=forecast_steps).predicted_mean  # Ensure proper extraction

        # Get the last year from training data
        last_training_year = category_series.index[-1]

        # Generate future years with proper format
        future_years = pd.date_range(start=last_training_year, 
                                     periods=forecast_steps, freq='YE')

        # Store the forecast
        forecasts[category] = pd.Series(forecast.values, index=future_years)

        # Print sample forecast to verify it's working
        print(f"Forecast for {category}:\n", forecasts[category].head())


#---------- Visulaisation: Plotting the Graph ----------

plt.figure(figsize=(14, 8))

for category in bin_names:
    if category in normalized_emissions.columns:
        # Get the last training year
        last_training_year = normalized_emissions.index[-1]

        # Generate future years with the correct length
        future_years = pd.date_range(start=last_training_year, periods=len(forecasts[category]), freq='YE')

        # Ensure forecast starts from the last known data point
        last_observed_value = normalized_emissions[category].iloc[-1]
        forecast_series = pd.concat([
            pd.Series([last_observed_value], index=[last_training_year]),  # Ensure smooth connection
            forecasts[category]  # Keep original forecast
        ])

        # Now, drop the first forecast value to match `future_years` length
        forecast_series = forecast_series.iloc[1:]  # Removes the extra first value

        # Plot observed emissions (solid line)
        observed_line, = plt.plot(normalized_emissions.index, normalized_emissions[category], 
                                  marker="", linestyle="-", label=f"Observed {category} Emissions")

        # Get the automatically assigned color from the observed line
        color = observed_line.get_color()

        # Plot forecasted emissions (dashed line, using the same color)
        plt.plot(future_years, forecast_series, marker="", linestyle="--", color=color, 
                 label=f"Predicted {category} Emissions", alpha=0.8)

plt.xlabel("Year", fontsize=14, fontweight="bold")
plt.ylabel("Emission Intensity (Normalized 0-1 Scale)", fontsize=14, fontweight="bold")
plt.title("Carbon Emissions: Observed vs. Forecasted Trends (1940-2035)", fontsize=18, fontweight="bold")

#----------Changing the Legend----------
import matplotlib.patches as mpatches

# Define smaller solid color patches for each emission category
legend_handles = [
    mpatches.Patch(color='blue', label="Low Emissions", linewidth=0.3),
    mpatches.Patch(color='orange', label="Medium Emissions", linewidth=0.3),
    mpatches.Patch(color='green', label="High Emissions", linewidth=0.3)
]

# Create the main legend with slight transparency
legend = plt.legend(handles=legend_handles, loc="upper left", title="Emission Trends", 
                    fontsize=10, frameon=True, framealpha=0.8, borderpad=1)

# Adjust legend background & spacing
legend.get_frame().set_edgecolor("black")  # Optional: Add a border to the legend box
legend.get_frame().set_linewidth(0.5)  # Make the border thinner

# Add explanation **inside** the legend as an extra text entry
plt.gca().add_artist(legend)  # Ensure the legend is drawn first

# Manually add explanation **below the legend**
plt.text(0.02, 0.75, "Solid = Observed\nDashed = Forecasted", 
         transform=plt.gca().transAxes, fontsize=9, fontstyle="italic",
         bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.3'))

plt.grid(True, linestyle="--", alpha=0.25)  # Lighter, less distracting grid
plt.gca().set_facecolor("#f8f8f8")  # Light gray background for better contrast

#----------Vertical Reference Lines for Key Years----------

# Convert key years into the same datetime format as x-axis
current_year = pd.to_datetime("2022-01-01")  # Last observed year
forecast_end = pd.to_datetime("2035-01-01")  # End of forecast

# Plot vertical reference lines at 2022 & 2035
plt.axvline(x=current_year, color="gray", linestyle="--", alpha=0.6, lw=1.2)
plt.axvline(x=forecast_end, color="gray", linestyle="--", alpha=0.6, lw=1.2)

# Add labels near the lines
plt.text(current_year, 0.08, "2022    \n(Last Observed)   ", rotation=0, fontsize=10, ha="right", va="top", color="black")

plt.text(forecast_end, 0.08, "2035    \n(Forecast End)   ", rotation=0, fontsize=10, ha="right", va="top", color="black")


#---------- Show & Save the plot ----------
plt.savefig('Matplot_Linechart.png', dpi=300, bbox_inches="tight")
plt.show()

# Print Mean Squared Errors for each category
for category in forecasts:
    print(f"Forecast for {category}: {forecasts[category].head()}")