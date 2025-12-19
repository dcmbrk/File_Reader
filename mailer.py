import ssl
import smtplib
import zipfile
import tempfile
from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

class Mailer():
    def __init__(self,
                email_sender = os.environ['EMAIL_SENDER'],
                email_password = os.environ['EMAIL_PASSWORD'],
                email_receiver = os.environ['EMAIL_RECEIVER'],
                filename = "csv_data.zip",
                path = "files"
                 ):
        self.email_sender = email_sender
        self.email_password = email_password
        self.email_receiver = email_receiver
        self.pdf_folder_path = Path(os.environ['PDF_FOLDER'])
        self.csv_folder_path = Path(os.environ['CSV_FOLDER'])
        self.zip_file = Path(os.environ['ZIP_FILE'])
        self.zip_file.unlink(missing_ok=True)
        self.filename = filename
        self.path = path

    def send_mail(self)-> None:
        em = self.create_email_message()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.send_message(em)

        for file in self.csv_folder_path.glob('*'):
            if file.is_file():
                file.unlink()

    def create_email_message(self) -> EmailMessage:
        subject, body = self.create_mail_content()
        zip_byze = self.create_zip_file()

        em = EmailMessage()
        em["From"] = self.email_sender
        em["To"] = self.email_receiver
        em["Subject"] = subject
        em.set_content(body)
        em.add_attachment(
            zip_byze,
            maintype="application",
            subtype="zip",
            filename= self.filename,
        )
        return em

    def create_zip_file(self) -> bytes:
        csv_files = [p for p in self.csv_folder_path.rglob("*") if p.is_file()]
        with tempfile.TemporaryDirectory() as td:
            zip_path = Path(td) / self.zip_file
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for p in csv_files:
                    zf.write(p, arcname=p.relative_to(self.csv_folder_path))
            return zip_path.read_bytes()

    def create_mail_content(self) -> tuple[str, str]:
        if self.path.endswith(".pdf"):
            body = f"Files: {self.path}"
        else:
            pdf_files = os.listdir(self.pdf_folder_path)
            file_list_str = "\n".join([f"- {file}" for file in pdf_files])
            body = f"Files: ({len(pdf_files)}):\n{file_list_str}"

        subject = f"File Reader"
        
        return subject, body


mailer = Mailer()
mailer.send_mail()