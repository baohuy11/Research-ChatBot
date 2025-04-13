import re
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from pdf_processor import summarize_pdf
from config.config import settings 
from core.model import summarizer_model

HUGGINGFACE_PAPERS_URL = settings.HUGGINGFACE_PAPERS_URL
PAPER_DATE = settings.PAPER_DATE
DATE = settings.DATE

def extract_link(url: str) -> str:
    links = {
        "arxiv_page": "",
        "arxiv_pdf": "",
        "project_page": "",
        "github_page": "",
        "summary": "",
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

def parse_papers(url: str, date: str) -> list[dict]:
    full_url = f"{url}{date}"
    response = requests.get(full_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
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

def save_data_locally(data, filename, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    file_path = os.path.join(directory, filename)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f'Data saved to {file_path}')

def main():
    today_papers = parse_papers(HUGGINGFACE_PAPERS_URL, PAPER_DATE)
    summarizer = summarizer_model()
    if not today_papers:
        print("No papers found for today.")
        return
        
    print(len(today_papers))

    for paper in today_papers:
        if not paper['arxiv_pdf']:
            print(f"No PDF link found for {paper['title']}")
            continue

        paper['summary'] = summarize_pdf(paper['arxiv_pdf'], summarizer)
            
    filename = f"papers_{DATE}.json"
    save_data_locally(today_papers, filename, settings.DB_PATH)

if __name__ == "__main__":
    main()