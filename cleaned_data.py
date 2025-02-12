# import pandas as pd
# import numpy as np
# import re
# from datetime import datetime

# # Load dataset
# df = pd.read_csv("cleaning_Data.csv")  # Replace with actual file name

# ### **Step 1: Trim spaces from column names**
# df.columns = df.columns.str.strip()

# ### **Step 2: Trim spaces and clean text fields**
# text_columns = ['Name', 'Candidate Current City', 'Education', 'Marriage Status']

# for col in text_columns:
#     if col in df.columns:
#         df[col] = df[col].astype(str)  # Convert to string
#         df[col] = df[col].str.strip()  # Remove spaces
#         df[col] = df[col].str.lower()  # Convert to lowercase
#         df[col] = df[col].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))  # Remove special characters

# ### **Step 3: Convert 'Date Of Birth' to Age**
# if 'Date_Of_Birth' in df.columns:
#     df['Date_Of_Birth'] = pd.to_datetime(df['Date_Of_Birth'], errors='coerce')
#     df['Age'] = df['Date_Of_Birth'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else np.nan)

# # Drop rows with missing Age
# df = df.dropna(subset=['Age'])



# ### **Step 5: Remove duplicate rows**
# df = df.drop_duplicates()

# ### **Step 6: Save cleaned data**
# df.to_csv("cleaned_data_new.csv", index=False)
# print("✅ Data Cleaning Completed. Saved as 'cleaned_data.csv'")

import pandas as pd

# Load the dataset
file_path = "cleaned_data_new.csv"  # Update if needed
df = pd.read_csv(file_path)

# Dictionary mapping known cities to their respective countries
city_to_country = {
    # Indian Cities
    "Ahmedabad": "India", "Rajkot": "India", "Vadodara": "India", "Gandhinagar": "India",
    "Junagadh": "India", "Surat": "India", "Mumbai": "India", "Delhi": "India", "Kolkata": "India",
    "Chennai": "India", "Bangalore": "India", "Pune": "India", "Hyderabad": "India", "Jaipur": "India",

    # USA Cities
    "New York": "USA", "Los Angeles": "USA", "Chicago": "USA", "Houston": "USA", "San Francisco": "USA",
    "Dallas": "USA", "Miami": "USA",

    # UK Cities
    "London": "UK", "Manchester": "UK", "Birmingham": "UK", 

    # Canada Cities
    "Toronto": "Canada", "Vancouver": "Canada", "Calgary": "Canada",

    # Australia Cities
    "Sydney": "Australia", "Melbourne": "Australia", "Brisbane": "Australia",
}

# Function to clean the country column
def clean_country(value):
    if pd.isna(value) or value.strip() == "":
        return None  # Set empty values as NaN

    value = value.strip().title()  # Standardize case
    value = value.replace("  ", " ")  # Remove double spaces

    # Fix common misspellings and variations
    corrections = {
        "Indea": "India", "INDiA": "India", "india": "India", "INDIA ": "India",
        "U k(London)": "UK", "United Kingdom": "UK", "United States": "USA", "Ontario, Canada": "Canada",
        "U.S.A": "USA", "Usa": "USA", "America": "USA"
    }
    if value in corrections:
        return corrections[value]

    # Replace city names with their respective country
    return city_to_country.get(value, value)

# Apply cleaning function
df["Country"] = df["Country"].apply(clean_country)

# Save cleaned data
cleaned_file_path = "cleaned_data_final_new.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"Cleaned dataset saved as {cleaned_file_path}")
