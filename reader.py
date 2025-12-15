import os
import re
from pypdf import PdfReader
from sqlalchemy import select
from connection.db import Session
from connection.models import Rules, Data

class Reader():
    def __init__(self, path, type):        
        self.path = path
        self.type = type


    def extract_file(self):
        reader = PdfReader(self.path)
        text = reader.pages[0].extract_text()

        with Session() as session:
            with session.begin():
                q = select(Rules)   
                r = session.scalars(q).all()

                for rule in r:
                    if rule.type == self.type:

                        data = Data(
                            name = os.path.basename(self.path),
                            rule_id = rule.id,
                            value = self.get_value(text, rule.regex)
                        )

                        session.add(data)

                        break


    def extract_folder(self):
        for file in os.listdir(self.path):
            if file.endswith('.pdf'):
                
                file_path = os.path.join(self.path, file)
                reader = PdfReader(file_path)
                text = reader.pages[0].extract_text()

                with Session() as session:
                    with session.begin():

                        for rule in session.scalars(select(Rules)).all():
                            if rule.type == self.type:
                                
                                data = Data(
                                    name = os.path.basename(file_path),
                                    rule_id = rule.id,
                                    value = self.get_value(text, rule.regex)
                                )

                                session.add(data)
                                
                                break

    def get_value(self, text, regex):
        res = {}
        for field, match in regex.items():
            res[field] = re.search(match, text).group()   
        return res

