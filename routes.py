from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Book, BorrowHistory
from schemas import BookCreate

router = APIRouter()


# DATABASE DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ADD BOOK
@router.post("/add-book")
def add_book(book: BookCreate, db: Session = Depends(get_db)):

    new_book = Book(
        title=book.title,
        author=book.author,
        category=book.category,
        cover=book.cover
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "message": "Book Added",
        "book_id": new_book.id
    }


# GET ALL BOOKS
@router.get("/books")
def get_books(db: Session = Depends(get_db)):

    books = db.query(Book).all()

    return books


# BORROW BOOK
@router.post("/borrow/{book_id}")
def borrow_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.available:
        raise HTTPException(status_code=400, detail="Book already borrowed")

    book.available = False

    history = BorrowHistory(
        book_id=book.id,
        action="borrowed"
    )

    db.add(history)
    db.commit()

    return {"message": "Book borrowed successfully"}


# RETURN BOOK
@router.post("/return/{book_id}")
def return_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.available = True

    history = BorrowHistory(
        book_id=book.id,
        action="returned"
    )

    db.add(history)
    db.commit()

    return {"message": "Book returned successfully"}


# DELETE BOOK
@router.delete("/delete-book/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}


# BORROW HISTORY
@router.get("/history")
def get_history(db: Session = Depends(get_db)):

    history = db.query(BorrowHistory).all()

    return history