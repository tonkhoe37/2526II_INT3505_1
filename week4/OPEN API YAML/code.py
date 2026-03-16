from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

template = {
    "swagger": "2.0",
    "info": {
        "title": "Book Management API",
        "description": "API dùng để quản lý sách (CRUD, tìm kiếm, cập nhật...)",
        "version": "1.0.0",
    },
    "basePath": "/",
}

swagger = Swagger(app, template=template)

# Fake database
books = [
    {"id": "1", "title": "Clean Code", "author": "Robert C. Martin", "price": 30},
    {"id": "2", "title": "Atomic Habits", "author": "James Clear", "price": 25},
]


# GET ALL BOOKS
@app.route("/api/books", methods=["GET"])
def get_books():
    """
    Get all books
    ---
    tags:
        - Books
    responses:
      200:
        description: List of books
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              title:
                type: string
              author:
                type: string
              price:
                type: number
    """
    return jsonify(books)


# GET BOOK BY ID
@app.route("/api/books/<id>", methods=["GET"])
def get_book(id):
    """
    Get book by ID
    ---
    tags:
        - Books
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Book found
        schema:
          type: object
          properties:
            id:
              type: string
            title:
              type: string
            author:
              type: string
            price:
              type: number
      404:
        description: Book not found
    """
    for b in books:
        if b["id"] == id:
            return jsonify(b)
    return jsonify({"error": "Book not found"}), 404


# CREATE BOOK
@app.route("/api/books", methods=["POST"])
def create_book():
    """
    Create a new book
    ---
    tags:
        - Books
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - id
            - title
            - author
            - price
          properties:
            id:
              type: string
            title:
              type: string
            author:
              type: string
            price:
              type: number
    responses:
      201:
        description: Book created
    """
    data = request.json
    books.append(data)
    return jsonify(data), 201


# UPDATE BOOK
@app.route("/api/books/<id>", methods=["PUT"])
def update_book(id):
    """
    Update a book
    ---
    tags:
        - Books
    parameters:
      - name: id
        in: path
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            price:
              type: number
    responses:
      200:
        description: Book updated
      404:
        description: Book not found
    """
    for b in books:
        if b["id"] == id:
            data = request.json
            b.update(data)
            return jsonify(b)
    return jsonify({"error": "Book not found"}), 404


# DELETE BOOK
@app.route("/api/books/<id>", methods=["DELETE"])
def delete_book(id):
    """
    Delete a book
    ---
    tags:
        - Books
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Book deleted
    """
    global books
    books = [b for b in books if b["id"] != id]
    return jsonify({"message": "Book deleted"})


if __name__ == "__main__":
    port = 5000
    print(f"Server running at http://localhost:{port}")
    app.run(port=port)
