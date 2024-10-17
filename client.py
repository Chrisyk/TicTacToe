import socket

gameProgress = []


def changeArrayToString(
        gameProgress):  # Makes the array a string to be recieved
    joinedStrings = []
    for smallArray in gameProgress:  # Splits the string up in parts
        joinedStrings.append(','.join(smallArray))
    return '|'.join(joinedStrings)


def stringToArray(string):
    global gameProgress

    print(string)

    gameProgress = string.split('|')  # Returns the string to an array
    print(gameProgress)
    for i in range(len(gameProgress)):
        print(gameProgress[i])
        gameProgress[i] = gameProgress[i].split(',')
    print(gameProgress)
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
        gameProgress[0][column] = '#'
    elif user_input[0].upper() == 'B':
        gameProgress[1][column] = '#'
    elif user_input[0].upper() == 'C':
        gameProgress[2][column] = '#'

    return True


sock = socket.socket()

sock.connect((socket.gethostname(), 5112))

while True:
    gameProgress = stringToArray(sock.recv(100000).decode())
    print(gameProgress)
    ChangeInputToGameValue(input("Your Move: "))
    sock.sendall(changeArrayToString(gameProgress).encode())
    print(gameProgress)
    print("Waiting for opponent's first move. Don't type anything!")
