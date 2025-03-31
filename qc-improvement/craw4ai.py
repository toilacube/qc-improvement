import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

async def main():
    browser_config = BrowserConfig()  # Default browser configuration
    run_config = CrawlerRunConfig(excluded_tags=['img'])   # Default crawl run configuration

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.lottemart.vn/login",
            config=run_config
        )
        with open("../json/html.md", "w", encoding="utf-8") as f:
            f.write(result.cleaned_html)

if __name__ == "__main__":
    asyncio.run(main())