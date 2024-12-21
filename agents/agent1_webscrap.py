import requests
import os
import sys
from dotenv import load_dotenv
load_dotenv()


# Specify the relative path to the folder where you want to save the file
folder_path = "./data"  # Replace with the full path to the target folder
file_path = os.path.join(folder_path, "extracted_text.txt")

# Jina AI-based extraction function
def fetch_page_text_with_jina(url, api_key=None):
    """
    Fetches and extracts clean text content from a webpage using Jina AI's Reader API.
    
    Args:
        url (str): The URL of the webpage to scrape.
        api_key (str, optional): Your Jina AI API key. Defaults to None.
    
    Returns:
        str: The extracted plain text content of the webpage.
    """
    # Prepend the base Reader API URL to the target URL
    reader_url = f"https://r.jina.ai/{url}"
    
    # Add headers for authentication if an API key is provided
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
    
    try:
        # Send a GET request to the Reader API
        response = requests.get(reader_url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Return the extracted text content
        return response.text
    
    except Exception as e:
        return f"Error occurred: {e}"

# Main logic
if __name__ == "__main__":
    # Retrieve the URL passed as an argument
    if len(sys.argv) < 2:
        print("No URL provided.")
        sys.exit(1)
    url = sys.argv[1]
    print(f"Scraping URL: {url}")   
    
    api_key = os.environ.get("JINA_API_KEY")
    # Use Jina AI to extract text
    extracted_text = fetch_page_text_with_jina(url, api_key)
    
    # Check if extraction was successful and handle the file saving
    if "Error" not in extracted_text:
        try:
            os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)  # Save extracted text to file
            print(f"Text extraction completed and saved to {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
    else:
        print("Text extraction failed. No file was saved.")
