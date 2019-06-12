from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
	content = render_template('content.html')
	scripts = render_template('scripts.html')
	return render_template('session.html', user='world', title='Session', content=content, scripts=scripts)

def messageReceived(methods=['GET','POST']):
	print('message was recevied.')

@socketio.on('my event')
def handleMyCustomEvent(json, methods=['GET','POST']):
	print('received my event: '+str(json))
	socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
	socketio.run(app, debug=True)

