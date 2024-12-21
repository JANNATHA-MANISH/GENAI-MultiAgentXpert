import os
import csv
import pandas as pd
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

folder_path = "./data"  # Replace with the full path to the target folder
input_file_path = os.path.join(folder_path, "keywords.txt")
output_file_path = os.path.join(folder_path, "resource_links.csv")

# Load environment variables from .env file
load_dotenv()

# Function to fetch datasets from Kaggle using the Kaggle Python API
def fetch_datasets_from_kaggle(query):
    try:
        api = KaggleApi()
        api.authenticate()
        search_results = api.dataset_list(search=query)
        resources = [
            {"name": dataset.title, "url": f"https://www.kaggle.com/{dataset.ref}", "source": "Kaggle"}
            for dataset in search_results
        ]
        return resources
    except Exception as e:
        print(f"Error fetching datasets from Kaggle for query '{query}': {e}")
        return []

# Function to extract use case details
def extract_use_case_details(use_case_text):
    use_cases = []
    use_case_blocks = use_case_text.split("\n\n")
    for block in use_case_blocks:
        lines = block.strip().split("\n")
        use_case = {}
        for line in lines:
            if line.startswith("**Use Case Title:**"):
                use_case["title"] = line.split("**Use Case Title:**")[1].strip()
            elif line.startswith("**Description:**"):
                use_case["description"] = line.split("**Description:**")[1].strip()
            elif line.startswith("**Keywords:**"):
                keywords = line.split("**Keywords:**")[1].strip().split(",")
                use_case["keywords"] = [keyword.strip() for keyword in keywords[:4]]
        if use_case:
            use_cases.append(use_case)
    return use_cases

# Function to fetch datasets and aggregate directly into a DataFrame
def process_and_aggregate(use_cases):
    all_resources = []

    # Fetch datasets for each use case based on the first 4 keywords
    for use_case in use_cases:
        title = use_case["title"]
        description = use_case["description"]
        keywords = use_case["keywords"]

        for keyword in keywords:
            # Fetch from Kaggle (limit to 1 link per keyword)
            kaggle_datasets = fetch_datasets_from_kaggle(keyword)[:1]
            for dataset in kaggle_datasets:
                all_resources.append({
                    "Use Case Title": title,
                    "Use Case Description": description,
                    "Keyword": keyword,
                    "Dataset Name": dataset["name"],
                    "Dataset Link": dataset["url"],
                    "Source": dataset["source"]
                })

    # Convert resources into a DataFrame
    df = pd.DataFrame(all_resources)

    if not df.empty:
        # Aggregate data by 'Use Case Title' and 'Use Case Description'
        aggregated_df = df.groupby(['Use Case Title', 'Use Case Description']).agg({
            'Keyword': lambda x: ', '.join(sorted(x.unique())),
            'Dataset Name': lambda x: ', '.join(sorted(x.unique())),
            'Dataset Link': lambda x: ', '.join(sorted(x.unique())),
            'Source': lambda x: ', '.join(sorted(x.unique()))
        }).reset_index()

        return aggregated_df
    else:
        print("No datasets found.")
        return pd.DataFrame()  # Return an empty DataFrame if no data is found

# Function to save the aggregated DataFrame directly to a CSV file
def save_aggregated_to_csv(aggregated_df, filename=output_file_path):
    try:
        aggregated_df.to_csv(filename, index=False)
        print(f"Aggregated data saved directly to {filename}.")
    except Exception as e:
        print(f"Error saving aggregated data to CSV: {e}")

# Main logic
if __name__ == "__main__":
    if not os.path.exists(input_file_path):
        print("Error: keywords.txt not found.")
    else:
        with open(input_file_path, "r", encoding="utf-8") as f:
            use_case_text = f.read()
        
        # Extract use case details
        use_cases = extract_use_case_details(use_case_text)
        
        if not use_cases:
            print("No use cases found in the provided text.")
        else:
            # Process and aggregate data directly
            aggregated_df = process_and_aggregate(use_cases)
            
            if not aggregated_df.empty:
                # Save the aggregated data directly to a single CSV file
                save_aggregated_to_csv(aggregated_df)
