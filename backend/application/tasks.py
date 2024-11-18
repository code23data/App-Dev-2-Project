import time
from application.workers import celery
from application.models import User, Books, SectionsBooks, Sections
from flask import current_app as app
from celery.schedules import crontab
from .mail import send_message
from jinja2 import Template
import csv
from .database import db
from weasyprint import HTML


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(20.0, send_monthly_reminder.s(), name="add every 20")
    sender.add_periodic_task(5.0, send_daily_reminder.s(), name="add every 5")
    sender.add_periodic_task(
        crontab(hour=0, minute=0),  # Execute daily at midnight
        check_and_return_books.s(),
    )


@celery.task
def check_and_return_books():
    with app.app_context():
        books = Books.query.filter(
            Books.date_issued.isnot(None), Books.date_returned.is_(None)
        ).all()
        for book in books:
            if time.time() - book.date_issued >= 7 * 24 * 60 * 60:  # 7 days
                book.date_returned = time.time()
                db.session.commit()


@celery.task()
def send_daily_reminder():
    now = time.time()
    threshold = now - 10
    print(threshold)

    inactive_users = User.query.filter(User.lastseen < threshold).all()

    template_file = "templates/daily_reminder.html"
    for inactive_user in inactive_users:
        if inactive_user.isadmin != True and inactive_user.username != "[deleted]":
            with open(template_file) as file:
                template = Template(file.read())
                message = template.render(user=inactive_user)
            send_message(
                to=inactive_user.email,
                subject="Daily Report",
                content_body=message,
            )
    return len(inactive_users)


def create_pdf_report(user, template, books, sections):
    with open(template) as f:
        template_file = Template(f.read())
        message = template_file.render(user=user, books=books, sections=sections)
        html = HTML(string=message)
        file_name = f"Reports/{str(user.username)}.pdf"
        print(file_name)
        html.write_pdf(target=file_name)


def generate_monthly_reminder(user_id):
    books = Books.query.filter_by(user_id=user_id).all()
    book_count = {}
    section_count = {}
    for book in books:
        if book.book_name not in book_count:
            book_count[book.book_name] = 1
        else:
            book_count[book.book_name] += 1
        for section_book in book.sections:
            section_name = section_book.sections.section_name
            if section_name not in section_count:
                section_count[section_name] = 1
            else:
                section_count[section_name] += 1
    return book_count, section_count


@celery.task()
def send_monthly_reminder():
    users = User.query.all()

    for user in users:
        if user.isadmin != True and user.username != "[deleted]":
            books, sections = generate_monthly_reminder(user.user_id)
            template_file = "templates/monthly_reminder.html"
            with open(template_file) as file:
                template = Template(file.read())
                message = template.render(user=user, books=books, sections=sections)
            create_pdf_report(user, template_file, books, sections)
            file_name = f"Reports/{str(user.username)}.pdf"
            print(file_name)
            send_message(
                to=user.email,
                subject="Monthly Report",
                content_body=message,
                attach_file=file_name,
            )
    return len(users)
