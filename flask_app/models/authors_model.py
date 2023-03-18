from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import books_model

class Author():
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors
    
    @classmethod
    def create_author(cls, data):
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        return connectToMySQL('books_schema').query_db(query, data)
    
    @classmethod
    def get_one_author(cls,data):
        query = "SELECT * FROM authors LEFT JOIN favorites on authors.id=favorites.author_id LEFT JOIN books on favorites.book_id = books.id where authors.id=(%(id)s);"
        results = connectToMySQL('books_schema').query_db(query,data)
        print(results)
        this_author = cls(results[0])
        authors_favorites = []
        for row in results:
            book_attributes = {
                'id':row['books.id'],
                'title':row['title'],
                'num_of_pages':row['num_of_pages'],
                'created_at':row['books.created_at'],
                'updated_at':row['books.updated_at']
            }
            authors_favorites.append(books_model.Book(book_attributes))
        this_author.favorites =  authors_favorites
        return this_author
    
    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)
