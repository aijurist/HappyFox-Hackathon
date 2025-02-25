from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
import json

#custom import statements
from github_crawler.schema import LinkSchema
from config import llm

def create_chain(llm, parser, prompt):
    '''Creates a chain by connecting the prompt template, llm and the output parser'''
    chain = prompt | llm | parser
    return chain 


parser = JsonOutputParser(pydantic_object=LinkSchema)

prompt = PromptTemplate(
    template='''Given the following extracted GitHub links: {input_text}, filter and categorize only the links that point to actual project code, specifically files and folders.  

                Include only:  
                - File Links: URLs pointing to individual code files inside a repository. These follow the pattern:  
                  https://github.com/{{username}}/{{repo}}/blob/{{branch}}/{{file_path}}  
                - Folder Links: URLs pointing to directories or subdirectories inside a repository. These follow the pattern:  
                  https://github.com/{{username}}/{{repo}}/tree/{{branch}}/{{folder_path}}  

                Ignore:  
                - Repository overview pages, such as https://github.com/{{username}}/{{repo}}  
                - User profile pages, such as https://github.com/{{username}} 
                - Repository metadata pages, including:  
                  - Stargazers (/stargazers), Forks (/forks), Branches (/branches), Tags (/tags), Activity (/activity)  
                  - Issues (/issues), Pull Requests (/pulls), Actions (/actions), Projects (/projects), Security (/security)  
                - General GitHub pages, such as https://github.com/trending, https://github.com/features/copilot  

                The goal is to extract only the relevant project code links so that folder links can be further searched for more files without unnecessary navigation.  

                {format_instruction}''',
    input_variables=["input_text"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)


link_extraction_chain = create_chain(llm, parser, prompt)