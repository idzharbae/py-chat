from app import app, socketio, db
from flask import request, render_template, redirect, url_for, session, flash
from app.controller.ChatController import ChatController
# from app.controller.AuthController import AuthController
from app.forms.LoginForm import LoginForm
from app.forms.RegisterForm import RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.model.User import User


chatController = ChatController(socketio)

@app.route('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('chat'))
	else:
		return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('chat'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('chat'))
	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat():
	return chatController.chat()

@app.route('/chat/<room>')
@login_required
def chatRoom(room):
	return chatController.chatRoom(room)

@app.route('/new-room', methods=['GET','POST'])
@login_required
def newRoom():
	return chatController.newRoom()

@socketio.on('connection-event')
def connectionEvent():
	return chatController.connectionEvent()

@socketio.on('disconnect')
def disconnectEvent():
	return chatController.disconnect()

@socketio.on('room')
def roomBroadcast(json, methods=['GET','POST']):
	return chatController.roomBroadcast(json, methods)
