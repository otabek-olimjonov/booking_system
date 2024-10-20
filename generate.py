import pandas as pd
import json

# Load the JSON data (replace 'your_file.json' with the path to your JSON file)
with open('HumanProducts.json', encoding='utf-8-sig') as json_file:
    data = json.load(json_file)

# Create a DataFrame from the JSON data
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file (replace 'output_file.csv' with the desired CSV filename)
df.to_csv('HumanProducts.csv', index=False)

print("JSON has been successfully converted to CSV!")
