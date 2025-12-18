from openai import OpenAI
from dotenv import load_dotenv
import os
from schema.classification_type import ClassificationType
load_dotenv()

class AI():
    def __init__(self):
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY']) 

    def classify_doc(self, text):    
        completion = self.client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are an expert in office document classification. "
                        "Analyze the provided text and categorize it into the most appropriate type "
                        "based on the predefined schema."
                    )
                },
                {"role": "user", "content": f"Document content to classify:\n{text[:3000]}"}
            ],
        response_format=ClassificationType,
        )
        return completion.choices[0].message.parsed.selected_type.value

    def extract_data(self, text, format):
        completion = self.client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a specialized data extraction assistant. Your task is to extract "
                        "information from invoice or receipt text into a structured JSON format. "
                        "Guidelines:\n"
                        "1. Maintain high precision for dates, amounts, and tax IDs.\n"
                        "2. If a field is missing, return null.\n"
                        "3. Handle OCR noise or misaligned table columns gracefully."
                    )
                },
                {"role": "user", "content": f"Extract data from the following text:\n{text}"}
            ],
        response_format=format,
        )
        return completion.choices[0].message.parsed

        



