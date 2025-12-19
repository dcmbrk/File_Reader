import sys
from reader import Reader
from mailer import Mailer

def main():
    if len(sys.argv) == 3:
        reader = Reader(path=sys.argv[2])
        mailer = Mailer(path=sys.argv[2])

        if sys.argv[1] == '--file':
            print("EXTRACTING FILE....")
            reader.extract_file()
            print("DONE....")
            print("SENDING MAIL....")
            mailer.send_mail()
            print("DONE....")
            
        elif sys.argv[1] == '--folder':
            print("EXTRACTING FOLDER....")
            reader.extract_folder()
            print("DONE....")
            print("SENDING MAIL....")
            mailer.send_mail()
            print("DONE....")
            

if __name__ == "__main__":
    main()

