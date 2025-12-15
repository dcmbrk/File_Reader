import os
import re
import csv
import uuid
from pypdf import PdfReader
from sqlalchemy import select
from connection.db import Session
from connection.models import Rules, Data

class Reader():
    def __init__(self, path, type):        
        self.path = path
        self.type = type

    def extract_file(self):
        id = uuid.uuid4()

        name = os.path.basename(self.path)
        reader = PdfReader(self.path)
        text = reader.pages[0].extract_text()

        with Session() as session:
            with session.begin():
                q = select(Rules)   
                r = session.scalars(q).all()

                for rule in r:
                    if rule.type == self.type:

                        data = Data(
                            name = name,
                            rule_id = rule.id,
                            value = self.get_value(name, text, rule.regex)
                        )

                        self.export_csv_file(filename=id, json_data=data.value)

                        session.add(data)

                        break


    def extract_folder(self):
        id = uuid.uuid4()

        for file in os.listdir(self.path):
            if file.endswith('.pdf'):
                name = os.path.basename(self.path)
                file_path = os.path.join(self.path, file)
                reader = PdfReader(file_path)
                text = reader.pages[0].extract_text()

                with Session() as session:
                    with session.begin():

                        for rule in session.scalars(select(Rules)).all():
                            if rule.type == self.type:
                                
                                data = Data(
                                    name = name,
                                    rule_id = rule.id,
                                    value = self.get_value(text, rule.regex)
                                )

                                csv_data = self.create_csv_data(data.value, file)

                                self.export_csv_file(filename=id, json_data=csv_data)

                                session.add(data)
                                
                                break

    def create_csv_data(data, filename):
        data['name'] = filename
        return data 

    def get_value(self, filename, text, regex):
        res = {}
        res['name'] = filename
        for field, match in regex.items():
            res[field] = re.search(match, text).group()   
        return res
    
    def export_csv_file(self, filename, json_data):
        
        file_path = os.path.join("csv", f"{filename}.csv")
        is_new = not os.path.exists(file_path)
        with open(f"csv/{filename}.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=json_data.keys())
            if is_new:
                writer.writeheader()
            writer.writerow(json_data)
