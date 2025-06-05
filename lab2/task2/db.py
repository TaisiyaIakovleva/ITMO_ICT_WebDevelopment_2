# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.future import select

# DATABASE_URL = "postgresql+asyncpg://Taisia1@localhost:5432/parseddb"

# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base = declarative_base()

# class ParsedPage(Base):
#     __tablename__ = "parsedpage"

#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String, nullable=False)
#     title = Column(String, nullable=False)

# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# async def save_parsed_page(url: str, title: str):
#     async with async_session() as session:
#         result = await session.execute(select(ParsedPage).where(ParsedPage.url == url))
#         existing = result.scalars().first()
#         if not existing:
#             page = ParsedPage(url=url, title=title)
#             session.add(page)
#             await session.commit()
#             print(f"[saved] {url}")
#         else:
#             print(f"[exists] {url}")

from sqlmodel import create_engine, SQLModel

DATABASE_URL = "postgresql://Taisia1@localhost:5432/parseddb"
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
