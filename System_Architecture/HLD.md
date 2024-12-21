
---

# **High-Level Design (HLD) for Multi-Agent Automation System**

---

## **1. System Overview**
The **Multi-Agent Automation System** is a modular architecture designed to perform web scraping, use case generation, and resource collection. The system leverages **Retrieval-Augmented Generation (RAG)** and **LangChain** for orchestration, ensuring an efficient workflow. It retrieves information from websites using a web scraper, generates use cases using the **Gemini AI API**, and stores relevant resource links in CSV format.

This system aims to simplify data extraction, use case generation, and resource collection by automating each task with dedicated agents.

---


#### **External Interfaces**:
- **Jina AI API**: Used by Agent 1 for text extraction from web pages.
- **Google Gemini API**: Used by Agent 2 for generating AI/ML use cases.
- **Kaggle API**: Used by Agent 3 to fetch datasets.

---
## **2.System Architecture**

The system follows a modular approach, where the main controller (`main_agent.py`) manages the workflow by coordinating three independent agents. Each agent handles a specific task.

### **Architecture Diagram**:


```
                          +-------------------------------+
                          |       Main Controller        |
                          |         main_agent.py        |
                          +-------------------------------+
                                     |     |     |
        -----------------------------+     |     +--------------------------------
        |                                  |                                  |
+------------------------+    +------------------------+    +------------------------+
|   Agent 1: Web Scraper |    | Agent 2: Use Case Gen  |    | Agent 3: Resource Coll |
|    agent1_webscrap.py  |    |  agent2_usecase.py     |    |  agent3_resource.py    |
+------------------------+    +------------------------+    +------------------------+
        |                         |                         |
        |                         |                         |
+------------------------+   +------------------------+   +------------------------+
|   Extracted Text File  |   |  Generated Use Cases   |   |   Downloaded Datasets  |
|   extracted_text.txt   |   | use_cases.txt          |   |   resource_links.csv   |
+------------------------+   +------------------------+   +------------------------+
                                     |
                          +------------------------+
                          |                        |
                          |   keywords.txt         |
                          +------------------------+
```

---

## **3.Database Design**

This system doesn't use a traditional database but relies on file-based storage to store outputs from each agent:

### **Data Storage Files**:
| **File Name**          | **Data Type**   | **Description**                                      |
|------------------------|-----------------|------------------------------------------------------|
| `extracted_text.txt`   | Plain Text      | Stores the extracted text from the web scraping agent. |
| `use_cases.txt`        | Plain Text      | Stores the generated use cases from the Gemini AI API. |
| `keywords.txt`         | Plain Text      | Stores the list of relevant keywords extracted during scraping. |
| `resource_links.csv`   | CSV             | Stores the resource links related to use cases.        |

---

## **Modules, Services, and Relationships**

### **Modules and Their Responsibilities**:

1. **Main Controller (`main_agent.py`)**:
   - Orchestrates the workflow and coordinates the execution of agents using LangChain.
   - Handles the sequential flow of tasks between agents.
   - Monitors the system's status and generates logs for tracking progress.
   
2. **Agent 1: Web Scraper (`agent1_webscrap.py`)**:
   - Scrapes websites using libraries such as `requests` and `BeautifulSoup`.
   - Extracts relevant text and saves it to `extracted_text.txt`.
   - Identifies keywords from the extracted text and stores them in `keywords.txt`.
   
3. **Agent 2: Use Case Generator (`agent2_usecase.py`)**:
   - Uses the **Gemini AI API** to generate use cases based on the extracted text.
   - Processes the extracted text from `extracted_text.txt`.
   - Saves generated use cases to `use_cases.txt`.
   
4. **Agent 3: Resource Collector (`agent3_resource.py`)**:
   - Collects relevant resource links based on the generated use cases.
   - Stores the resource links in `resource_links.csv`.

---

## **4.Hardware, Software, and Interfaces**

### **Hardware Requirements**:
- **Processor**: Intel Core i5 or higher.
- **RAM**: Minimum of 8 GB (16 GB recommended).
- **Storage**: At least 10 GB of available storage.

### **Software Requirements**:
- **Operating System**: Windows 10, Linux, or macOS.
- **Programming Language**: Python 3.9 or later.
- **Virtual Environment**: `menv` (Python virtual environment).
  
### **Software Interfaces**:
| **Interface**               | **Description**                                          |
|-----------------------------|----------------------------------------------------------|
| **Gemini AI API**           | For generating use cases based on input text.            |
| **File System Interface**   | To save and load text files and CSV.                     |
| **LangChain**                | Orchestrates the flow between agents and manages interactions. |

---
### **User Interfaces**:
Since the system is designed to run from the command line, the user interacts with the system using minimal input:
- **CLI Commands**: Execute `python main_agent.py` to trigger the automation process.
- **Logs and Outputs**: Logs the progress and outputs the results into respective files in the `data/` folder.

