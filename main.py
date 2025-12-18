import sys
from reader import Reader

def main():
    if len(sys.argv) == 3:
        reader = Reader(path=sys.argv[2])

        if sys.argv[1] == '--file':
            print("EXTRACTING FILE....")
            reader.extract_file()
            print("DONE....")
            
        elif sys.argv[1] == '--folder':
            print("EXTRACTING FOLDER....")
            reader.extract_folder()
            print("DONE....")
    else:
        print('Nhap sai')

if __name__ == "__main__":
    main()

