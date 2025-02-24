from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from thread_summarizer.utils import generate_chunks, summarize_thread
from config import llm

def summarize_long_thread(thread_text):
    """
    Summarizes a long forum thread using map-reduce summarization.

    Args:
        thread_text (str): The input text of the forum thread.

    Returns:
        str: The summarized thread.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, 
        chunk_overlap=200 
    )

    summarization_chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        verbose=True
    )

    summary = summarize_thread(
        text_splitter=text_splitter,
        summary_chain=summarization_chain,
        thread_text=thread_text
    )
    
    return summary
