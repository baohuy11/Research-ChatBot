from transformers import pipeline

# Load a summarization pipeline (you can customize the model as needed)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    # You may need to fine tune settings such as max_length or min_length.
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    sample_text = (
        "This paper explores the empirical capabilities of GPT-4o in generating images..."
        "It presents a thorough evaluation of image quality, prompting, and benchmark comparisons."
    )
    print(summarize_text(sample_text))
