import json
from connection.db import Model, Session, engine
from connection.models import Rules

def main():
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open('data/rules.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                data = [data]

                for item in data:
                    rule = Rules(**item) 
                    session.add(rule)

if __name__ == "__main__":
    main()
