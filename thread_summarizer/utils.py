from langchain_google_genai import GoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

def generate_chunks(text_splitter, text):
    return text_splitter.split_text(text)

def summarize_thread(text_splitter, summary_chain, thread_text):
    # Step 1: Chunk the thread
    chunks = generate_chunks(text_splitter=text_splitter, text=thread_text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    # Step 2: Run Map-Reduce Summarization
    summary =summary_chain.run(docs)
    return summary