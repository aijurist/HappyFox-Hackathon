import asyncio
from crawl4ai import *
import json

#custom imports
from github_crawler.utils import link_extraction_chain
from github_crawler.code_eval import code_eval_chain
from config import llm
from github_crawler.all_links import recursive_crawl
from github_crawler.file_extractor import extract_and_combine_code


async def analyze_links(url: str):
    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            exclude_external_links=True,
            exclude_social_media_links=True,
            exclude_domains=["facebook.com", "twitter.com"],
            excluded_tags=['form', 'header', 'footer', 'nav'],
            wait_for="js:() => window.loaded === true"
            # css_selector='.clearfix container-xl px-md-4 px-lg-5 px-3'
        )
        result = await crawler.arun(url=url, config=config)
        print(f"Found {len(result.links['internal'])} internal links")
        print(f"Found {len(result.links['external'])} external links")
        # print(result.links)
        for link in result.links['internal']:
            print(f"Href: {link['href']}\nText: {link['text']}\n")
        return result.links


def get_links(input_text):
    '''Function to invoke the chain for the given input text and style'''
    #chain invoking to extract required links
    result = link_extraction_chain.invoke({
        "input_text": input_text,
    })
    print(json.dumps(result, indent=4))
    return result

def code_eval(input_code):
    '''Function to invoke the chain for the given input text and style'''
    #chain invoking to extract required links
    result = code_eval_chain.invoke({
        "input_text": input_code,
    })
    print(json.dumps(result, indent=4))
    return result

def code_eval_test(chunks):
    all_optimizations = []
    all_vulnerabilities = []
    optimization_id = 1
    vulnerability_id = 1

    for idx, input_code in enumerate(chunks):
        try:
            # Invoke the chain for each chunk
            result = code_eval_chain.invoke({
                "input_text": input_code,
            })

            # Ensure result is a valid dict
            if isinstance(result, str):
                result = json.loads(result)

            # Process and aggregate optimizations
            for opt in result.get("optimization", []):
                opt["id"] = optimization_id
                all_optimizations.append(opt)
                optimization_id += 1

            # Process and aggregate vulnerabilities
            for vuln in result.get("vulnerability", []):
                vuln["id"] = vulnerability_id
                all_vulnerabilities.append(vuln)
                vulnerability_id += 1

        except json.JSONDecodeError as json_err:
            print(f"JSON Parsing Error in chunk {idx}: {json_err}")
            continue  # Skip the problematic chunk

        except Exception as e:
            print(f"Error processing chunk {idx}: {e}")
            continue  # Continue with next chunk even if one fails

    # Final aggregated result
    aggregated_result = {
        "optimization": all_optimizations,
        "vulnerability": all_vulnerabilities
    }

    print(json.dumps(aggregated_result, indent=4))
    return aggregated_result

def model_repo_eval(url):
    res = asyncio.run(recursive_crawl(url))
    combined_code = asyncio.run(extract_and_combine_code(res))
    print(combined_code)
    
    code_evaluvation_res = code_eval(combined_code)
    print(json.dumps(code_evaluvation_res, indent=4))
    return res

# if __name__ == '__main__':
#     model_repo_eval('https://github.com/unclecode/crawl4ai')