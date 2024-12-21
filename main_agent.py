import subprocess
import sys
import os

def run_agents():
    # Use the current Python interpreter
    python_executable = sys.executable

    # Define a list of URLs to pass to the agents
    urls = [
        "https://www.tatamotors.com",          # Automotive
        #"https://www.mahindra.com",            # Automotive
        #"https://www.dlf.in",                  # Real Estate
        ##"https://www.infosys.com",             # IT Services
        #"https://www.hdfcbank.com",            # Finance
        #"https://www.apollohospitals.com",     # Healthcare
        #"https://www.drreddys.com",            # Pharmaceuticals
        #"https://www.flipkart.com/",           # E-commerce/Retail
        #"https://byjus.com/"                   # Education
        ]

    
    # Define the path to the agents folder
    agents_folder = os.path.join("agents")

    # Loop through the URLs and run the agents for each URL
    for url in urls:
        # Run Agent 1 (Web Scraper) with the correct path to agent1_webscrap.py
        print(f"Running Agent 1 (Web Scraper) for URL: {url}")
        #subprocess.run([python_executable, os.path.join(agents_folder, "agent1_webscrap.py"), url])
        
        # Run Agent 2 (Use Case Generator)
        print("Running Agent 2 (Use Case Generator)...")
        #subprocess.run([python_executable, os.path.join(agents_folder, "agent2_usecase.py")])
        
        # Run Agent 3 (Resource Collector)
        print("Running Agent 3 (Resource Collector)...")
        subprocess.run([python_executable, os.path.join(agents_folder, "agent3_resources.py")])

        

    print("All agents executed.👍")

if __name__ == "__main__":
    run_agents()
