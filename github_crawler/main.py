import asyncio
from crawl4ai import *
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
import json

#custom imports
from github_crawler.utils import link_extraction_chain

async def analyze_links(url: str):
    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(
            # cache_mode=CacheMode.ENABLED,
            exclude_external_links=True,
            exclude_social_media_links=True,
            exclude_domains=["facebook.com", "twitter.com"],
            excluded_tags=['form', 'header', 'footer', 'nav'],
            css_selector='.clearfix container-xl px-md-4 px-lg-5 px-3'
        )
        result = await crawler.arun(url=url, config=config)
        print(f"Found {len(result.links['internal'])} internal links")
        print(f"Found {len(result.links['external'])} external links")
        # print(result.links)
        return result.links


def get_links(input_text):
    '''Function to invoke the chain for the given input text and style'''
    #chain invoking to extract required links
    result = link_extraction_chain.invoke({
        "input_text": input_text,
    })
    print(json.dumps(result, indent=4))
    return result

if __name__ == "__main__":
    url = "https://github.com/aijurist/HappyFox-Hackathon"
    res = asyncio.run(analyze_links(url))
    links = get_links(res)
