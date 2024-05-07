from flask import Blueprint, render_template, request, redirect, url_for, jsonify

about_bp = Blueprint("about", __name__)


@about_bp.route("/")
def about():
    return render_template("about.html")
