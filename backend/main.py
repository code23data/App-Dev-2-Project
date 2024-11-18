import os
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from application import workers
from flask_cors import CORS
from application import workers

app = None
api = None
celery = None


def create_app():

    # Create an instance of the app
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "88de62152601bbef1f6fce8d"

    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)

    # Initializing the database
    db.init_app(app)

    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.Task = workers.ContextTask
    app.app_context().push()

    return app, celery


app, celery = create_app()
# Enable CORS
# CORS(app)
CORS(app, resources={r"*": {"origins": "*"}})

# Import all the controllers so they are loaded
from application.controllers import *


api = Api(app)

jwt = JWTManager(app)

from application.api import *

db.create_all()
# with app.app_context():
#     db.create_all()
from application.authentication import *

# Add all restful controllers
api.add_resource(UserResource, "/api/users", "/api/users/<user_id>")
api.add_resource(BookListResource, "/api/books/all")
api.add_resource(SectionListResource, "/api/sections/all")
api.add_resource(BookResource, "/api/books", "/api/books/<book_id>")
api.add_resource(SectionResource, "/api/sections", "/api/sections/<section_id>")
api.add_resource(ReviewResource, "/api/reviews", "/api/reviews/<roll>")
api.add_resource(ReviewListResource, "/api/reviews/all")
api.add_resource(UserListResource, "/api/users/all")

from application.tasks import *


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=8080, debug=True)
