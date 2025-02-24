import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
import json

# custom imports
from content.schema import OutputSchema
from config import llm
load_dotenv()

def create_chain(llm, parser, prompt):
    '''Creates a chain by connecting the prompt template, llm and the output parser'''
    chain = prompt | llm | parser
    return chain 


parser = JsonOutputParser(pydantic_object=OutputSchema)

prompt = PromptTemplate(
    template='''Given the following input text: "{input_text}", and the requested style: "{style}", enhance the text by correcting any 
    grammatical errors, improving the overall structure, and rephrasing it to make it sound more fluent and coherent, 
    according to the specified style. The goal is to generate a clearer, more polished version of the text while preserving the original meaning.

    Depending on the style, the text should be adjusted:
    - For "Shakespearean", make the language more poetic and old-fashioned.
    - For "concise", make the text shorter while maintaining key points.
    - For "explain in detail", expand the content and clarify any ambiguous points.
    - Any other styles should be interpreted based on the context of the text.
    - If no style is given, keep the information as simple, only enhancing the grammatical errors

    Additionally, generate a list of suggestions (choices) related to the content of the text that a user can select from. The suggestions should be contextually relevant and designed to guide the user in refining or expanding the given content.

    Return the output in the following JSON format: {format_instruction}''',
    input_variables=["input_text", "style"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

content_generation_chain = create_chain(llm, parser, prompt)

def get_enhanced_content(input_text, style):

    # Invoke the chain to generate the content choices
    result = content_generation_chain.invoke({
        "input_text": input_text,
        "style": style
    })

    # Print the result (choices generated)
    print(json.dumps(result, indent=4))
    return result

# if __name__ == "__main__":
#     main()