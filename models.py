from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    author = Column(String(255))
    category = Column(String(255))
    cover = Column(String(500))
    available = Column(Boolean, default=True)
    
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    cover = Column(String)
    available = Column(Boolean, default=True)


class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    action = Column(String)
