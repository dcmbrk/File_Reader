import ssl
import smtplib
import zipfile
import tempfile
from pathlib import Path
from email.message import EmailMessage

email_sender = "anhson2972005@gmail.com"
email_password = "mvlxryevppkbrdgr"
email_receiver = "kurinthefox@gmail.com"

pdf_folder_path = Path("files")
csv_folder_path = Path("csv")

try:
    pdf_files = list(pdf_folder_path.rglob("*.pdf"))
    pdf_count = len(pdf_files)
    pdf_list_str = "\n".join([f"- {p.name}" for p in pdf_files])
except FileNotFoundError:
    pdf_count = 0
    pdf_list_str = ""

csv_files = [p for p in csv_folder_path.rglob("*") if p.is_file()]

subject = f"Báo Cáo Tự Động: Đã xử lý {pdf_count} file PDF"

body = f"""
Tổng số lượng file PDF đã đọc: {pdf_count}
Danh sách file PDF đã xử lý:
{pdf_list_str}
"""

Path("csv.zip").unlink(missing_ok=True)

with tempfile.TemporaryDirectory() as tmpdir:
    zip_path = Path(tmpdir) / "csv.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in csv_files:
            zf.write(p, arcname=p.relative_to(csv_folder_path))

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    em.add_attachment(
        zip_path.read_bytes(),
        maintype="application",
        subtype="zip",
        filename="csv_data.zip",
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
