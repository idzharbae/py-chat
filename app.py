from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
rooms = ['dashboard','random','work']
connectedUsers = {}

@app.route('/')
def login():
	if 'username' in request.cookies:
		return redirect('/chat/')
	return render_template('login.html')

@app.route('/chat/<room>')
def sessions(room):
	if 'username' not in request.cookies:
		return redirect(url_for('login'))
	return render_template('dashboard.html', user='world', connectedUsers=connectedUsers, room=room, rooms=rooms)

@socketio.on('connection-event')
def connectionEvent():
	print('connection event.')
	username = request.cookies.get('username')
	room = request.cookies.get('room')
	if room in connectedUsers:
		connectedUsers[room].append(username)
	else:
		connectedUsers[room] = [username]
	socketio.emit('update-online-users-'+room, (username, connectedUsers[room]))

@socketio.on('disconnect')
def disconnect():
	username = request.cookies.get('username')
	room = request.cookies.get('room')
	print(username+' disconnected.')
	connectedUsers[room].remove(username)
	socketio.emit('disconnect-online-users-'+room, (username, connectedUsers))
	print('disconnection event.')

@socketio.on('room')
def handleMyCustomEvent(json, methods=['GET','POST']):
	print('room message: '+str(json))
	socketio.emit('message-broadcast-'+json['room'], json)

if __name__ == '__main__':
	socketio.run(app, debug=True)

