import requests
import json
from hashlib import sha256
import random
import threading
from threading import Thread
from time import sleep, perf_counter



def moveForward(array):
    try:
        if (roverDirectionState == 'North'):
            if (roverPosition[1] == 0):
                print("Command Ignored: At the edge");
                return

            """if (array[roverPosition[1] - 1][roverPosition[0]][1] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""

            roverPosition[1] = roverPosition[1] - 1;

        elif (roverDirectionState == 'South'):
            if (roverPosition[1] == rows):
                print("Command Ignored: At the edge");
                return
            """if (array[roverPosition[1] + 1][roverPosition[0]][1] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""

            roverPosition[1] = roverPosition[1] + 1;

        elif (roverDirectionState == 'East'):
            if (roverPosition[0] == columns):
                print("Command Ignored: At the edge");
                return

            """if (array[roverPosition[1]][roverPosition[0] + 1][1] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""


            roverPosition[0] = roverPosition[0] + 1;

        elif (roverDirectionState == 'West'):
            if (roverPosition[0] == 0):
                print("Command Ignored: At the edge");
                return
            """if (array[roverPosition[1]][roverPosition[0] - 1][1] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""

            roverPosition[0] = roverPosition[0] - 1;

    except IndexError:
        print("index out of range")


def turnLeft(roverDirectionState):
    if (roverDirectionState == 'North'):
        roverDirectionState = 'West'
    elif (roverDirectionState == 'East'):
        roverDirectionState = 'North'
    elif (roverDirectionState == 'South'):
        roverDirectionState = 'East'
    elif (roverDirectionState == 'West'):
        roverDirectionState = 'South'
    return roverDirectionState


def turnRight(roverDirectionState):
    if (roverDirectionState == 'North'):
        roverDirectionState = 'East'
    elif (roverDirectionState == 'East'):
        roverDirectionState = 'South'
    elif (roverDirectionState == 'South'):
        roverDirectionState = 'West'
    elif (roverDirectionState == 'West'):
        roverDirectionState = 'North'
    return roverDirectionState


start_time = perf_counter()

def createArray():
    with open("mines.txt", "r") as f:
        rowsAndColumns = f.readline().split();
        global rows
        rows = rowsAndColumns[0]
        global columns
        columns = rowsAndColumns[1]

        print(rows + " " + columns)

        array = []
        for line in f:
            array.insert(len(array), line.split())

        print(array)

    return array

# get moves

def getMoves():
    response = requests.get('https://coe892.reev.dev/lab1/rover/1')

    data = response.text

    parse_json = json.loads(data);

    moves = parse_json['data']['moves']

    # moves = 'MMDLMLMDRMD'

    print("moves: " + moves)

    return moves


roverState = "Alive"
roverDirectionState = 'South'
roverPosition = [0, 0]  # x, y

# start traversing minefield
def startTraverse():
    array = createArray()
    moves = getMoves()
    global roverDirectionState

    for i in range(len(moves)):
        if (moves[i] == 'M'):  # move forward
            state = moveForward(array)
            if (state == "Dead"):
                roverState = "Dead"
                break

        elif (moves[i] == 'L'):  # turn left
            roverDirectionState = turnLeft(roverDirectionState)
        elif (moves[i] == 'R'):  # turn right
            roverDirectionState = turnRight(roverDirectionState)

        elif (moves[i] == 'D'):
            try:
                print(array)
                print(roverPosition)
                print("digging procedure: ", array[roverPosition[1]][roverPosition[0]])
                if (array[roverPosition[1]][roverPosition[0]][1] == '1'):
                    print("mine is here")
                    number = random.randint(1000, 9999)
                    temp_mine_key = str(number) + array[roverPosition[1]][roverPosition[0]];
                    print("TEMP MINE KEY: ", temp_mine_key)
                    hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
                    print("HASH: ", hash)
                    while (hash[0] != '0'):
                        print("pin invalid, try again")
                        number = random.randint(1000, 9999)
                        temp_mine_key = str(number) + array[roverPosition[1]][roverPosition[0]];
                        # print("TEMP MINE KEY: ", temp_mine_key)
                        hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
                        # print("HASH: ", hash)

                    print("pin valid, disarm mine")
                else:
                    print("mine is not here")
            except IndexError:
                print("IndexError");
        print("Direction: " + roverDirectionState)
        print("Position: ", roverPosition)
        print("---------")



start_time = perf_counter()

createArray()
getMoves()
startTraverse()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
print("seq program done....")
seq_done = 1;







def createArray_Thr():
    with open("mines.txt", "r") as f:
        rowsAndColumns = f.readline().split();
        global rows
        rows = rowsAndColumns[0]
        global columns
        columns = rowsAndColumns[1]

        print(rows + " " + columns)

        array = []
        for line in f:
            array.insert(len(array), line.split())

        print(array)

    return array
def getMoves_Thr():
    response = requests.get('https://coe892.reev.dev/lab1/rover/' + '1')

    data = response.text

    parse_json = json.loads(data);

    moves = parse_json['data']['moves']

    moves = 'MMDLMLMDRMD'

    print("moves: " + moves)

    return moves
def startTraverse_Thr():
    array = createArray()
    moves = getMoves()
    global roverDirectionState

    for i in range(len(moves)):
        if (moves[i] == 'M'):  # move forward
            state = moveForward(array)
            if (state == "Dead"):
                roverState = "Dead"
                break

        elif (moves[i] == 'L'):  # turn left
            roverDirectionState = turnLeft(roverDirectionState)
        elif (moves[i] == 'R'):  # turn right
            roverDirectionState = turnRight(roverDirectionState)

        elif (moves[i] == 'D'):
            print(array)


            print("digging procedure: ", array[roverPosition[1]][roverPosition[0]])


            if (array[roverPosition[1]][roverPosition[0]][1] == '1'):
                number = random.randint(1000, 9999)
                temp_mine_key = str(number) + array[roverPosition[1]][roverPosition[0]];
                print("TEMP MINE KEY: ", temp_mine_key)
                hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
                print("HASH: ", hash)
                while (hash[0] != '0'):
                    print("pin invalid")
                    number = random.randint(1000, 9999)
                    temp_mine_key = str(number) + array[roverPosition[1]][roverPosition[0]];
                    # print("TEMP MINE KEY: ", temp_mine_key)
                    hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
                    # print("HASH: ", hash)

                print("pin valid")
            else:
                print("no digging command, exploded.")

        print("Direction: " + roverDirectionState)
        print("Position: ", roverPosition)
        print("---------")


if(seq_done):

    roverState = "Alive"
    roverDirectionState = 'South'
    roverPosition = [0, 0]  # x, y

    start_time = perf_counter()

    t1 = Thread(target=createArray_Thr)
    t2 = Thread(target=getMoves_Thr)
    t3 = Thread(target=startTraverse_Thr)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    end_time = perf_counter()

    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

