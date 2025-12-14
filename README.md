# PDF READER
### Cai dat thu vien:
`pip install -r requirements.txt`
### Cai dat pgadmin, postgrest (neu can)
`docker-compose up -d`
### Cai dat ket noi database (SQLAlchemy) trong .env
`DATABASE_URL='postgresql+psycopg2://Username:Password@localhost:5432/database'`
## Trich xuat thong tin tu file
`python main.py -file <file-path> <file-type>`
## Trich xuat thong tin tu folder
`python main.py -folder <folder-path> <file-type>`
