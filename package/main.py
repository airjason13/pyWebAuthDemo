# main.py

from datetime import timedelta
from flask import Blueprint, render_template, url_for, redirect, request, session
from flask_login import login_required, current_user, logout_user
from . import db
from . import auth
main = Blueprint('main', __name__)


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
	print("profile")
	return render_template('profile.html', name=current_user.name)


@main.route('/reauth/', methods=('GET', 'POST'))
def reauth():
	print("main reauth\n")
	print("remote ip : ", request.remote_addr)
	auth.logout()
	# return render_template('index.html')
	if current_user is None:
		print("current_user is None")
		return render_template('profile.html', name="Bad guy!")
	return render_template('profile.html', name=current_user.name)


@main.route("/helloworld")
def hello_world():
    return "<p>Hello, World from \
                redirected page.!</p>"

@main.before_app_request
def create_tables():
	db.create_all()


