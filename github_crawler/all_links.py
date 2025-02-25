import asyncio
from crawl4ai import *
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
import json

# custom imports
from github_crawler.utils import link_extraction_chain
from github_crawler.code_eval import code_eval_chain

async def analyze_links(url: str):
    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            exclude_external_links=True,
            exclude_social_media_links=True,
            exclude_domains=["facebook.com", "twitter.com"],
            excluded_tags=['form', 'header', 'footer', 'nav'],
            wait_for="js:() => window.loaded === true"
        )
        result = await crawler.arun(url=url, config=config)
        print(f"Found {len(result.links['internal'])} internal links")
        print(f"Found {len(result.links['external'])} external links")
        for link in result.links['internal']:
            print(f"Href: {link['href']}\nText: {link['text']}\n")
        return result.links

def get_links(input_text):
    '''Function to invoke the chain for the given input text'''
    result = link_extraction_chain.invoke({"input_text": input_text})
    print(json.dumps(result, indent=4))
    return result

def code_eval(input_code):
    '''Function to invoke the code evaluation chain'''
    result = code_eval_chain.invoke({"input_text": input_code})
    print(json.dumps(result, indent=4))
    return result

async def recursive_crawl(start_url):
    visited_folders = set()
    all_file_links = set()
    folders_to_visit = [start_url]

    while folders_to_visit:
        current_folder = folders_to_visit.pop()
        if current_folder in visited_folders:
            continue

        print(f"Analyzing: {current_folder}")
        links = await analyze_links(current_folder)
        extracted_links = get_links(links)

        # Collect file links
        all_file_links.update(extracted_links.get("file_links", []))

        # Add new folder links to the queue
        new_folders = extracted_links.get("folder_links", [])
        for folder_link in new_folders:
            if folder_link not in visited_folders:
                folders_to_visit.append(folder_link)

        visited_folders.add(current_folder)

    print("\nAll Discovered File Links:")
    for file_link in all_file_links:
        print(file_link)

    return list(all_file_links)

if __name__ == "__main__":
    start_url = "https://github.com/unclecode/crawl4ai"
    asyncio.run(recursive_crawl(start_url))
