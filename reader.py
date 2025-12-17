import pymupdf4llm, pymupdf
import os
from ai import AI
from connection.db import Session
from connection.models import Document
from format import FORMAT

class Reader():
    def __init__(self, path):
        self.path = path
        self.ai = AI()

    def extract_file(self):
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
                    data=data.model_dump_json(indent=2))
                session.add(document)
                print(document.data)

    def extract_folder(self):
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
                            data=data.model_dump_json(indent=2))
                        session.add(document)
                        print(document.name)



# reader = Reader("files/1C25TMH47_2.pdf")
# reader.extract_file()

reader = Reader("files")
reader.extract_folder()