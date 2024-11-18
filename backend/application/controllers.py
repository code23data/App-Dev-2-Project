from flask import render_template, jsonify, request
from flask import current_app as app
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Books, Sections, User
from application.database import db
import time


@app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
def home(path):
    return render_template("index.html")


@app.route("/books/search=<string:term>")
def search(term):
    books = Books.query.filter(Books.book_name.like(f"%{term}%")).all()
    return [book.to_dict() for book in books]


@app.route("/sections/search=<string:term>")
def search_sections(term):
    sections = Sections.query.filter(Sections.section_name.like(f"%{term}%")).all()
    return [section.to_dict() for section in sections]


@app.route("/issue_book/<int:book_id>", methods=["POST"])
@jwt_required()
def issue_book(book_id):
    user = User.query.get_or_404(get_jwt_identity())
    book = Books.query.get_or_404(int(book_id))

    if book.user_id is not None:
        return (
            jsonify(
                {
                    "error": "User cannot issue book as it is issued by someone else currently."
                }
            ),
            400,
        )

    user.issued_books.append(book)
    book.date_issued = time.time()
    book.date_returned = None

    print(user.can_issue_book())

    if not user.can_issue_book():
        return jsonify({"error": "User cannot issue more than 5 books at a time."}), 400

    db.session.commit()

    return jsonify({"message": "Book issued successfully."}), 200


@app.route("/return_book/<int:book_id>", methods=["GET", "POST"])
@jwt_required()
def return_book(book_id):
    user = User.query.get_or_404(get_jwt_identity())
    book = Books.query.get_or_404(book_id)

    if book in user.issued_books:
        user.issued_books.remove(book)
        book.date_returned = time.time()
        db.session.commit()
        return jsonify({"message": "Book returned successfully"}), 200
    else:
        return jsonify({"error": "The book is not issued by the user"}), 400
