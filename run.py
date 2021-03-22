# from game import routes
from game import app 
from flask_socketio import SocketIO, join_room, leave_room

socketio = SocketIO(app)


@socketio.on('send_message')
def handle_send_message_event(data):
    print(data)
    # app.logger.info("{} has sent message to the room {}. Message: {}".format(data['username'], data['room'], data['message']))
    socketio.emit('recieve_message', data, room=data['room'])
@socketio.on('join_room')
def handle_join_room_event(data):
  join_room(data['room'])
  
  user= data['username']
  if user == "":
      socketio.emit('join_room_annoucement', f"Anonymous has joined")
  else:
    socketio.emit('join_room_annoucement', f"{data['username']} has joined")

@socketio.on('start_game')
def start_game():
  socketio.emit('game_started')









if __name__ == "__main__":
  socketio.run(app, debug=True)