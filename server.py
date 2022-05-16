import time
from flask import Flask, request, render_template, redirect
from flask_socketio import SocketIO, emit
from MySQL_Commands import DB_Commands

app = Flask(__name__)
socket = SocketIO(app)
db = DB_Commands()
#traversing pages
@app.route('/')
def login():
    return render_template("login.html")

@app.route('/client')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/create_group')
def create_group():
    return render_template("group.html")

#socket commands
@socket.on('login')
def login(username_password):
    print("[LOGIN]: ", username_password)
    user_data = db.on_login(username_password)
    if user_data[0] != "#":
        print("[LOGIN FAIL]")
        emit('login_fail', broadcast=False)
    else:
        print("[LOGIN SUCCESS REDIRECT TO CLIENT]")
        emit('login_success', user_data, broadcast=False)

@socket.on('register')
def register(username_password_chatname):
    reg_status = db.on_register(username_password_chatname)
    if reg_status == "Error 1":
        emit('register_fail', "Login name already taken!", broadcast=False)
    elif reg_status == "Error 2":
        print("[REGISTER ERROR]")
        emit('register_fail', "Too many users with this chat name!", broadcast=False)
    else:
        print("[REGISTER SUCCESS]")
        emit('register_success', broadcast=False)

@socket.on('group')
def group(new_group):
    group_status = db.on_create(new_group)
    if group_status == "Error 3":
        emit("create_fail", broadcast=False)
    else:
        emit('create_success', group_status, broadcast=False)
@socket.on('join')
def join(join_code):
    join_status = db.on_join(join_code)
    if join_status == "Error 4":
        emit('join_fail', "Group chat does not exist!")
    elif join_status == "Error 5":
        emit('join_fail', "You are already in this group!")
    else:
        emit('join_success', join_status)
        
@socket.on('viewing')
def viewing(group_id):
    messages = db.on_viewing(group_id)
    for i in reversed(messages):
        messages = f"{i[0]}|@@@|[{i[2]} {i[3]}]: {i[5]}|@@@|{i[4]}"
        emit('returndata', messages, broadcast=False)

@socket.on('connect')
def connect():
    print("[CLIENT CONNECTED]:", request.sid)

@socket.on('disconnect')
def disconn():
    print("[CLIENT DISCONNECTED]:", request.sid)

@socket.on('notify')
def notify(user):
    print("[NOTIFY]:", user)
    status = db.on_notify(user)
    emit('notify_', status, broadcast=True)

@socket.on('data')
def emitback(data):
    print(data)
    group_id, data = data.split("@#@#@_")
    print("[RETURN DATA]:", data)
    data = db.on_send(group_id, data)
    emit('returndata', data, broadcast=True)

@socket.on('room_code')
def room_code(group_id):
    code = db.on_room_code(group_id)
    emit("join_code_return", code, broadcast=False)
    

if __name__ == "__main__":
    socket.run(app)