# PDF READER
### Cài đặt thư viện
`pip install -r requirements.txt`
### Cài đặt pgadmin, postgrest (nếu cần)
`docker-compose up -d`
### Cài đặt kết nối databasae (SQLAlchemy) trong .env
`DATABASE_URL='postgresql+psycopg2://Username:Password@localhost:5432/database'`
## Trích xuất thông tin từ file
`python main.py -file <file-path> <file-type>`
## Trích xuất thông tin từ folder
`python main.py -folder <folder-path> <file-type>`
