import pandas as pd

# Load the Excel file
df = pd.read_excel("Book1.xlsx")

# Print the columns to verify
print("Columns in the Excel file:", df.columns)
