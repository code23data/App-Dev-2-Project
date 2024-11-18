from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.utils import decode_token
from werkzeug.security import generate_password_hash
from flask_restful import Resource
from flask_restful import reqparse, abort, request
from flask import jsonify
from application.database import db
from application.cache import cache
from application.models import (
    Books,
    Sections,
    User,
    SectionsBooks,
    Reviews,
)
from application.validation import (
    NotFoundError,
    BusinessValidationError,
    DuplicationError,
)
import datetime as dt
import time


parser = reqparse.RequestParser()


class BookListResource(Resource):
    @cache.memoize()
    def get(self):
        books = Books.query.all()
        return [book.to_dict() for book in books]


class ReviewListResource(Resource):
    @cache.memoize()
    def get(self):
        reviews = Reviews.query.all()
        return [review.to_dict() for review in reviews]


class SectionListResource(Resource):
    @cache.memoize()
    def get(self):
        sections = Sections.query.all()
        return [section.to_dict() for section in sections]


class UserListResource(Resource):

    @jwt_required()
    @cache.memoize()
    def get(self):
        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if decoded_token["isadmin"]:
            users = User.query.all()
            return [user.to_dict() for user in users]
        else:
            return {"error": "You are not authorized to access user details"}, 400


class BookResource(Resource):

    # Read
    @jwt_required()
    def get(self, book_id):
        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if book_id == None:
            return
        book = Books.query.get_or_404(
            book_id, description=f"Book with id {book_id} not found."
        )
        return book.to_dict()

    # Update
    @jwt_required()
    def put(self, book_id):

        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if decoded_token["isadmin"]:
            book = Books.query.filter_by(book_id=book_id).first()
            book_name = request.json.get("book_name")
            content = request.json.get("content")
            authors = request.json.get("authors")
            sections = request.json.get("sections", None)
            reviews = request.json.get("post", None)
            if book_name:
                book.book_name = book_name
            if content:
                book.content = content
            if authors:
                book.authors = authors
            if sections:
                for section_name in sections:
                    section = Sections.query.filter_by(
                        section_name=section_name
                    ).first()
                    if section is not None:
                        section_books = SectionsBooks.query.filter_by(
                            sections=section, books=book
                        ).first()
                        if not section_books:
                            section_books = SectionsBooks(sections=section, books=book)
                            db.session.add(section_books)
            db.session.commit()
            return {"message": "Book updated successfully"}, 200
        else:
            return {"message": "You are not authorized to perform this action"}, 400

    # Delete
    @jwt_required()
    def delete(self, book_id):
        verify_jwt_in_request()

        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if decoded_token["isadmin"]:
            book = Books.query.filter_by(book_id=book_id).first()

            if book:
                sectionsbooks = SectionsBooks.query.filter_by(
                    book_id=book.book_id
                ).all()
                if sectionsbooks:
                    for sectionbook in sectionsbooks:
                        db.session.delete(sectionbook)

                db.session.delete(book)
                db.session.commit()
                return {"message": "Book deleted successfully"}, 200
            else:
                return {"message": "Book not found"}, 404
        else:
            return {"message": "You are not authorized to perform this action"}, 400

    # Create
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if decoded_token["isadmin"]:
            data = request.get_json()
            name = data.get("book_name")
            content = data.get("content")
            authors = data.get("authors")
            sections = data.get("sections", None)
            reviews = data.get("post", None)

            if Books.query.filter_by(book_name=name).first():
                raise DuplicationError("The book already exists", 401)

            new_book = Books(book_name=name, content=content, authors=authors)

            if sections:
                for section_name in sections:
                    section = Sections.query.filter_by(
                        section_name=section_name
                    ).first()
                    if section is not None:
                        section_books = SectionsBooks(sections=section, books=new_book)
                        db.session.add(section_books)

            db.session.add(new_book)
            db.session.commit()
            return {"message": "Book added successfully"}, 200
        else:
            return {"message": "You are not authorized to perform this action"}, 400


