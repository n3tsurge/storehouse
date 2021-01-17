# storehouse/views.py

import os
from flask import render_template, request, redirect, url_for, g, abort, flash, Blueprint, current_app
from .models import db, User

admin = Blueprint('list_manager', __name__, url_prefix="/admin")
auth = Blueprint('auth', __name__, url_prefix="/auth")
api = Blueprint('api', __name__, url_prefix="/api")

@current_app.before_first_request
def create_user():
    user = User(email='admin@localhost.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

@admin.route("/")
def index():
    return render_template('admin/base.html')