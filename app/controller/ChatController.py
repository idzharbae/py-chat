from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
from flask_login import current_user

class ChatController:
	def __init__(self, socketio):
		self.socketio = socketio
		self.rooms = ['Dashboard', 'Random', 'Work']
		self.connectedUsers = {}
		if current_user != None:
			self.username = current_user.username
		else:
			self.username = None

	def chat(self):
		return redirect('/chat/dashboard')

	def chatRoom(self,room):
		if 'username' not in request.cookies:
			return redirect(url_for('login'))
		return render_template('dashboard.html', user='world', connectedUsers=self.connectedUsers, room=room, rooms=self.rooms)

	def newRoom(self):
		room = request.form['roomTitle']
		self.rooms.append(room)
		return redirect('/chat/'+room)

	def connectionEvent(self):
		print('connection event.')
		room = request.cookies.get('room')
		if room in self.connectedUsers:
			self.connectedUsers[room].append(self.username)
		else:
			self.connectedUsers[room] = [self.username]
		self.socketio.emit('update-online-users-'+room, (self.username, self.connectedUsers[room]))

	def disconnect(self):
		room = request.cookies.get('room')
		print(self.username+' disconnected.')
		self.connectedUsers[room].remove(username)
		self.socketio.emit('disconnect-online-users-'+room, (self.username, self.connectedUsers))
		print('disconnection event.')

	def roomBroadcast(self, json, methods=['GET','POST']):
		print('room message: '+str(json))
		self.socketio.emit('message-broadcast-'+json['room'], json)