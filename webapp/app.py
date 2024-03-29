from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from game_connect4 import Connect4, transposition_table
import numpy as np
import json

app = Flask(__name__)
CORS(app)

game = Connect4()

@app.route('/')
def index():
    global game
    game = Connect4()
    return render_template('index.html', game=game.gameboard.tolist())

@app.route('/start_game', methods=['GET'])
def start_game():
    global game
    game = Connect4()
    return jsonify({'game': game.gameboard.tolist(), 'coin': game.coin})

@app.route('/play', methods=['POST'])
def play():
    global game
    x = int(request.json.get('x')) if request.json.get('x') is not None else None
    result = game.add_coin(x)
    # game.print_gameboard()
    # print(game.top_row)
    x = int(x -1)
    y = int(game.top_row[x]+1)
    return jsonify({'result': result, 'game': game.gameboard.tolist(), 'coin': game.coin, 'x': x, 'y':y})

@app.route('/reset', methods=['POST'])
def reset():
    global game
    global transposition_table
    game.reset()
    transposition_table = {}
    return jsonify({'game': game.gameboard.tolist(), 'coin': game.coin})

@app.route('/ai_move', methods=['POST'])
def ai_move():
    global game
    x = game.generate_move()
    result = game.add_coin(x)
    y = int(game.top_row[x-1]+1)
    return jsonify({'result': result, 'game': game.gameboard.tolist(), 'coin': game.coin, 'x': int(x), 'y':y})

if __name__ == "__main__":
    app.run(debug=True)
