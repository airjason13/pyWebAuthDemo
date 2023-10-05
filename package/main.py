# main.py
import os
from datetime import timedelta
from flask import Blueprint, render_template, url_for, redirect, request, session, send_from_directory
from flask_login import login_required, current_user, logout_user
from . import db
from . import auth
import json
main = Blueprint('main', __name__)



@main.route('/')
def index():
	return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
	print("profile")
	jpg_filename = "CyberSecurity.jpg"
	try:
		messages = request.args['messages']
		# messages = session['messages']
		print(messages)
		filename = messages.strip('{}').split(':')[1]
		print("filename :", filename)
		filename = filename.replace('"', '')
		filename = filename.lstrip(" ")
		print("filename :", filename)
		jpg_filename = filename
	except Exception as e:
		print(e)
	print("jpg_filename :", jpg_filename)
	return render_template('profile.html', name=current_user.name, show_jpg_filename=jpg_filename)


@main.route('/uploads/', methods=['GET', 'POST'])
@login_required
def uploads():
	print("request.files['file']", request.files['file'])
	f = request.files['file']
	UPLOAD_FOLDER = os.getcwd() + "/package/static/material/"
	f.save(UPLOAD_FOLDER + "/" + f.filename)
	print("f.filename:", f.filename)
	os.sync()

	messages = json.dumps({"name": f.filename})
	session['messages'] = messages
	return redirect(url_for('main.profile', messages=messages))
	# return render_template('profile.html', name=current_user.name, show_jpg_filename="CyberSecurity.jpg")
	# return render_template('profile.html', name=current_user.name, show_jpg_filename="CyberSecurity.jpg")


@main.route('/get_thumbnail/<filename>')
@login_required
def route_get_thumbnail(filename):
	print("os.getcwd :", os.getcwd())
	print("filename:", filename)
	material_path = os.getcwd() + "/package/static/material/"
	return send_from_directory(material_path, filename, as_attachment=True)


@main.route('/reauth/', methods=('GET', 'POST'))
def reauth():
	print("main reauth\n")
	print("remote ip : ", request.remote_addr)
	auth.logout()
	# return render_template('index.html')
	if current_user is None:
		print("current_user is None")
		return render_template('profile.html', name="Bad guy!")
	return render_template('profile.html', name=current_user.name, show_jpg_filename="CyberSecurity.jpg")


@main.before_app_request
def create_tables():
	db.create_all()


