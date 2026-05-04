
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# STEP 5: ANALYSIS
print("Connecting to Database...")

# Open connection to our local database
connection = sqlite3.connect("job_market.db")

# Write a pure SQL query to select everything from our table
query = "SELECT * FROM python_jobs"

# Ask Pandas to execute the query and convert the result back into a DataFrame
df = pd.read_sql_query(query, connection)

# Close the connection (the data is safely in our RAM now)
connection.close()

print("Data loaded successfully from SQL!")
print(f"Total rows retrieved: {len(df)}")

# We want to calculate the average minimum salary. 
# To do that, we need to filter out the rows where the minimum salary is not available (NaN).
df_salaries_only = df.dropna(subset=['Min_Salary'])

print(f"Rows with actual salary data: {len(df_salaries_only)}")

# Calculates the average of the minimum salaries
average_min_salary = df_salaries_only['Min_Salary'].mean()
print(f"The average minimum salary for a Python Dev is: {average_min_salary:.2f}€")

# STEP 6: VISUALIZATION

print("\nGenerating Visualization...")

# Sorts the data so the highest salaries appear first
df_sorted = df_salaries_only.sort_values(by='Min_Salary', ascending=False)

# Sets up the canvas and plot
plt.figure(figsize=(10, 6)) # Width 10, Height 6

# Create a bar chart: X axis = Company names, Y axis = Min Salaries
plt.bar(df_sorted['Company'], df_sorted['Min_Salary'], color='skyblue')

# Add labels and title
plt.title('Minimum Salaries for Python Developers', fontsize=14)
plt.xlabel('Company', fontsize=12)
plt.ylabel('Salary (€)', fontsize=12)

# Rotate company names so they are readable
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()