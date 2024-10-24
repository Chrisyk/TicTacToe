"""
Name: Christopher Ko
Team: Christopher Ko, Jas Chwala
Date: 10/23/2024
Assignment: (Assignment #4)
Due Date: 10/23/2024
About this project: The client side connects to the server and allows the user to play tic-tac-toe through a socket connection.
Assumptions: Assumes the server is running in the same network and given port. assumes that the players take turns to the end of the game nicely.
    If other situations such as players making moves out of order or client/server crashing/losing connection in the middle of the game,
    the program’s behavior can be non-deterministic. 
All work below was performed solely by Christopher Ko and Jas Chwala.
I used code generated by an AI tool.
"""

import sys
import socket
from ticTacToeLogic import TicTacToeClient


if len(sys.argv) != 2:
    print("Usage: ko_c_tictactoeclient.py <port>")
    sys.exit(1)

try:
    port = int(sys.argv[1])
except ValueError:
    print("Please provide a valid port number.")
    sys.exit(1)

ttc = TicTacToeClient()
opponentMove = None
clientMove = None
sock = socket.socket()

sock.connect((socket.gethostname(), port))

def check_input(user_input):
    while True:
        if len(user_input) != 2:
            user_input = input("Enter a move([ABC][123]): ")
            continue
        if user_input[0].upper() not in ['A', 'B', 'C']:
            user_input = input("Enter a move([ABC][123]): ")
            continue
        try:
            column = int(user_input[1]) - 1
            if column < 0 or column >= 3:
                user_input = input("Enter a move([ABC][123]): ")
                continue
        except ValueError:
            user_input = input("Enter a move([ABC][123]): ")
            continue
        break
    return user_input

print(ttc)

while True:
    if ttc.checkGameStatus():
        exit()
    if opponentMove:
        clientMove = check_input(input(f"Your opponent played {opponentMove}, your move([ABC][123]): "))
    else:
        clientMove = check_input(input("Enter a move([ABC][123]): "))

    while not ttc.inputToUserGameValue(clientMove):
        print("This square has already been played (please try again).")
        clientMove = check_input(input(f"Your opponent played {opponentMove}, your move([ABC][123]): "))

    print(ttc)
    sock.sendall(clientMove.encode())
    if ttc.checkGameStatus():
        exit()
    print("Wait for your opponent move (don't type anything)!")
    opponentMove = sock.recv(100000).decode()
    ttc.inputToOpponentGameValue(opponentMove)
    print(ttc)

