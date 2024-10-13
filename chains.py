import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv  


load_dotenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, 
        groq_api_key= os.getenv("GROQ_API_KEY"), 
        model_name="llama-3.1-70b-versatile")


    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """ 
            ### SCRAPED TEXT FROM WEBSTIE:
            {page_data}
             ### INSTRUCTION:
             The scraped text is from the careers's page of website.
             Your job is to extract the job postings and retun them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
        )
        
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke (input = {"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException as e:
            raise OutputParserException("Context too big. Unable to parse jobs")
        return res if isinstance(res,list) else [res]
    
    def write_email(self, job, links):
        email_prompt = PromptTemplate.from_template(
             """ 
            ### JOB DESCRIPTION
            {job_description}

            ### INSTRUCTION
            You are hamza, a business development executive at Apex Soft. Apex Soft
            is an AI & Software consulting firm. We help seamless integration of business processes through automated tools. Over out experience we have 
            empowered numerous enterprises with tailored soltions, fostering job process optimzation, cost reduction, and heightened overall efficiency.
            Your job is to write a cold email to the client regardging the job mentioned above describing the demands to fulfil the needs.
            Add most relevents ones from following links to showcase Apex Soft portfolio: {link_list}
            """
        )
        chain_email = prompt_email | llm
        res = chain_email.invoke(input = {"job_description": job["description"], "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))