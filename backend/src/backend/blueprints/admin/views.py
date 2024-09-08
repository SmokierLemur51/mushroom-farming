import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app

from ...models.models import db
from .forms import 


admin = Blueprint('admin', __name__, template_folder="templates/admin", url_prefix="/admin")


@admin.route("/")
def index():
    elements = {
        "title": "Welcome Team", 
    }
    return render_template("admin_index.html", elements=elements)


