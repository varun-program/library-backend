from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

DATA_FILE = "books.json"


def read_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_books(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# GET ALL BOOKS
@router.get("/books")
def get_books():
    return read_books()


# ADD BOOK
@router.post("/add-book")
def add_book(book: dict):
    books = read_books()

    book["id"] = len(books) + 1
    book["available"] = True

    books.append(book)
    save_books(books)

    return {"message": "Book added", "book": book}


# BORROW BOOK
@router.post("/borrow/{book_id}")
def borrow_book(book_id: int):
    books = read_books()

    for book in books:
        if book["id"] == book_id:
            if not book["available"]:
                raise HTTPException(status_code=400, detail="Book already borrowed")

            book["available"] = False
            save_books(books)
            return {"message": "Book borrowed"}

    raise HTTPException(status_code=404, detail="Book not found")


# RETURN BOOK
@router.post("/return/{book_id}")
def return_book(book_id: int):
    books = read_books()

    for book in books:
        if book["id"] == book_id:
            book["available"] = True
            save_books(books)
            return {"message": "Book returned"}

    raise HTTPException(status_code=404, detail="Book not found")


# DELETE BOOK
@router.delete("/delete-book/{book_id}")
def delete_book(book_id: int):
    books = read_books()

    books = [book for book in books if book["id"] != book_id]

    save_books(books)

    return {"message": "Book deleted"}
