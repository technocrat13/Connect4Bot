from flask import Flask, render_template, session, jsonify, request
import numpy as np
from game_connect4 import Connect4

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

game = Connect4()

@app.route('/')
def index():
    session['game'] = game.gameboard.tolist()
    return render_template('index.html', game=session['game'])

@app.route('/play', methods=['POST'])
def play():
    x_pos = request.get_json()['move']
    result = game.add_coin(x_pos)
    session['game'] = game.gameboard.tolist()
    return jsonify({'result': result, 'game': session['game']})



if __name__ == '__main__':
    app.run(debug=True)
