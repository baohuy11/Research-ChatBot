from scraper import get_today_papers
from local_model import summarize_text

def main():
    # Step 1: Retrieve today's papers from Hugging Face
    papers = get_today_papers()
    if not papers:
        print("No papers found for today.")
        return

    # Step 2: For each paper, create a summary.
    for paper in papers:
        # Use paper details as input to summarizer (you might combine title and description)
        text_to_summarize = f"Title: {paper['title']}\nDetails: {paper['summary_source']}"
        summary = summarize_text(text_to_summarize)
        print(f"Paper Title: {paper['title']}")
        print(f"Summary: {summary}")
        print("-" * 80)

if __name__ == "__main__":
    main()
