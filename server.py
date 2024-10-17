import socket

## Default paradime of creating a class for the socket binding

hostSocket = socket.socket()

hostSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

hostSocket.bind((socket.gethostname(), 5112))

print("Waiting for programs to connect....")

hostSocket.listen(2)

client, address = hostSocket.accept()

gameProgress = [['-1', '-1', '-1'], ['-1', '-1', '-1'], ['-1', '-1', '-1']]
print("We Connected", address)


def changeArrayToString(
        gameProgress):  # Makes the array a string to be recieved
    joinedStrings = []
    for smallArray in gameProgress:  # Splits the string up in parts
        joinedStrings.append(','.join(smallArray))
    return '|'.join(joinedStrings)


def stringToArray(string):
    global gameProgress
    gameProgress = string.split('|')  # Returns the string to an array
    for i in range(len(gameProgress)):
        gameProgress[i] = gameProgress[i].split(',')
    return gameProgress


def ChangeInputToGameValue(user_input):  # Input would be a value like B3
    global gameProgress

    while True:
        if len(user_input) != 2:
            user_input = input("Your Move: ")
            continue
        if user_input[0].upper() not in ['A', 'B', 'C']:
            user_input = input("Your Move: ")
            continue
        try:
            column = int(user_input[1]) - 1
            if column < 0 or column >= len(gameProgress[0]):
                user_input = input("Your Move: ")
                continue
        except ValueError:
            user_input = input("Your Move: ")
            continue
        break

    if user_input[0].upper() == 'A':
        gameProgress[0][column] = 'O'
    elif user_input[0].upper() == 'B':
        gameProgress[1][column] = 'O'
    elif user_input[0].upper() == 'C':
        gameProgress[2][column] = 'O'

    return True


#client.sendall(b"Welcome to the game, please enter your move")
client.sendall(changeArrayToString(gameProgress).encode())

runner = True
while runner:
    print("Waiting for opponent's first move. Don't type anything!")
    gameProgress = stringToArray(client.recv(100000).decode())
    print(gameProgress)
    # changeArrayToString(input("Your Move: "))
    ChangeInputToGameValue(input('Your Move: '))
    client.sendall(changeArrayToString(gameProgress).encode())
