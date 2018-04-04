from flask import g, session
from app import socketio, celery_app


def push_model(model):
    """Push the model to all connected Socket.IO clients."""
    socketio.emit('updated_model', {'class': model.__class__.__name__,
                                    'model': model.to_dict()})


@socketio.on('ping_user')
def on_ping_user(token):
    """Clients must send this event periodically to keep the user online."""
    # verify_token(token, add_to_session=True)
    print("kkkkkkkkkkk***********")
    return "ddfdfd"
    # if g.current_user:
    #     # Mark the user as still online
    #     g.current_user.ping()


@celery_app.task
def post_message(user_id, data):
    """Celery task that posts a message."""


@socketio.on('post_message')
def on_post_message(data, token):
    """Clients send this event to when the user posts a message."""
    # verify_token(token, add_to_session=True)
    if g.current_user:
        post_message.apply_async(args=(g.current_user.id, data))


@socketio.on('disconnect')
def on_disconnect():
    """A Socket.IO client has disconnected. If we know who the user is, then
    update our state accordingly.
    """
