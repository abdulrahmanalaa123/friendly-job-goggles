import ddgs
import re, validators, asyncio
from crawl4ai import AsyncWebCrawler

async def guess_domain(company_name):
    query = f"{company_name} official site"
    urls = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            urls.append(r['href'])
    print("the urls for{comapny} is",domains)


    # Filter social / irrelevant
    skip_domains = ["linkedin.com", "wikipedia.org", "facebook.com",
                    "twitter.com", "youtube.com", "glassdoor.com"]
    candidates = [u for u in urls if all(s not in u for s in skip_domains)]

    # Normalize & validate
    domains = []
    for u in candidates:
        m = re.search(r"https?://([^/]+)", u)
        if m:
            host = m.group(1)
            if validators.domain(host):
                domains.append(host)
    print("the domains for{comapny} is",domains)
    # Optionally verify via Crawl4AI that the page mentions the company
    async with AsyncWebCrawler() as crawler:
        for d in domains:
            res = await crawler.arun(url=f"https://{d}")
            text = res.markdown.raw_markdown.lower()
            if company_name.lower() in text[:2000]:  # appears early on page
                return d
    return domains[0] if domains else None

async def main():
    companies = ["Canonical", "Stripe", "Mozilla", "SpaceX"]
    for c in companies:
        d = await guess_domain(c)
        print(f"{c:15} -> {d}")

if __name__ == "__main__":
    asyncio.run(main())
