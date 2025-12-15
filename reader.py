import os
import re
import csv  # [Thêm] Thư viện CSV
from pypdf import PdfReader
from sqlalchemy import select
from connection.db import Session
from connection.models import Rules, Data


class Reader:
    def __init__(self, path, type):
        self.path = path
        self.type = type

    # [Thêm] Hàm ghi file CSV
    def save_csv(self, data):
        os.makedirs("csv", exist_ok=True)  # Tạo folder nếu chưa có
        file_path = os.path.join("csv", f"{self.type}.csv")
        is_new = not os.path.exists(file_path)

        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if is_new:
                writer.writeheader()
            writer.writerow(data)

    def extract_file(self):
        reader = PdfReader(self.path)
        text = reader.pages[0].extract_text()

        with Session() as session:
            with session.begin():
                q = select(Rules)
                r = session.scalars(q).all()

                for rule in r:
                    if rule.type == self.type:
                        vals = self.get_value(text, rule.regex)  # Lấy dữ liệu
                        self.save_csv(vals)  # [Thêm] Lưu ra CSV

                        data = Data(
                            name=os.path.basename(self.path),
                            rule_id=rule.id,
                            value=vals,
                        )

                        session.add(data)
                        break

    def extract_folder(self):
        for file in os.listdir(self.path):
            if file.endswith(".pdf"):
                file_path = os.path.join(self.path, file)

                reader = PdfReader(file_path)
                text = reader.pages[0].extract_text()

                with Session() as session:
                    with session.begin():

                        for rule in session.scalars(select(Rules)).all():
                            if rule.type == self.type:
                                vals = self.get_value(text, rule.regex)  # Lấy dữ liệu
                                self.save_csv(vals)  # [Thêm] Lưu ra CSV

                                data = Data(
                                    name=os.path.basename(file_path),
                                    rule_id=rule.id,
                                    value=vals,
                                )

                                session.add(data)
                                break

    def get_value(self, text, regex):
        res = {}
        for field, match in regex.items():
            try:
                res[field] = re.search(match, text).group()
            except AttributeError:
                res[field] = ""
        return res
