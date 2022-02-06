import requests
import json
import numpy as np





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


# get moves
response = requests.get('https://coe892.reev.dev/lab1/rover/' + '1')

data = response.text

parse_json = json.loads(data);

moves = parse_json['data']['moves']

print("moves: " + moves)


# start traversing minefield
# https://stackoverflow.com/questions/19753430/how-to-replace-a-single-character-in-a-text-file

f = open("path_" + str(1) + ".txt", "w+");

arrayPath = array;
arrayPath[0][0] = "*"

roverState = "Alive"
roverDirectionState = 'South'
roverPosition = [0, 0] # x, y



def moveForward():


    try:
        if(roverDirectionState == 'North'):
            if(roverPosition[1] == 0):
                print("Command Ignored: At the edge");
                return
            if (arrayPath[roverPosition[0]][roverPosition[1] - 1] == '1'):
                print("Mine Ahead");
                roverState = "Dead"
                return roverState

            roverPosition[1] = roverPosition[1] - 1;
            arrayPath[roverPosition[0]][roverPosition[1]] = "*"
        elif(roverDirectionState == 'South'):
            if (roverPosition[1] == rows):
                print("Command Ignored: At the edge");
                return
            if(arrayPath[roverPosition[0]][roverPosition[1]+1] == '1'):
                print("Mine Ahead");
                roverState = "Dead"
                return roverState

            roverPosition[1] = roverPosition[1] + 1;
            arrayPath[roverPosition[0]][roverPosition[1]] = "*"
        elif(roverDirectionState == 'East'):
            if (roverPosition[0] == columns):
                print("Command Ignored: At the edge");
                return

            if (arrayPath[roverPosition[0]+1][roverPosition[1]] == '1'):
                print("Mine Ahead");
                roverState = "Dead"
                return roverState

            roverPosition[0] = roverPosition[0] + 1;
            arrayPath[roverPosition[0]][roverPosition[1]] = "*"
        elif(roverDirectionState == 'West'):
            if (roverPosition[0] == 0):
                print("Command Ignored: At the edge");
                return
            if (arrayPath[roverPosition[0]-1][roverPosition[1]] == '1'):
                print("Mine Ahead");
                roverState = "Dead"
                return roverState

            roverPosition[0] = roverPosition[0] - 1;
            arrayPath[roverPosition[0]][roverPosition[1]] = "*"
    except IndexError:
        print("index out of range")



def turnLeft(roverDirectionState):
    if (roverDirectionState == 'North'):
        roverDirectionState = 'West'
    elif(roverDirectionState == 'East'):
        roverDirectionState = 'North'
    elif(roverDirectionState == 'South'):
        roverDirectionState = 'East'
    elif(roverDirectionState == 'West'):
        roverDirectionState = 'South'
    return roverDirectionState

def turnRight(roverDirectionState):
    
    if(roverDirectionState == 'North'):
        roverDirectionState = 'East'
    elif(roverDirectionState == 'East'):
        roverDirectionState = 'South'
    elif(roverDirectionState == 'South'):
        roverDirectionState = 'West'
    elif(roverDirectionState == 'West'):
        roverDirectionState = 'North'
    return roverDirectionState

for i in range(len(moves)):
        if(moves[i] == 'M'): # move forward
            state = moveForward()
            if(state == "Dead"):
                roverState = "Dead"
                break

        elif(moves[i] == 'L'): # turn left
            roverDirectionState = turnLeft(roverDirectionState)
        elif(moves[i] == 'R'): # turn right
            roverDirectionState = turnRight(roverDirectionState)


        print("Direction: " + roverDirectionState)
        print("Position: ",  roverPosition)
        print("---------")




for row in arrayPath:
    f.write(" ".join(row) + "\n")