from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
connectedUsers = []

@app.route('/')
def login():
	if 'username' in request.cookies:
		return redirect(url_for('sessions'))
	return render_template('login.html')

@app.route('/chat')
def sessions():
	if 'username' not in request.cookies:
		return redirect(url_for('login'))
	return render_template('dashboard.html', user='world', connectedUsers=connectedUsers)

@socketio.on('connection-event')
def connectionEvent():
	print('connection event.')
	username = request.cookies.get('username')
	connectedUsers.append(username)
	socketio.emit('update-online-users', (username, connectedUsers))

@socketio.on('disconnection-event')
def disconnectionEvent(username):
	print('disconnection event.')
	connectedUsers.remove(username)
	socketio.emit('disconnect-online-user', (username, connectedUsers))

@socketio.on('room-1')
def handleMyCustomEvent(json, methods=['GET','POST']):
	print('room-1 message: '+str(json))
	if(json['username']):
		connectedUsers.append(json['username'])
		print(connectedUsers)
	socketio.emit('message-broadcast', json)

if __name__ == '__main__':
	socketio.run(app, debug=True)

