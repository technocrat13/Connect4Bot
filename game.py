import random


y, x = 6, 7
gameboard = [[0 for j in range(x)] for i in range(y)]

global moves
global coin
global top
global toppedOut
global notToppedOut

moves = []
toppedOut = []
notToppedOut = [0, 1, 2, 3, 4, 5, 6]



def printGameboard():
    for i in gameboard:
        print(i)

def checkConnectList(l):
    #assert len(l) == 4, return continue
    if sum(l) in [20, 28]:
        return True
    

 # check if the product is equal to 4 times coin in that move from that xPos
def checkConnect4(xPos, yPos):

    #listToCheck = []
    indexErrorCount = 0

    # checking x axis
    for i in range(1, 5):
        try:
            #listToCheck.append(gameboard[yPos][xPos - 4 + i: xPos + i])
            if checkConnectList(gameboard[yPos][xPos - 4 + i: xPos + i]) == True:
                return '4connected'
        except IndexError:
            indexErrorCount = indexErrorCount + 1

    # checking bellow xPos
    try:
        #listToCheck.append([gameboard[i][xPos] for i in range(yPos - 0, yPos + 4)])
        if checkConnectList([gameboard[i][xPos] for i in range(yPos - 0, yPos + 4)]) == True:
            return '4connected'
    except:
        indexErrorCount = indexErrorCount + 1
        #print('col not tall enough')

    # checking top down diagonals
    for j in range(0, 4):
        listDiagonal = []
        for i in range(1 + j, 5 + j):
            try:
                listDiagonal.append(gameboard[yPos - 4 + i][xPos - 4 + i])
            except:
                indexErrorCount = indexErrorCount + 1

        #listToCheck.append(listDiagonal)
        if checkConnectList(listDiagonal) == True:
            return '4connected'

    # check bottom up diagonals
    for j in range(0, 4):
        listDiagonal = []
        for i in range(1 + j, 5 + j):
            try:
                listDiagonal.append(gameboard[yPos + 4 - i][xPos - 4 + i])
            except IndexError:
                indexErrorCount = indexErrorCount + 1

        #listToCheck.append(listDiagonal)
        if checkConnectList(listDiagonal) == True:
            return '4connected'

def probableMove(xPos, yPos):
    for i in [5, 7]:
        gameboard[yPos][xPos] = i
        if checkConnect4(xPos, yPos) == '4connected':
            gameboard[yPos][xPos] = 0
            if i == 7:
                print('aha saved a connect4 at ' + str(xPos + 1))
            else:
                print('i win in this simple move at ' + str(xPos + 1))
            return '4connected'
        gameboard[yPos][xPos] = 0




def stopAll4s():
    #checkconnect4(takes xPos and then yPos) so find the highest yPos and check for every xPos

    top = []
    for i in range(0, x):
        for j in range(y - 1, -1, -1):
            if gameboard[j][i] == 0:
                top.append(j)
                break

    for j, i in zip(top, range(0, x)):
        #print('checking i , j: ' + str((i, j)))
        if probableMove(i, j) == '4connected':
            return i
    
    #move = random.randint(0, 6)
    #if move in toppedOut()
    #print('can choose from: ', end='')
    #print(notToppedOut)
    return random.choice(notToppedOut)


def validMove(xPos, yPos):
    if xPos in toppedOut:
        return False
    

    if yPos == 0:
        toppedOut.append(xPos)
        notToppedOut.remove(xPos)

    return True

    



    
def validMoveX(xPos):
    if xPos in toppedOut:
        return False
    return True



def addCoin(xPos):
    moves.append(str(xPos))
    for j in range(y - 1, -1, -1):
        #print(j)
        if gameboard[j][xPos] == 0 and validMove(xPos, j) == True:
            gameboard[j][xPos] = coin
            yPos = j
            break
    return checkConnect4(xPos, yPos)




def takeInput():
    #moves = ''
    if coin == 7:
        move = int(input('drop coin at: ').rstrip()) - 1
        while validMoveX(move) == False:
            move = int(input('last input invalid, go agane: ').rstrip()) - 1
        return move
    else:
        print('AI is calculating its next move.....')
        aiMove = stopAll4s()
        #aiMove = random.randint(0, 6)
        print('Playing at: ' + str(aiMove + 1))
        return aiMove




turn = 0
coin = 7
while addCoin(takeInput()) != '4connected':
    if turn % 2 == 0:
        coin = 5
    else:
        coin = 7

    printGameboard()
    turn = turn + 1
else:
    printGameboard()
    file = open('pastGames.txt', 'a')
    file.write('\n')
    file.write(''.join(moves))
    file.close()

print('wow ' + str(coin) + ' wins!!1!!!!1111!')
