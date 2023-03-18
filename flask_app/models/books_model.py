from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import authors_model

class Book():
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for row in results:
            books.append(cls(row))
        return books
    
    @classmethod
    def create_book(cls, data):
        query = "INSERT INTO books (title,num_of_pages) VALUES (%(title)s, %(num_of_pages)s)"
        return connectToMySQL('books_schema').query_db(query, data)
    
    @classmethod
    def get_one_book(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites on books.id=favorites.book_id LEFT JOIN authors on favorites.author_id = authors.id where books.id=(%(id)s);"
        results = connectToMySQL('books_schema').query_db(query,data)
        this_book = cls(results[0])
        favorited_by = []
        for row in results:
            author_attributes = {
                'id':row['authors.id'],
                'name':row['name'],
                'created_at':row['authors.created_at'],
                'updated_at':row['authors.updated_at']
            }
            favorited_by.append(authors_model.Author(author_attributes))
        this_book.favorited_by = favorited_by
        print(favorited_by)
        return this_book