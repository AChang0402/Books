from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.authors_model import Author
from flask_app.models.books_model import Book

@app.route('/books')
def book():
    books = Book.get_all_books()
    return render_template('books.html', books=books)

@app.route('/books/create', methods=['post'])
def newbook():
    new_book_id = Book.create_book(request.form)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):
    book = Book.get_one_book({'id':id})
    authors = Author.get_all_authors()
    print(book)
    return render_template('books_show.html', book=book, authors=authors)

@app.route('/books/<int:id>/addfavorite', methods=['post'])
def add_favorite_book(id):
    data = {
        'book_id':id,
        'author_id': request.form['author_id']
    }
    new_favorite_id = Author.add_favorite(data)
    return redirect('/books/'+str(id))