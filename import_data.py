from connection.db import Model, engine
from connection import models 

def main():
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

if __name__ == "__main__":
    main()