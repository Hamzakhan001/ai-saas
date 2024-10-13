import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text 


def create_streamlit_app(llm,portfolio,clean_text):
    st.title("Cold Email Generator")
    input_url = st.text_input("Enter a url to scrap", value='https://jobs.nike.com/job/R-40387')
    submit_btn = st.button("Submit")


    if submit_btn:
        try:
            loader = WebBaseLoader([input_url])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills',[])
                links = portfolio.query_links(skills)
                email = llm.write_email(job,links)
                st.code(email,language='markdown')
        except Exception as e:
            st.error(f"An error occured: {e}")
                
