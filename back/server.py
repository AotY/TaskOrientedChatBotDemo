from flask import Flask
from flask_socketio import SocketIO, emit

from nlu_test import predict
from dst import DST
from dpl import DPL
from nlg import NLG

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

_dst = DST()
_dpl = DPL()
_nlg = NLG()

last_action, last_state = None, None
Hn = list()

@socketio.on("receive")
def recevie_msg(msg):
    print(msg)
    # get intent & slots
    nlu_result = predict(msg)

    # get state (Gn, Un, Hn)
    state = _dst.get_state(nlu_result, last_action, last_state, Hn)

    # get action
    action, Hn = _dpl.get_action(state)

    r_msg = _nlg.generate(action)

    with open("./dialog.txt", "a") as f_dialog:
        f_dialog.write(msg + "\t" + r_msg + "\n")

    emit("response", {"msg": r_msg})


if __name__ == "__main__":
    print('socketio runing ...')
    socketio.run(app, host="0.0.0.0", port=8002)
