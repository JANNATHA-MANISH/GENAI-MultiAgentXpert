# Multi-Agent AI Use Case Generator

## **Project Overview**
The Multi-Agent AI Use Case Generator is designed to extract information from company websites, identify company-specific details, and generate AI/ML use cases that enhance business operations, customer experience, and efficiency. The system uses cutting-edge APIs such as Jina AI for web scraping and Gemini/OpenAI for language processing.

---

## **Project Architecture**

### **Folder Structure:**
```
/Multi-agent architecture
│
├── /agents
│   ├── agent_1_web_scraper.py           # Extracts webpage text using Jina AI Reader API
│   ├── agent_2_use_case_generator.py    # Extracts company details & generates AI/ML use cases
│   ├── agent_3_resource_collector.py    # Collects relevant datasets and resources
│   └── main_agent_executor.py           # Orchestrates agent execution
│
├── /data
│   ├── use_cases.csv                    # CSV output of generated AI/ML use cases
│   ├── use_cases.txt                    # Detailed text file of use cases
│   └── resource_links.txt               # Dataset links from Kaggle/HuggingFace
│
├── requirements.txt                     # Project dependencies
└── config.py                            # API keys and configurations
```

---

## **Agents Overview**

### **1. Agent 1: Web Scraper**
- **Description:** Extracts textual content from company websites using the Jina AI Reader API.
- **Functionality:**
  - Sends HTTP GET requests.
  - Extracts and cleans webpage content.
  - Saves the extracted text into `extracted_text.txt`.

### **2. Agent 2: Use Case Generator**
- **Description:** Identifies company details (name, industry, services, mission) and generates AI/ML use cases.
- **Functionality:**
  - Uses OpenAI/Gemini APIs to process text.
  - Extracts company-specific data points.
  - Generates detailed AI/ML use cases with these components:
    - **Use Case Title**
    - **Objective:** Business goal
    - **AI Application:** Proposed AI/ML solution
    - **Cross-Functional Benefits:** Benefits across relevant departments
  - Saves the output in `use_cases.csv` and `use_cases.txt`.

### **3. Agent 3: Resource Collector**
- **Description:** Collects relevant datasets from online sources like Kaggle and HuggingFace.
- **Functionality:**
  - Searches relevant datasets based on use cases.
  - Extracts and stores dataset links in `resource_links.txt`.

### **4. Main Agent Executor**
- **Description:** Coordinates all agents and manages the workflow.
- **Functionality:**
  - Executes agents sequentially.
  - Handles task dependencies and process monitoring.

---

## **Installation and Setup**

### **1. Clone the Repository:**
```bash
git clone <repository-url>
cd Multi-agent-architecture
```

### **2. Set Up Environment:**
- Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate    # On Windows
```

### **3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

### **4. Configure API Keys:**
- Update `config.py` with your API keys for Jina AI, OpenAI/Gemini, etc.

### **5. Run the Project:**
```bash
python agents/main_agent_executor.py
```

---

## **Technologies Used**
- **Web Scraping:** Jina AI Reader API
- **Language Processing:** OpenAI/Gemini API
- **File Management:** CSV and text file handling using Python’s built-in libraries

---

## **Project Workflow**
1. **Web Scraper Agent:** Extracts full webpage text.
2. **Use Case Generator Agent:** Identifies company data and generates customized AI/ML use cases.
3. **Resource Collector Agent:** Finds relevant datasets and saves links.
4. **Execution Management:** Orchestrates all agents and ensures seamless workflow.

---

## **Future Enhancements**
- Integration with LangChain for advanced task coordination.
- Cloud-based dataset collection and storage.
- Enhanced UI for easier interaction.

---

**Contributors:** [Your Name]  
**Contact:** [Your Email]  
**License:** MIT License

Let me know if you'd like additional sections or details! 🚀

