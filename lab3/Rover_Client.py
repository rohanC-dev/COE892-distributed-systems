
from __future__ import print_function

import logging
import random
from hashlib import sha256
import copy

import grpc
import ground_control_pb2
import ground_control_pb2_grpc

import pika
import pickle

# source: https://stackoverflow.com/questions/14681609/create-a-2d-list-out-of-1d-list
def to_matrix(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]




def moveForward():
    try:
        if (roverDirectionState == 'North'):
            if (roverPosition[1] == 0):
                print("Command Ignored: At the edge");
                return

            """if (arrayPath[roverPosition[1] - 1][roverPosition[0]] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""


            roverPosition[1] = roverPosition[1] - 1;
            arrayPath[roverPosition[1]][roverPosition[0]] = "*"
        elif (roverDirectionState == 'South'):
            if (roverPosition[1] == rows):
                print("Command Ignored: At the edge");
                return

            """if (arrayPath[roverPosition[1] + 1][roverPosition[0]] == '1'):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""


            roverPosition[1] = roverPosition[1] + 1;
            arrayPath[roverPosition[1]][roverPosition[0]] = "*"
        elif (roverDirectionState == 'East'):
            if (roverPosition[0] == columns):
                print("Command Ignored: At the edge");
                return

            """if (arrayPath[roverPosition[1]][roverPosition[0] + 1] == '1' ):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""


            roverPosition[0] = roverPosition[0] + 1;
            arrayPath[roverPosition[1]][roverPosition[0]] = "*"
        elif (roverDirectionState == 'West'):
            if (roverPosition[0] == 0):
                print("Command Ignored: At the edge");
                return

            """if (arrayPath[roverPosition[1]][roverPosition[0] - 1] == '1' ):
                print("Mine Ahead, Exploded");
                roverState = "Dead"
                return roverState"""


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

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ground_control_pb2_grpc.GroundControlStub(channel)
        response = stub.getMap(ground_control_pb2.mapRequest())
    print("Rover client received: ")
    array = response.map;
    global rows
    global columns
    rows = response.rowsNum;
    columns = response.colsNum;

    array = to_matrix(array, int(rows));
    print(array)

    print("Rows: " + response.rowsNum)
    print("Columns: " + response.colsNum)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ground_control_pb2_grpc.GroundControlStub(channel)
        global roverNumber
        roverNumber = input("Enter the rover number: ")

        response2 = stub.getCommands(ground_control_pb2.commandsRequest(commandNum=int(roverNumber)))
        print(str(response2))

    global roverDirectionState
    global roverState
    global roverPosition
    roverState = "Alive"
    roverDirectionState = 'South'
    roverPosition = [0, 0]  # x, y

    f = open("path_" + str(roverNumber) + ".txt", "w+");

    global arrayPath
    arrayPath = copy.deepcopy(array)
    arrayPath[0][0] = "*"

    global moves
    moves = response2.commands

    global currentMoveNum
    for i in range(len(moves)):
        currentMoveNum = i

        if (moves[i] == 'M'):  # move forward
            moveForward()


        elif (moves[i] == 'L'):  # turn left
            roverDirectionState = turnLeft(roverDirectionState)
        elif (moves[i] == 'R'):  # turn right
            roverDirectionState = turnRight(roverDirectionState)
        print("Direction: " + roverDirectionState)
        print("Position: ", roverPosition)
        print("---------")

        if (array[roverPosition[1]][roverPosition[0]] == '1'):
            print("Mine Encounter")
            rover_pos_string = str(roverPosition[0]) + " " + str(roverPosition[1])
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = ground_control_pb2_grpc.GroundControlStub(channel)
                response3 = stub.getMineSerialNum(ground_control_pb2.serialNumRequest(roverPosition=rover_pos_string))

            print("Serial Number retrieved: " + str(response3.serialNum))
            demining_task = {
                             "coordinates": roverPosition,
                             "id": random.randint(1, 2),
                             "serialNum": response3.serialNum,
                             }



            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='Demine-queue')

            channel.basic_publish(exchange='', routing_key='Demine-Queue', body=pickle.dumps(demining_task)) # serializing data
            print(" [x] Sent Demining Task")
            connection.close()

            #####
            array[roverPosition[1]][roverPosition[0]] = '0'


    for row in arrayPath:
        f.write(" ".join(row) + "\n")






if __name__ == '__main__':
    logging.basicConfig()
    run()
