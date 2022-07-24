import requests
import json
import threading
from threading import Thread
from time import sleep, perf_counter

# get moves
def getMoves(number):
    response = requests.get('https://coe892.reev.dev/lab1/rover/' + str(number))

    data = response.text

    parse_json = json.loads(data);

    moves = parse_json['data']['moves']

    # print("moves: " + moves)

    return moves


# start traversing minefield
def startTraverse(num):
    global roverDirectionState
    global roverState
    global roverPosition
    roverState = "Alive"
    roverDirectionState = 'South'
    roverPosition = [0, 0]  # x, y

    f = open("path_" + str(num) + ".txt", "w+");

    arrayPath = array;
    arrayPath[0][0] = "*"

    moves = getMoves(num)

    for i in range(len(moves)):
        if (moves[i] == 'M'):  # move forward
            state = moveForward()
            if (state == "Dead"):
                roverState = "Dead"
                break

        elif (moves[i] == 'L'):  # turn left
            roverDirectionState = turnLeft(roverDirectionState)
        elif (moves[i] == 'R'):  # turn right
            roverDirectionState = turnRight(roverDirectionState)
        elif (moves[i] == 'D'):
            if(arrayPath[roverPosition[1]][roverPosition[0]] == '1'):
                print("mine is here, start digging")
            else:
                print("mine not here")
        print("Direction: " + roverDirectionState)
        print("Position: ", roverPosition)
        print("---------")

    for row in arrayPath:
        f.write(" ".join(row) + "\n")


def moveForward():
    try:
        if (roverDirectionState == 'North'):
            if (roverPosition[1] == 0):
                print("Command Ignored: At the edge");
                return
            if (arrayPath[roverPosition[1] - 1][roverPosition[0]] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState

            roverPosition[1] = roverPosition[1] - 1;
            arrayPath[roverPosition[1]][roverPosition[0]] = "*"
        elif (roverDirectionState == 'South'):
            if (roverPosition[1] == rows):
                print("Command Ignored: At the edge");
                return
            if (arrayPath[roverPosition[1] + 1][roverPosition[0]] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState

            roverPosition[1] = roverPosition[1] + 1;
            arrayPath[roverPosition[1]][roverPosition[0]] = "*"
        elif (roverDirectionState == 'East'):
            if (roverPosition[0] == columns):
                print("Command Ignored: At the edge");
                return

            if (arrayPath[roverPosition[1]][roverPosition[0] + 1] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState

            roverPosition[0] = roverPosition[0] + 1;
            arrayPath[roverPosition[1]][roverPosition[0]] = "*"
        elif (roverDirectionState == 'West'):
            if (roverPosition[0] == 0):
                print("Command Ignored: At the edge");
                return
            if (arrayPath[roverPosition[1]][roverPosition[0] - 1] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState

            roverPosition[0] = roverPosition[0] - 1;
            arrayPath[roverPosition[1]][roverPosition[0]] = "*"
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

with open("map.txt", "r") as f:
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



arrayPath = array;
arrayPath[0][0] = "*"

for i in range(1, 11, 1):
    startTraverse(i)
    print("------------------- TRAVERSE " + str(i) + " COMPLETED -------------------")

end_time = perf_counter();

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

print("seq program done....")
seq_done = 1

def createArray_thr():
    with open("map.txt", "r") as f:
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



def thr2():
    roverState = "Alive"
    roverDirectionState = 'South'
    roverPosition = [0, 0]  # x, y

    arrayPath = array;
    arrayPath[0][0] = "*"

    for i in range(1, 11, 1):
        startTraverse(i)



if (seq_done == 1):
    val = input("Run multithreaded program? (y/n): ")
    if(val == 'y'):
        start_time = perf_counter()


        t1 = Thread(target=createArray_thr)
        t2 = Thread(target=thr2)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        end_time = perf_counter()

        print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')