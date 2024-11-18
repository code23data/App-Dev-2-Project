from sqlalchemy import ForeignKey
from .database import db


class Books(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    date_issued = db.Column(db.Float, nullable=True, default=None)
    date_returned = db.Column(db.Float, nullable=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    sections = db.relationship("SectionsBooks", back_populates="books")
    reviews = db.relationship("Reviews", backref="books")

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "book_name": self.book_name,
            "content": self.content,
            "authors": self.authors,
            "date_issued": self.date_issued,
            "date_returned": self.date_returned,
            "user_id": self.user_id,
            "sections": [section.to_dict() for section in self.sections],
            "reviews": [review.to_dict() for review in self.reviews],
        }


class Sections(db.Model):
    __tablename__ = "sections"
    section_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    section_name = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    sections_books = db.relationship("SectionsBooks", back_populates="sections")

    def to_dict(self):
        return {
            "section_id": self.section_id,
            "section_name": self.section_name,
            "date_created": self.date_created,
            "description": self.description,
            "books": [book.to_dict() for book in self.sections_books],
        }


# Many-to-Many relationship between Books and Sections
class SectionsBooks(db.Model):
    __tablename__ = "sections_books"
    section_id = db.Column(
        db.Integer, db.ForeignKey("sections.section_id"), primary_key=True
    )
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), primary_key=True)
    sections = db.relationship("Sections", back_populates="sections_books")
    books = db.relationship("Books", back_populates="sections")

    def to_dict(self):
        return {
            "section_id": self.section_id,
            "book_id": self.book_id,
            "book_name": self.books.book_name,
            "authors": self.books.authors,
            "section_name": self.sections.section_name,
        }


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    isadmin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String, unique=True, nullable=False)
    issued_books = db.relationship("Books", backref="user", lazy=True)
    lastseen = db.Column(db.Float)

    def can_issue_book(self):
        print(len(self.issued_books))
        return len(self.issued_books) <= 5 or self.isadmin

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            # "password": self.password,
            "is_admin": self.isadmin,
            "email": self.email,
            "issued_books": [book.to_dict() for book in self.issued_books],
            "lastseen": self.lastseen,
        }


class Reviews(db.Model):
    __tablename__ = "reviews"
    roll = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey("user.user_id"), nullable=True)
    post = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))

    def to_dict(self):
        return {
            "roll": self.roll,
            "user_id": self.user_id,
            "post": self.post,
            "rating": self.rating,
            "book_id": self.book_id,
        }
