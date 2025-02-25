from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import json

#custom import statements
from github_crawler.schema import LinkSchema
from config import llm

def create_chain(llm, parser, prompt):
    '''Creates a chain by connecting the prompt template, llm and the output parser'''
    chain = prompt | llm | parser
    return chain 

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=20000, 
        chunk_overlap=1000 
    )

parser = JsonOutputParser(pydantic_object=LinkSchema)

prompt = PromptTemplate(
    template='''Given the following extracted GitHub links: {input_text}, filter and categorize only the links that point to actual project code, specifically files and folders.

                Include only:  
                - File Links: URLs pointing to individual code files inside a repository. These follow the pattern:  
                  https://github.com/{{username}}/{{repo}}/blob/{{branch}}/{{file_path}}  
                  Convert these links to their raw content format as follows:  
                  https://raw.githubusercontent.com/{{username}}/{{repo}}/{{branch}}/{{file_path}}  

                - Folder Links: URLs pointing to directories or subdirectories inside a repository. These follow the pattern:  
                  https://github.com/{{username}}/{{repo}}/tree/{{branch}}/{{folder_path}}  

                Ignore:  
                - Repository overview pages, such as https://github.com/{{username}}/{{repo}} 
                - Github Settings such as https://github.com/{{username}}/{{repo}}/.github 
                - Setup Files such as package.json, package_lock.json, requirements.txt, __init__.py and other files
                - Readme files, Code of Conduct and any markdown files
                - Test folders and documentation folders
                - User profile pages, such as https://github.com/{{username}}  
                - Repository metadata pages, including:  
                  - Stargazers (/stargazers), Forks (/forks), Branches (/branches), Tags (/tags), Activity (/activity)  
                  - Issues (/issues), Pull Requests (/pulls), Actions (/actions), Projects (/projects), Security (/security)  
                - General GitHub pages, such as https://github.com/trending, https://github.com/features/copilot  

                The goal is to extract only the relevant project code links. For file links, provide the converted raw URLs so they can be accessed directly, while folder links should remain unchanged for further exploration.

                {format_instruction}''',
    input_variables=["input_text"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)



link_extraction_chain = create_chain(llm, parser, prompt)

def generate_chunks(text_splitter, text):
    return text_splitter.split_text(text)

def summarize_thread(text_splitter, summary_chain, thread_text):
    # Step 1: Chunk the thread
    chunks = generate_chunks(text_splitter=text_splitter, text=thread_text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    # Step 2: Run Map-Reduce Summarization
    summary =summary_chain.run(docs)
    return summary