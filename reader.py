import uuid
import pymupdf4llm, pymupdf
import os
from ai import AI
from connection.db import Session
from connection.models import Document
from format import FORMAT
import pandas as pd

class Reader():
    def __init__(self, path):
        self.path = path
        self.ai = AI()

    def extract_file(self):
        id = uuid.uuid4()
        doc = pymupdf.open(self.path)
        md = pymupdf4llm.to_markdown(doc)
        type = self.ai.classify_doc(md)
        data = self.ai.extract_data(md, FORMAT[type])

        with Session() as session:
            with session.begin():
                document = Document(
                    name=os.path.basename(self.path), 
                    type=type, 
                    text=md, 
                    data=data.model_dump())
                session.add(document)
                print(document.data)
                self.export_csv_file(id, document)

    def extract_folder(self):
        id = uuid.uuid4()
        for file in os.listdir(self.path):
            if file.endswith('.pdf'):
                file_name = os.path.basename(file)
                file_path = os.path.join(self.path, file)
                doc = pymupdf.open(file_path)
                md = pymupdf4llm.to_markdown(doc)
                type = self.ai.classify_doc(md)
                data = self.ai.extract_data(md, FORMAT[type])

                with Session() as session:
                    with session.begin():
                        document = Document(
                            name=file_name, 
                            type=type, 
                            text=md, 
                            data=data.model_dump())
                        session.add(document)
                        print(document.name)
                        self.export_csv_file(id, document.data)


    def export_csv_file(self, filename, document):
        os.makedirs("csv", exist_ok=True)
        file_path = os.path.join("csv", f"{filename}.csv")
        
        base_info = {
            "file_name": document.name,
            "doc_type": document.type
        }
        
        detail_df = pd.json_normalize(document.data)
        detail_dict = detail_df.to_dict(orient='records')[0]
        
        combined_data = {**base_info, **detail_dict}
        
        df = pd.DataFrame([combined_data])

        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
        else:
            df.to_csv(file_path, mode='a', index=False, header=False, encoding="utf-8-sig")


# reader = Reader("files/1C25TMH47_2.pdf")
# reader.extract_file()

# reader = Reader("files")
# reader.extract_folder()