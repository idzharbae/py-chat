from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import sys, os, config
from controller.ChatController import ChatController
from controller.AuthController import AuthController

app = Flask(__name__)
app = config.config(app)
socketio = SocketIO(app)
chatController = ChatController(socketio)
authController = AuthController(app)

@app.route('/')
def login():
	if 'username' in request.cookies:
		return redirect('/chat/dashboard')
	return render_template('login.html')

@app.route('/chat')
def chat():
	return chatController.chat()

@app.route('/chat/<room>')
def chatRoom(room):
	return chatController.chatRoom(room)

@app.route('/new-room', methods=['GET','POST'])
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

if __name__ == '__main__':
	socketio.run(app, debug=True)

