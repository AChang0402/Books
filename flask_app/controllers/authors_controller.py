from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.authors_model import Author
from flask_app.models.books_model import Book

@app.route('/authors')
def authors():
    authors = Author.get_all_authors()
    return render_template("authors.html", authors=authors)

@app.route('/authors/create', methods=['post'])
def add_author():
    new_author_id = Author.create_author(request.form)
    return redirect('/authors')

@app.route('/authors/<int:id>')
def show_author(id):
    author = Author.get_one_author({'id':id})
    books = Book.get_all_books()
    return render_template('authors_show.html', author=author, books=books)

@app.route('/authors/<int:id>/addfavorite', methods=['post'])
def add_favorite(id):
    print(request.form)
    data = {
        'author_id':id,
        'book_id': request.form['book_id']
    }
    new_favorite_id = Author.add_favorite(data)
    return redirect('/authors/'+str(id))