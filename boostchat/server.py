__author__ = 'Oscar Eriksson <oscar.eriks@gmail.com>'

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask import Blueprint

socketio = SocketIO()
main = Blueprint('main', __name__)


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    app.register_blueprint(main)

    socketio = SocketIO(app, message_queue='redis://')
    socketio.init_app(app)
    return app


def start():
    app = create_app()
    socketio.run(app)


@socketio.on('connect', namespace='/chat')
def connect(data):
    pprint(data)
    user_id = data['user_id']
    join_room(user_id)
    emit('response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/chat')
def disconnect(data):
    user_id = data['user_id']
    leave_room(user_id)


from pprint import pprint

@socketio.on('text', namespace='/chat')
def on_message(data):
    pprint(data)
    target = data['target']
    send(data, json=True, namespace='/chat', room=target)

from flask import session, redirect, url_for, render_template, request
from .forms import LoginForm


@main.route('/', methods=['GET', 'POST'])
def index():
    """"Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['user_id'] = form.user_id.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.user_id.data = session.get('user_id', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('user_id', '')
    if name == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=name, user_id=name)