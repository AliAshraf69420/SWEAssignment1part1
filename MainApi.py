from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

books = []

@app.route('/')
def home():
    return 'Welcome to the Bookstore!'
@app.route('/bookswithcriteria', methods=['GET'])
def get_books_with_criteria():
    """
    Get all books or filter books by author, published year, or genre
    ---
    parameters:
      - in: query
        name: author
        type: string
        required: false
      - in: query
        name: published_year
        type: integer
        required: false
      - in: query
        name: genre
        type: string
        required: false
    responses:
      200:
        description: A list of books
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
              author:
                type: string
              published_year:
                type: integer
              isbn:
                type: string
              genre:
                type: string
    """
    author = request.args.get('author')
    published_year = request.args.get('published_year')
    genre = request.args.get('genre')

    filtered_books = books
    if author:
        filtered_books = [book for book in filtered_books if book['author'] == author]
    if published_year:
        filtered_books = [book for book in filtered_books if book['published_year'] == int(published_year)]
    if genre:
        filtered_books = [book for book in filtered_books if book['genre'] == genre]

    return jsonify(filtered_books)
@app.route('/books', methods=['GET'])
def get_all_books():
    """
    Get all books
    ---
    responses:
      200:
        description: A list of books
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
    """
    return jsonify(books)
@app.route('/books', methods=['POST'])
def create_book():
    """
    Create a new book
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
            - author
            - published_year
            - isbn
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            isbn:
              type: string
            genre:
              type: string
    responses:
      201:
        description: The created book
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            isbn:
              type: string
            genre:
              type: string
    """
    new_book = request.json
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<string:isbn>', methods=['GET'])
def get_book(isbn):
    """
    Get a book by ISBN
    ---
    parameters:
      - in: path
        name: isbn
        type: string
        required: true
    responses:
      200:
        description: The requested book
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            isbn:
              type: string
            genre:
              type: string
      404:
        description: Book not found
    """
    book = next((book for book in books if book['isbn'] == isbn), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book)

@app.route('/books/<string:isbn>', methods=['PUT'])
def update_book(isbn):
    """
    Update a book by ISBN
    ---
    parameters:
      - in: path
        name: isbn
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            genre:
              type: string
    responses:
      200:
        description: The updated book
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            published_year:
              type: integer
            isbn:
              type: string
            genre:
              type: string
      404:
        description: Book not found
    """
    book = next((book for book in books if book['isbn'] == isbn), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    updated_data = request.json
    book.update(updated_data)
    return jsonify(book)

@app.route('/books/<string:isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Delete a book by ISBN
    ---
    parameters:
      - in: path
        name: isbn
        type: string
        required: true
    responses:
      204:
        description: Book deleted
      404:
        description: Book not found
    """
    global books
    books = [book for book in books if book['isbn'] != isbn]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)