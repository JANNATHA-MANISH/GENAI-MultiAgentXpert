import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

folder_path = "./data"  # Replace with the full path to the target folder
input_file_path = os.path.join(folder_path, "extracted_text.txt")
output_file_path = os.path.join(folder_path, "use_cases.txt")
keywords_file_path = os.path.join(folder_path, "keywords.txt")
os.makedirs(os.path.dirname(keywords_file_path), exist_ok=True)  # This only ensures the folder exists

# Load environment variables from .env file
load_dotenv()

def generate_intro_with_gemini(company_name, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.67,
        google_api_key=api_key
    )
    
    # Define a prompt template for generating the introduction
    intro_prompt = PromptTemplate(
        input_variables=["company_name"],
        template="""
        Write an introductory paragraph for Generative AI & ML use cases for {company_name} in this format:
        
        GenAI & ML Use Cases for {company_name}
        newline(/n)
        As one of the leading players in the [industry] sector, {company_name} can leverage Generative AI, Large Language Models (LLMs), and Machine Learning to enhance operational efficiency, improve product quality, and expand service offerings. By utilizing AI Planet’s GenAI Stack and collaborating with a team of AI experts, {company_name} can unlock transformative AI-driven solutions that drive innovation, streamline processes, and deliver superior results across operations. With the support of cutting-edge AI technologies, {company_name} can gain a competitive edge in the market and achieve sustainable growth.     
           
         dont mention the url
                 """
    )

    # Create a chain with the prompt and LLM
    intro_chain = LLMChain(llm=llm, prompt=intro_prompt)
    
    # Generate the introduction
    return intro_chain.run({"company_name": company_name})


def generate_additional_resources_prompt(company_description, api_key):

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )
       
    additional_resources_prompt = PromptTemplate(
        input_variables=["company_description"],
        template="""
        Based on this company description: {company_description}, perform the following:

        
         Recommend agents to refer to reports and insights on AI and digital transformation from industry-specific sources like McKinsey, Deloitte, or Nexocode. Be sure to include a list of valuable reports or insights related to AI and digital transformation for the company’s industry.
        
         Conduct a search for industry-specific use cases. For example, "how is the retail industry leveraging AI and ML" or "AI applications in automotive manufacturing." Provide examples and trends in how companies in the relevant industry are implementing AI/ML technologies.

         Use the generated research from steps 2 and 3 to inform the next step where we generate specific AI/ML use cases for the company based on the description provided.

        The goal is to generate a comprehensive set of reports, use cases, and insights that can directly inform actionable AI/ML use cases for the company based on the famous insignts speciffic sources and other.
        
        Please ensure that the content is specific to the company’s industry and its operational needs.
        """
    )

    # Create a chain with the prompt and LLM
    additional_resources_chain = LLMChain(llm=llm, prompt=additional_resources_prompt)
    
    # Generate the additional resources prompt

    return additional_resources_chain.run({"company_description": company_description})

def generate_use_cases_with_gemini(company_description, api_key):

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.67,
        google_api_key=api_key
    )
    
    # Define a prompt template for generating use cases
    use_case_prompt = PromptTemplate(
        input_variables=["company_description"],
        template="""
        Based on this company description: {company_description}, generate at least 4 Generative AI & ML based on company industry department use cases in this format:
        
           Use Case Title: [Title]
           Objective/Use Case: [Objective]
           AI Application: [Specific AI technology used]
           Cross-Functional Benefit: [Impacts on operations, finance, supply chain, etc.]
        
        Ensure that each use case is unique and relevant to the company's operations and industry only.
        """
    )
    
    # Create a chain with the prompt and LLM
    use_case_chain = LLMChain(llm=llm, prompt=use_case_prompt)
    
    # Generate the use cases
    return use_case_chain.run({"company_description": company_description})

def generate_keywords_from_use_cases(use_cases, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )
    
    # Define a prompt template for generating keywords
    keywords_prompt = PromptTemplate(
        input_variables=["use_cases"],
       template = """Based on the following AI/ML use cases:

{use_cases}

For the use cases above,

Generate a list of relevant keywords that can be used to search datasets on platforms like Kaggle or Hugging Face. These keywords should be in the following format:

**Use Case Title:** 
**Description:** 
**Keywords:** 

The keywords should include technologies, methods, applications, and relevant industry terms. Ensure that the formatting matches the example provided:  
- Use **bold** for "Use Case Title", "Description", and "Keywords" labels only (not the content).
- The **title** should be capitalized correctly and maintain consistent formatting.
- Ensure that **keywords** are separated by commas, with no extra punctuation or line breaks.
- Provide only one unbroken paragraph for each entry.

Do not provide the information in any other format.
"""
)

    
    # Create a chain with the prompt and LLM
    keywords_chain = LLMChain(llm=llm, prompt=keywords_prompt)
    
    # Generate the keywords
    return keywords_chain.run({"use_cases": use_cases})



# Save output to a file
def save_output_to_file(output, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)


# Main logic
if __name__ == "__main__":
    # Load extracted text (company description) from a file
    if not os.path.exists(input_file_path):
        print("Error: extracted_text.txt not found.")
    else:
        with open(input_file_path, "r", encoding="utf-8") as f:
            extracted_text = f.read().strip()
        
        google_api_key = os.getenv("GOOGLE_API_KEY")  
        
        if not google_api_key:
            print("Error: GOOGLE_API_KEY not found in environment variables.")
        else:
            try:
                # Step 1: Generate introductory paragraph
                company_name = extracted_text.split(".")[0]  # Extract company name from text (first sentence)
                intro = generate_intro_with_gemini(company_name, google_api_key)

                additional_resources = generate_additional_resources_prompt(extracted_text, google_api_key)

                use_cases = generate_use_cases_with_gemini(extracted_text, google_api_key)

                keywords = generate_keywords_from_use_cases(use_cases, google_api_key)
                
                # Combine intro and use cases
                full_output = f"{intro}\n\n{use_cases}"
                
                # Save to file
                save_output_to_file(full_output, output_file_path)
                save_output_to_file(keywords, keywords_file_path)

                
                print("Use cases generated successfully.")
             

            except Exception as e:
                print(f"Error: {e}")