class SectionResource(Resource):

    # Read
    @jwt_required()
    def get(self, section_id):
        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print(f"\n\n {decoded_token} \n\n")
        return Sections.query.get_or_404(
            section_id, description=f"Section with id {section_id} not found."
        ).to_dict()

    # Update
    @jwt_required()
    def put(self, section_id):
        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if decoded_token["isadmin"]:
            section = Sections.query.filter_by(section_id=section_id).first()
            name = request.json.get("name")
            date_created = time.time()
            description = request.json.get("description")
            if section:
                if name:
                    section.section_name = name
                if date_created:
                    section.date_created = date_created
                if description:
                    section.description = description
                db.session.commit()
                return {"message": "Section updated successfully"}, 200
            else:
                raise NotFoundError("Section with ID {section_id} not found.", 404)
        else:
            return {"message": "You are not authorized to perform this action"}, 400

    # Delete
    @jwt_required()
    def delete(self, section_id):
        verify_jwt_in_request()

        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if decoded_token["isadmin"]:
            section = Sections.query.filter_by(section_id=section_id).first()
            if section:
                # Delete the association between the section and its books
                SectionsBooks.query.filter_by(section_id=section_id).delete()
                # Delete the section
                db.session.delete(section)
                db.session.commit()
                return {"message": "Section deleted successfully"}, 200
            else:
                raise NotFoundError("Section with ID {section_id} not found.", 404)
        else:
            return {"message": "You are not authorized to perform this action"}, 400

    # Create
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)
        print("\n\n", decoded_token, "\n\n")

        if decoded_token["isadmin"]:
            data = request.get_json()
            name = data.get("name")
            date = time.time()
            description = data.get("description")

            # Check if a section with the given name already exists
            existing_section = Sections.query.filter_by(section_name=name).first()
            if existing_section is not None:
                return {"message": "A section with this name already exists"}, 400

            new_section = Sections(
                section_name=name, date_created=date, description=description
            )
            db.session.add(new_section)
            db.session.commit()
            return {"message": "Section added successfully"}, 200
        else:
            return {"message": "You are not authorized to perform this action"}, 400


class UserResource(Resource):

    # Read
    @jwt_required()
    def get(self, user_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(
            user_id, description=f"User with ID {user_id} not found."
        )
        return jsonify(user.to_dict())

    # Update
    @jwt_required()
    def put(self, user_id):
        admin = get_jwt_identity()

        token = request.headers.get("Authorization").split()[1]
        decoded_token = decode_token(token)

        user = User.query.get_or_404(user_id)
        name = request.json.get("username", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)

        if decoded_token["isadmin"]:
            if user:
                if name:
                    user.username = name
                if password:
                    user.password = generate_password_hash(
                        password, method="pbkdf2:sha256"
                    )
                if email:
                    user.email = email
                db.session.commit()
            else:
                raise NotFoundError(f"The user with ID {user_id} not found", 404)
        else:
            return {"error": "You are not authorized to perform this action"}, 400

    # Delete
    @jwt_required
    def delete(self, user_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return "Successfully deleted"


class ReviewResource(Resource):

    @jwt_required()
    def get(self, roll):
        review = Reviews.query.get(roll)
        if review:
            return jsonify(review.to_dict()), 200
        else:
            return jsonify({"error": "Review not found"}), 404

    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        data = request.get_json()
        book_id = data.get("book_id", None)
        post = data.get("post", None)
        rating = data.get("rating", None)
        if not post or not rating:
            return {"error": "Missing required fields"}, 400
        book = Books.query.get(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        if user != book.user_id:
            return {"error": "Not authorized to review this book"}, 401
        review = Reviews(user_id=user, post=post, rating=rating)
        book.reviews.append(review)
        db.session.add(review)
        db.session.commit()
        return {"message": "Review added successfully"}, 200

    @jwt_required()
    def put(self, roll):
        user = get_jwt_identity()
        data = request.get_json()
        review = Reviews.query.get(roll)
        post = data.get("post")
        rating = data.get("rating")
        if review and user == review.user_id:
            if post:
                review.post = post
            if rating:
                review.rating = rating
            db.session.commit()
            return {"message": "Review updated successfully"}, 200
        else:
            return {"error": "You are not authorised to edit the review"}

    @jwt_required()
    def delete(self, roll):
        user = get_jwt_identity()
        review = Reviews.query.get(roll)
        if review and user == review.user_id:
            db.session.delete(review)
            db.session.commit()
            return {"message": "Review deleted"}, 200
        else:
            return {"error": "Review not found or not authorized to delete"}, 404
