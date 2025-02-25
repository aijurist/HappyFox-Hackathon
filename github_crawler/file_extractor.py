import asyncio
from crawl4ai import *
#custom imports
from github_crawler.all_links import recursive_crawl

async def file_code_extractor(url):
    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(
            css_selector="read-only-cursor-text-area"
        )
        result = await crawler.arun(
            url=url,
        )
        return result.markdown

async def extract_and_combine_code(file_links):
    combined_code = ""
    for file_url in file_links[:10]:
        code_content = await file_code_extractor(file_url)
        file_name = file_url.split("/")[-1]
        combined_code += f"\n# ===== {file_name} =====\n{code_content}\n"
    return combined_code


