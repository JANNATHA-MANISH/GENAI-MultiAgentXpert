## **Low-Level Design (LLD) for**
### **Multi-Agent Architecture**

The **Low-Level Design (LLD)** focuses on the specific modules, classes, functions, methods, variables, and their interactions for implementing the system. In the case of the **multi-agent architecture**, we break down each agent, module, and component to ensure a detailed, executable, and well-organized solution that adheres to the functional specifications.

In this **LLD**, we will cover each component involved in the architecture and provide detailed information on implementation, including coding practices, execution flow, and integration steps.

---

### **1. Main Agent (main_agent.py)**

#### **Purpose**:
- Orchestrates the execution of other agents (Agent 1, Agent 2, Agent 3).
- Manages the flow of data between agents.

#### **Modules & Components**:
- **URL List**: A list of URLs to be processed.
- **Subprocess Management**: Launches subprocesses to run Agent 1, Agent 2, and Agent 3.
- **Error Handling**: Handles errors in subprocess execution.
- **Logging**: Logs each step of the agent execution.

#### **Flow**:
1. **Input**: A list of URLs is provided.
2. **URL Processing**:
   - The script iterates over the URLs.
   - For each URL, it invokes `subprocess.run()` to start the scraping process (Agent 1).
   - After Agent 1 completes, the script triggers Agent 2 and then Agent 3.
3. **Output**: Logs the progress and errors to a log file and indicates when all agents are executed.

#### **Detailed Functionality**:
```python
import subprocess
import sys
import os

def run_agents():
    python_executable = sys.executable  # Current Python executable path

    # List of URLs to process
    urls = [
        "https://www.tatamotors.com",  # Example URL
        # Add more URLs as needed
    ]

    agents_folder = os.path.join("agents")  # Folder containing agents

    # Loop through each URL and process with agents
    for url in urls:
        print(f"Running Agent 1 (Web Scraper) for URL: {url}")
        subprocess.run([python_executable, os.path.join(agents_folder, "agent1_webscrap.py"), url])
        
        print("Running Agent 2 (Use Case Generator)...")
        subprocess.run([python_executable, os.path.join(agents_folder, "agent2_usecase.py")])
        
        print("Running Agent 3 (Resource Collector)...")
        subprocess.run([python_executable, os.path.join(agents_folder, "agent3_resources.py")])

    print("All agents executed.👍")

if __name__ == "__main__":
    run_agents()
```

#### **Execution Details**:
- The main agent runs each agent sequentially for every URL.
- Error handling: If any subprocess fails, it will print an error message but continue processing other agents.

---

### **2. Agent 1: Web Scraping (agent1_webscrap.py)**

#### **Purpose**:
- Scrapes the provided URL to extract text using Jina AI API.
  
#### **Modules & Components**:
- **Environment Variables**: Loads API keys from `.env`.
- **API Request**: Makes a GET request to Jina AI’s Reader API for text extraction.
- **File Management**: Saves extracted content into `extracted_text.txt`.

#### **Flow**:
1. **Input**: Receives the URL as a command-line argument.
2. **Text Extraction**:
   - Sends a request to Jina AI's API with the URL.
   - Receives the extracted text.
3. **Output**: Writes the extracted text to `data/extracted_text.txt`.

#### **Detailed Functionality**:
```python
import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Fetches the plain text from a webpage using Jina AI API
def fetch_page_text_with_jina(url, api_key=None):
    reader_url = f"https://r.jina.ai/{url}"
    
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
    
    try:
        response = requests.get(reader_url, headers=headers)
        response.raise_for_status()  # Raise an error for any HTTP issue
        return response.text
    except Exception as e:
        return f"Error occurred: {e}"

# Main logic
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
            os.makedirs("./data", exist_ok=True)
            with open("./data/extracted_text.txt", "w", encoding="utf-8") as file:
                file.write(extracted_text)
            print(f"Text extraction completed and saved.")
        except Exception as e:
            print(f"Error saving file: {e}")
    else:
        print("Text extraction failed.")
```

#### **Execution Details**:
- The `url` is passed via the command line.
- The Jina AI API is queried for text extraction.
- The text is saved in a `.txt` file in the `data` directory.

---

### **3. Agent 2: Use Case Generation (agent2_usecase.py)**

#### **Purpose**:
- Reads the extracted text and generates AI/ML use cases and additional insights using Google Gemini AI.

#### **Modules & Components**:
- **Input Handling**: Reads `extracted_text.txt` to retrieve company information.
- **AI Model (Google Gemini)**: Interacts with the Gemini AI model via Langchain to generate use cases.
- **Output Handling**: Writes the generated use cases and keywords to `use_cases.txt` and `keywords.txt`.

#### **Flow**:
1. **Input**: Reads `extracted_text.txt`.
2. **Use Case Generation**:
   - Interacts with Gemini AI to generate an introductory paragraph and AI/ML use cases.
   - Extracts keywords for each use case.
3. **Output**: Saves the generated use cases and keywords into text files.

