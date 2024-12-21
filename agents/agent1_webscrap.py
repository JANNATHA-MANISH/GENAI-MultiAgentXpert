import requests
import os
import sys
from dotenv import load_dotenv
load_dotenv()



folder_path = "./data"  
file_path = os.path.join(folder_path, "extracted_text.txt")


def fetch_page_text_with_jina(url, api_key=None):
    
    
    reader_url = f"https://r.jina.ai/{url}"
    
    
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
    
    try:
        
        response = requests.get(reader_url, headers=headers)
        response.raise_for_status()  
        
        
        return response.text
    
    except Exception as e:
        return f"Error occurred: {e}"


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("No URL provided.")
        sys.exit(1)
    url = sys.argv[1]
    print(f"Scraping URL: {url}")   
    
    api_key = os.environ.get("JINA_API_KEY")
    
    extracted_text = fetch_page_text_with_jina(url, api_key)
    
    
    if "Error" not in extracted_text:
        try:
            os.makedirs(folder_path, exist_ok=True)  
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)  
            print(f"Text extraction completed and saved to {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
    else:
        print("Text extraction failed. No file was saved.")
