import requests
from io import BytesIO
from PyPDF2 import PdfReader
from transformers import pipeline

def summarize_pdf(url: str) -> str:
    """
    Download a PDF from the given URL, extract the text, and summarize it.
    
    Parameters:
        url (str): The URL to the PDF file.
    
    Returns:
        A summary string (approximately one paragraph long).
    """
    try:
        # Download the PDF content
        response = requests.get(url)
        response.raise_for_status()
        
        # Read the PDF content from bytes
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        
        # Extract text from each page of the PDF
        extracted_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
        
        if not extracted_text.strip():
            return "No text could be extracted from the PDF."
        
        # Initialize the summarization pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # The summarizer may require the text to be below a certain token limit.
        # If the text is very long, you might want to truncate or split it.
        # Here, we'll just summarize the first 1000 words as an example.
        words = extracted_text.split()
        truncated_text = " ".join(words[:1000])
        
        # Generate a summary. You can tweak max_length and min_length to control output.
        summary = summarizer(truncated_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    
    except Exception as e:
        return f"An error occurred: {e}"

# Example use
if __name__ == "__main__":
    pdf_url = "https://arxiv.org/pdf/2504.07491"
    summary = summarize_pdf(pdf_url)
    print("PDF Summary:\n", summary)
