import os
import wget
import json 

TARGET_FILE = 'papers_2025_04_15.json'

# Path to folder with your .json files
json_folder_path = "../../data/paper_db"
pdf_folder_path = "../../data/papers_pdf"


# Make sure the PDF folder exists
os.makedirs(pdf_folder_path, exist_ok=True)

file_links = []

if TARGET_FILE == 'all':
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith(".json")]
else:
    json_files = [TARGET_FILE] if os.path.exists(os.path.join(json_folder_path, TARGET_FILE)) else []

for filename in json_files:
    filepath = os.path.join(json_folder_path, filename)
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                file_links.extend(data)
            elif isinstance(data, dict):
                file_links.append(data)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        
def is_exist(file_links):
    return os.path.exists(f"../../data/papers_pdf/{file_links['title']}.pdf")

for file_link in file_links:
    if not is_exist(file_link):
        wget.download(file_link['arxiv_pdf'], f"../../data/papers_pdf/{file_link['title']}.pdf")
    else:
        print(f"File {file_link['title']}.pdf already exists.")