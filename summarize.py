import pdfplumber
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def reformat_chatgpt_response(response):
    # Split the response into paragraphs based on double newline characters
    paragraphs = response.strip().split('\n\n')

    formatted_text = ""

    for para in paragraphs:
        # Check if the paragraph starts with a bullet point (assuming '- ' as the marker)
        if para.startswith('- '):
            # Split the bullet points
            bullet_points = para.split('\n')
            formatted_text += "<ul>"
            for bullet in bullet_points:
                formatted_text += f"<li>{bullet.strip('- ')}</li>"
            formatted_text += "</ul>"
        else:
            # Otherwise, treat it as a regular paragraph
            formatted_text += f"<p>{para}</p>"

    return formatted_text

def summarize_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the latest chat model you have access to
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            #{"role": "user", "content": f"List solar regulations in the following text in bullet points: {text}."}
            {"role": "user", "content": f"Extract the paragraphs relating to solar development: {text}."}
        ]
    )

    summary = response.choices[0].message.content

    print(summary)

    # formatted_response = reformat_chatgpt_response(summary)

    return summary

if __name__ == '__main__':
    # For testing purposes
    pdf_file = 'path_to_your_pdf_file.pdf'
    print(summarize_pdf(pdf_file))