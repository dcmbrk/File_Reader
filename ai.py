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
            {"role": "system", "content": "Bạn là chuyên gia phân loại tài liệu văn phòng."},
            {"role": "user", "content": f"Phân loại văn bản sau: {text[:2000]}"}
        ],
        response_format=ClassificationType,
        )
        return completion.choices[0].message.parsed.selected_type.value

    def extract_data(self, text, format):
        completion = self.client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia bóc tách hóa đơn."},
            {"role": "user", "content": f"Trích xuất dữ liệu từ bảng sau sang JSON:\n{text}"}
        ],
        response_format=format,
        )
        return completion.choices[0].message.parsed

        



