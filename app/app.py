
from flask import Flask, render_template
from database import create_db

import sys
sys.path.append(".")
sys.path.append("..")

import date_utils
from routers import (
    calendar,
    gallery,
    search,
    about,
    api,
)

flaskApp = Flask(__name__)
flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memoryful_day_database.db'

@flaskApp.route("/")
def index() -> str:
    title = "Main Page"
    return render_template(
        "index.html",
        title=title
    )

flaskApp.register_blueprint(calendar.calendar_bp, url_prefix="/calendar")
flaskApp.register_blueprint(gallery.gallery_bp, url_prefix="/gallery")
flaskApp.register_blueprint(search.search_bp, url_prefix="/search")
flaskApp.register_blueprint(api.api_bp, url_prefix="/api")
flaskApp.register_blueprint(about.about_bp, url_prefix="/about")

@flaskApp.context_processor
def inject_variables():
    return dict(
        get_month_name = date_utils.month_number_to_name,
        get_current_year = date_utils.get_current_year
    )

if __name__ == '__main__':
    create_db(flaskApp)
    flaskApp.run(debug=True)

