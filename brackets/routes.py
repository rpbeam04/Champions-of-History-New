from flask import Blueprint, render_template

from .services import build_bracket_preview

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/bracket")
def bracket():
    return render_template("bracket_page.html", bracket_html=build_bracket_preview())