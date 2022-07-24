# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import random
from hashlib import sha256
import copy

import grpc
import ground_control_pb2
import ground_control_pb2_grpc

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
        elif (moves[i] == 'D'):
            """rover_pos_string = str(roverPosition[0]) + " " + str(roverPosition[1])
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = ground_control_pb2_grpc.GroundControlStub(channel)
                response3 = stub.getMineSerialNum(ground_control_pb2.serialNumRequest(roverPosition=rover_pos_string))

            print(response3)
            number = random.randint(1000, 9999)
            temp_mine_key = str(number) + str(response3.serialNum)
            print("TEMP MINE KEY: ", temp_mine_key)
            hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
            print("HASH: ", hash)
            while (hash[0] != '0'):
                print("pin invalid, try again")
                number = random.randint(1000, 9999)
                temp_mine_key = str(number) + str(response3.serialNum)
                # print("TEMP MINE KEY: ", temp_mine_key)
                hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
                # print("HASH: ", hash)
            print("pin valid, disarm mine. sharing with ground control")

            with grpc.insecure_channel('localhost:50051') as channel:
                stub = ground_control_pb2_grpc.GroundControlStub(channel)
                response4 = stub.sharePIN(ground_control_pb2.pinRequest(pin=number))
            """
            print("DIGGING COMMAND: ")
            print("MINE HERE?: " + array[roverPosition[1]][roverPosition[0]])
            if (array[roverPosition[1]][roverPosition[0]] == '1'):
                print("mine is here, start digging")
                rover_pos_string = str(roverPosition[0]) + " " + str(roverPosition[1])
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = ground_control_pb2_grpc.GroundControlStub(channel)
                    response3 = stub.getMineSerialNum(
                        ground_control_pb2.serialNumRequest(roverPosition=rover_pos_string))

                print(response3)
                number = random.randint(1000, 9999)
                temp_mine_key = str(number) + str(response3.serialNum)
                print("TEMP MINE KEY: ", temp_mine_key)
                hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
                print("HASH: ", hash)
                while (hash[0] != '0'):
                    print("pin invalid, try again")
                    number = random.randint(1000, 9999)
                    temp_mine_key = str(number) + str(response3.serialNum)
                    # print("TEMP MINE KEY: ", temp_mine_key)
                    hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
                    # print("HASH: ", hash)
                print("pin valid, disarm mine. sharing with ground control")

                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = ground_control_pb2_grpc.GroundControlStub(channel)
                    response4 = stub.sharePIN(ground_control_pb2.pinRequest(pin=number))


            else:
                print("mine not here")
        print("Direction: " + roverDirectionState)
        print("Position: ", roverPosition)
        print("---------")
        if (array[roverPosition[1]][roverPosition[0]] == '1'):
            print("Mine Encounter, Exploded");
            roverState = "Dead"
            break;

    for row in arrayPath:
        f.write(" ".join(row) + "\n")

    if(roverState == "Alive"):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = ground_control_pb2_grpc.GroundControlStub(channel)
            response5 = stub.checkCompleted(ground_control_pb2.checkRequest(roverStatus="Rover " + str(roverNumber) + " has completed"))
    else:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = ground_control_pb2_grpc.GroundControlStub(channel)
            response5 = stub.checkCompleted(ground_control_pb2.checkRequest(roverStatus="Rover " + str(roverNumber) + " has exploded"))






if __name__ == '__main__':
    logging.basicConfig()
    run()