#### **Detailed Functionality**:
```python
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

def generate_intro_with_gemini(company_name, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.67,
        google_api_key=api_key
    )

    intro_prompt = PromptTemplate(
        input_variables=["company_name"],
        template="""
        Write an introductory paragraph for Generative AI & ML use cases for {company_name}...
        """
    )

    intro_chain = LLMChain(llm=llm, prompt=intro_prompt)
    return intro_chain.run({"company_name": company_name})

def generate_use_cases_with_gemini(company_description, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.67,
        google_api_key=api_key
    )

    use_case_prompt = PromptTemplate(
        input_variables=["company_description"],
        template="""
        Based on this company description: {company_description}, generate at least 4 Generative AI & ML use cases...
        """
    )

    use_case_chain = LLMChain(llm=llm, prompt=use_case_prompt)
    return use_case_chain.run({"company_description": company_description})

def generate_keywords_from_use_cases(use_cases, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )

    keywords_prompt = PromptTemplate(
        input_variables=["use_cases"],
        template="""
        Based on the following AI/ML use cases: {use_cases}, generate a list of relevant keywords...
        """
    )

    keywords_chain = LLMChain(llm=llm, prompt=keywords_prompt)
    return keywords_chain.run({"use_cases": use_cases})

def save_output_to_file(output, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output)

# Main logic
if __name__ == "__main__":
    if not os.path.exists("./data/extracted_text.txt"):
        print("Error: extracted_text.txt not found.")
    else:
        with open("./data/extracted_text.txt", "r", encoding="utf-8") as file:
            extracted_text = file.read().strip()
        
        google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not google_api_key:
            print("Error: GOOGLE_API_KEY not found.")
        else:
            try:
                intro = generate_intro_with_gemini(extracted_text.split(".")[0], google_api_key)
                use_cases = generate_use_cases_with_gemini(extracted_text, google_api_key)
                keywords = generate_keywords_from_use_cases(use_cases, google_api_key)

                save_output_to_file(f"{intro}\n\n{use_cases}", "./data/use_cases.txt")
                save_output_to_file(keywords, "./data/keywords.txt")

                print("Use cases generated successfully.")
            except Exception as e:
                print(f"Error: {e}")


```

#### **Execution Details**:
- Reads `extracted_text.txt`.
- Uses Google Gemini AI to generate an introduction and AI/ML use cases.
- Extracts keywords related to the use cases and saves them in `use_cases.txt` and `keywords.txt`.

---

### **4. Agent 3: Resource Collection (agent3_resources.py)**

#### **Purpose**:
- Queries Kaggle API to search for datasets based on extracted keywords.

#### **Modules & Components**:
- **Kaggle API**: Utilizes the Kaggle API to search for relevant datasets.
- **File Management**: Saves dataset links and details to `resource_links.csv`.

#### **Flow**:
1. **Input**: Reads keywords from `keywords.txt`.
2. **Dataset Collection**:
   - Uses Kaggle API to search for datasets based on the keywords.
   - Aggregates dataset information (links, dataset names).
3. **Output**: Saves dataset details to a CSV file.

#### **Detailed Functionality**:
```python
import os
import kaggle
import csv

def fetch_datasets_from_kaggle(keyword):
    # Fetch datasets from Kaggle based on the provided keyword
    datasets = kaggle.api.datasets_list(search=keyword)
    return [(dataset.title, dataset.url) for dataset in datasets]

def save_datasets_to_csv(dataset_info):
    with open("./data/resource_links.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Dataset Name", "Dataset URL"])
        writer.writerows(dataset_info)

# Main logic
if __name__ == "__main__":
    if not os.path.exists("./data/keywords.txt"):
        print("Error: keywords.txt not found.")
    else:
        with open("./data/keywords.txt", "r", encoding="utf-8") as file:
            keywords = file.readlines()

        dataset_info = []
        for keyword in keywords:
            datasets = fetch_datasets_from_kaggle(keyword.strip())
            dataset_info.extend(datasets)

        save_datasets_to_csv(dataset_info)
        print("Resource links saved successfully.")
```

#### **Execution Details**:
- Reads `keywords.txt`.
- Queries the Kaggle API for relevant datasets based on each keyword.
- Saves the dataset details to `resource_links.csv`.

---

## **Error Handling and Logging**
- **Network Errors:**
  - Retry logic for API calls and web scraping.
  - Log detailed error messages in a `logs/` directory.

- **File I/O Errors:**
  - Check file existence before read/write operations.
  - Handle `FileNotFoundError` and log issues.

- **Invalid Inputs:**
  - Validate URLs using regular expressions.
  - Return appropriate error messages to the user.

---

## **Testing and Validation**
### **Unit Tests:**
| **Module**        | **Function**          | **Test Case**                                      |
|-------------------|-----------------------|--------------------------------------------------|
| `agent1_webscrap` | `fetch_webpage`       | Validate correct HTML response for valid URLs.   |
| `agent1_webscrap` | `parse_html`          | Ensure extracted text excludes HTML tags.        |
| `agent2_usecase`  | `extract_keywords`    | Validate keyword extraction from sample text.    |
| `agent2_usecase`  | `generate_use_cases`  | Ensure use cases are generated for given input.  |

### **Integration Tests:**
- Test the entire pipeline from URL input to output files.
- Validate data integrity at each step.

---

### **Conclusion**
The **Low-Level Design (LLD)** for this **multi-agent architecture** outlines the specific steps, functions, and code required to implement each agent in the system. Each agent focuses on a single task, from scraping web content to generating use cases and collecting datasets, and integrates smoothly with the next agent in the sequence.