---

## **5.Workflow of the User Process**

### **Workflow Diagram**:
1. **User Action**: The user runs `main_agent.py` via the command line.
2. **System Process**:
   - **Agent 1 (Web Scraper)** extracts text from the provided URLs and stores it in `extracted_text.txt`.
   - **Agent 2 (Use Case Generator)** uses the Gemini AI API to generate use cases based on the scraped text and stores them in `use_cases.txt`.
   - **Agent 3 (Resource Collector)** identifies and collects relevant resource links, saving them to `resource_links.csv`.

---

## **6. Performance Specifications**

| **Criteria**            | **Specification**                                       |
|------------------------|---------------------------------------------------------|
| **Scalability**         | Agents can be extended with minimal code changes for additional tasks. |
| **Execution Time**      | Time taken varies depending on the complexity of the URLs and data retrieval. |
| **Reliability**         | Robust error handling and logging ensure fault tolerance. |
| **Resource Utilization**| Moderate CPU and memory usage. Optimal for small to medium-sized tasks. |
| **Security**            | API keys are securely stored in the `.env` file.         |

---

### **7. Data Dictionary**

A **Data Dictionary** provides a detailed description of the data used throughout the system.

| **Data Name**             | **Description**                                                            | **Data Type**   | **Source/Target**                  |
|---------------------------|----------------------------------------------------------------------------|-----------------|------------------------------------|
| **URLs**                   | List of URLs to scrape from the web.                                        | List of Strings | Input (from user)                 |
| **Extracted Text**         | Text extracted from a web page.                                             | Text (String)   | Output (from Agent 1)             |
| **Use Cases**              | AI/ML use cases generated from the extracted text.                          | Text (String)   | Output (from Agent 2)             |
| **Keywords**               | Keywords related to AI/ML use cases.                                       | List of Strings | Output (from Agent 2)             |
| **Dataset Information**    | Information about datasets from Kaggle (name, URL).                        | List of Tuples  | Output (from Agent 3)             |
| **resource_links.csv**     | A CSV file containing dataset names and URLs.                              | CSV File        | Output (from Agent 3)             |
| **use_cases.txt**          | A text file containing the AI/ML use cases.                                | Text File       | Output (from Agent 2)             |
| **keywords.txt**           | A text file containing the extracted keywords for use case generation.     | Text File       | Output (from Agent 2)             |
| **extracted_text.txt**     | A text file containing the extracted plain text from the webpage.          | Text File       | Output (from Agent 1)             |

---

### **8.Flow Diagrams for agents**

The **flowchart** for the overall system and each agent can be broken down as follows:

#### **Main Agent Flowchart**
```plaintext
            +--------------------------+
            |  Start (Main Agent)      |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Load URLs from Input    |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Run Agent 1 (Scraping)  |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Run Agent 2 (Use Cases) |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Run Agent 3 (Resources) |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Finish Process           |
            +--------------------------+
```

#### **Agent 1 (Web Scraping) Flowchart**
```plaintext
            +--------------------------+
            |  Start (Agent 1)         |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Fetch URL from Input    |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Call Jina AI API        |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Extract Text            |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Save Extracted Text     |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Finish Agent 1          |
            +--------------------------+
```

#### **Agent 2 (Use Case Generation) Flowchart**
```plaintext
            +--------------------------+
            |  Start (Agent 2)         |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Read Extracted Text     |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Call Google Gemini API  |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Generate Use Cases      |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Save Use Cases          |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Save keywords           |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Finish Agent 2          |
            +--------------------------+
```

#### **Agent 3 (Resource Collection) Flowchart**
```plaintext
            +--------------------------+
            |  Start (Agent 3)         |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Read Keywords from File |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Call Kaggle API         |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Collect Datasets        |
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Save Dataset Information|
            +--------------------------+
                        |
                        v
            +--------------------------+
            |  Finish Agent 3          |
            +--------------------------+
```

---

### **9. Decision Tables**

A **Decision Table** is useful for complex decision-making based on certain conditions. Here’s a decision table for handling potential errors during the text extraction process (Agent 



| **Condition**                          | **Action 1**                    | **Action 2**                   | **Action 3**                    |
|----------------------------------------|---------------------------------|--------------------------------|---------------------------------|
| URL is valid                           | Proceed with extraction         | Log error: Invalid URL         | Retry or Terminate              |
| Text extraction is successful          | Save extracted text             |                                |                                 |
| Text extraction fails                  | Log error                       | Retry extraction or Terminate  |                                 |

---


## **Summary**

This **High-Level Design (HLD)** provides an overview of the architecture, modules, services, and data flow for the Multi-Agent Automation System. The system efficiently extracts data, generates insights, and retrieves resource links with minimal user intervention. By using RAG, LangChain, and Gemini AI API, it enhances the capabilities of automation with advanced data processing and orchestration.
