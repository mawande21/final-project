from flask import Flask, render_template, request,redirect,url_for,session
from flask_socketio import SocketIO, join_room,leave_room,emit
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.config['SECRET_TYPE'] = 'secrete'
app.config['SESSION_TYPE'] = 'filesystem'

# initialising apps
Session(app)

socketio = SocketIO(app, manage_session=False)  # ms stops socketio from opening their own sessions

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html') # when we open it come straight to this html


@app.route('/chat', methods=['GET','POST'])  # post means whenever a user logs in the info is sent back to the server. The Get means when someone reloads we dont lose the info
# if someone logs in we need the username and room
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']  # get these entries
        # we need to store the data in a session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session=session)
# elif hes already logged in
    else:
       if(session.get('username')is not None):
           return render_template('chat.index', session=session)
       else:
           return redirect(url_for('index')) #login

# definitions for socketio
@socketio.on('text', namespace='/chat')
def text(message):  # on the textarea what must be shown
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)  # getting the massage, person who sent it and the room

# for someone who wants to join the chat
@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)  # function : letting the user join the room and passing this room
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)

# for someone who leaves the room
@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)  # function
    session.clear()  # when reloads doesn't show but gets pop out
    emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ =='__main__':
    socketio.run(app)
