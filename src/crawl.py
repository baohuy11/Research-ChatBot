import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from config import HUGGINGFACE_PAPERS_URL, PDF_URL, PAPER_DATE, DATE

def fetch_page(url: str, date: str) -> str:
    full_url = f"{url}{date}"
    response = requests.get(full_url)
    response.raise_for_status()
    return response.text

def extract_link(url: str) -> str:
    links = {
        "arxiv_page": "",
        "arxiv_pdf": "",
        "project_page": "",
        "github_page": ""
    }
    
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
        
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(url, href)
        if re.search(r'arxiv\.org/abs/\d+\.\d+', href):
            links["arxiv_page"] = full_url
            arxiv_id = href.split("/")[-1]
            links["arxiv_pdf"] = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        elif 'github.com' in href:
            links["github_page"] = full_url
        elif 'Project page' in a.get_text(strip=True):
            links["project_page"] = full_url
        
    return links

def parse_papers(url: str, html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    papers = []
    entries = soup.find_all("article", class_="relative flex flex-col overflow-hidden rounded-xl border")
    for entry in entries:
        info = entry.find("a", class_="line-clamp-3 cursor-pointer text-balance")
        
        paper_href = info.get("href")
        title = info.get_text(strip=True)
        paper_url = urljoin(url, paper_href)
        
        additional_links = extract_link(paper_url)
        
        paper_info = {
            "title": title,
            "huggingface_url": paper_url,
            **additional_links
        }
        
        papers.append(paper_info)
        
    return papers

# def parse_papers(html: str) -> list[dict]:
#     soup = BeautifulSoup(html, "html.parser")
#     papers = []
#     entries = soup.find_all("article", class_="relative flex flex-col overflow-hidden rounded-xl border")
#     for entry in entries:
#         info = entry.find("a", class_="line-clamp-3 cursor-pointer text-balance")
        
#         paper_href = info.get("href")
#         paper_code = paper_href.split("/")[-1]
        
#         title = info.get_text(strip=True)
#         pdf_url = f"{PDF_URL}{paper_code}"
        
#         papers.append({
#             "huggingface_url": f"{HUGGINGFACE_PAPERS_URL}{paper_href}",
#             "title": title,
#             "pdf_url": pdf_url
#         })
#     return papers

def get_today_papers(url: str, date: str) -> list[dict]:
    html = fetch_page(url, date)
    papers = parse_papers(HUGGINGFACE_PAPERS_URL, html)
    return papers

def main():
    try:
        today_papers = get_today_papers(HUGGINGFACE_PAPERS_URL, PAPER_DATE)
        if not today_papers:
            print("No papers found for today.")
            return
        
        print(len(today_papers))

        for paper in today_papers:
            print(f"Title: {paper['title']}")
            print(f"HuggingFace URL: {paper['huggingface_url']}")
            print(f"arXiv Page: {paper.get('arxiv_page', 'Not found')}")
            print(f"arXiv PDF: {paper.get('arxiv_pdf', 'Not found')}")
            print(f"Project Page: {paper.get('project_page', 'Not found')}")
            print(f"GitHub Page: {paper.get('github_page', 'Not found')}")
            print("-" * 80)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()