import berserk
import os
from dotenv import load_dotenv
import sys
import secrets
import engine
def not_empty(moves: list):
    if moves == ['']:
        return 0
    else:
        return len(moves)
def invert_color(color: str):
    if color == "white":
        return "black"
    elif color == "black":
        return "white"
load_dotenv()
key = os.environ.get("BOT_KEY")
session = berserk.TokenSession(key)
client = berserk.Client(session=session)
isMyTurn = False
fen = 'startpos'
for response in client.bots.stream_incoming_events():
    if response.get("type") == "challenge":
        game_id = response['challenge']['id']
        if response['challenge']['rated'] == True:
            client.bots.decline_challenge(game_id, 'rated')
            sys.exit()
        color = invert_color(response['challenge']['finalColor'])
        client.bots.accept_challenge(game_id)
        break
    elif response.get("type") == "gameStart":
        fen = response['game']['fen']
        game_id = response['game']['gameId']
        isMyTurn = response['game']['isMyTurn']
        color = response['game']['color']
        break
chess_engine = engine.Engine()
def make_move(move_list: str, fen: str):
    moves = chess_engine.evaluate(move_list, fen)
    move = moves[0][secrets.randbelow(len(moves[0]))]
    client.bots.make_move(game_id, move)
if isMyTurn:
    make_move("", fen)
    isMyTurn = False
elif color == "white" and fen == "startpos":
    make_move("", fen)
for response in client.bots.stream_game_state(game_id):
    if response.get("moves") is not None:
        count = not_empty(str(response['moves']).split(' '))
        bot_turn = (count%2==1 and color=="black") or (count%2==0 and color=="white")
        if bot_turn:
            make_move(response['moves'], fen)
        else:
            if response.get("initialFen") is not None:
                fen = response['initialFen']