# from sqlmodel import Session, select
# from db import engine
# from models import ParsedPage

# with Session(engine) as session:
#     results = session.exec(select(ParsedPage)).all()
#     print(f"{'ID':<3} | {'URL':<35} | Title")
#     print("-" * 90)
#     for r in results:
#         print(f"{r.id:<3} | {r.url:<35} | {r.title[:60]}")
from sqlmodel import Session, SQLModel, create_engine, select
from models import ParsedPage

DATABASE_URL = "postgresql://Taisia1@localhost:5432/parseddb"
engine = create_engine(DATABASE_URL)

def main():
    with Session(engine) as session:
        results = session.exec(select(ParsedPage)).all()
        for row in results:
            print(f"{row.id:<3} | {row.url:<35} | {row.title[:60]}")

if __name__ == "__main__":
    main()
