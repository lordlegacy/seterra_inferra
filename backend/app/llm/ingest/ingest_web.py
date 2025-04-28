from apify_client import ApifyClient
from sqlalchemy.orm import Session
from app.llm.chunking import chunk_text
from app.llm.embedding import embed_texts
from app.models.web_snippet import WebSnippet
from app.core.logger import app_logger
from dotenv import load_dotenv
import os

load_dotenv()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

# Initialize the official ApifyClient once
client = ApifyClient(APIFY_API_TOKEN)

def get_search_results(query: str, max_results: int = 3) -> list[str]:
    """
    Uses Apify to search Google and return top URLs.
    """
    run_input = {
        "queries": query,   # ✅ SINGLE STRING not list
        "num": max_results,
    }

    run = client.actor("apify/google-search-scraper").call(run_input=run_input)
    urls = [item.get("url") for item in client.dataset(run["defaultDatasetId"]).iterate_items()]
    return urls


def scrape_page(url: str) -> tuple[str, str]:
    """
    Scrape a single page using Apify Website Content Crawler.
    """
    run_input = {
        "startUrls": [{"url": url}],
        "useSitemaps": False,
        "respectRobotsTxtFile": True,
        "crawlerType": "playwright:adaptive",
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg, img[src^='data:'],
[role=\"alert\"],
[role=\"banner\"],
[role=\"dialog\"],
[role=\"alertdialog\"],
[role=\"region\"][aria-label*=\"skip\" i],
[aria-modal=\"true\"]""",
        "clickElementsCssSelector": "[aria-expanded=\"false\"]",
        "proxyConfiguration": { "useApifyProxy": True }
    }

    run = client.actor("apify/website-content-crawler").call(run_input=run_input)
    results = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    if not results:
        raise ValueError("No content found during scrape.")

    title = results[0].get("title", url)
    body = results[0].get("text") or results[0].get("content") or ""

    return title, body

def chunk_and_embed(text: str) -> list[list[float]]:
    """
    Chunks and embeds text into vectors.
    """
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    return list(zip(chunks, embeddings))

def store_web_snippet(db: Session, url: str, title: str, chunk: str, embedding: list[float]):
    """
    Store a single web snippet into DB.
    """
    snippet = WebSnippet(
        url=url,
        title=title,
        content=chunk,
        embedding=embedding
    )
    db.add(snippet)
    db.commit()

def ingest_web_for_ticket(db: Session, ticket_text: str, max_links: int = 3):
    app_logger.info(f"Starting ingestion for ticket text: {ticket_text}")

    urls = get_search_results(ticket_text, max_links)
    app_logger.info(f"Found {len(urls)} URLs to scrape.")

    for url in urls:
        try:
            app_logger.info(f"Scraping URL: {url}")
            title, page_content = scrape_page(url)
            app_logger.info(f"Scraped {len(page_content)} characters from {url}")

            chunked_embeddings = chunk_and_embed(page_content)
            app_logger.info(f"Generated {len(chunked_embeddings)} chunks from {url}")

            for chunk, emb in chunked_embeddings:
                store_web_snippet(db, url, title, chunk, emb)
            app_logger.info(f"Stored {len(chunked_embeddings)} chunks for {url}")

        except Exception as e:
            app_logger.error(f"Error ingesting {url}: {e}")

    app_logger.info("Ingestion complete.")

