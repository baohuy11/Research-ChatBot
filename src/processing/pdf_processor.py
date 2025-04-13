from PyPDF2 import PdfReader
from io import BytesIO
import requests

def summarize_pdf(url: str, summarizer) -> str:
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
        
    words = extracted_text.split()
    truncated_text = " ".join(words[:1000])
        
    # Generate a summary. You can tweak max_length and min_length to control output.
    summary = summarizer(truncated_text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']