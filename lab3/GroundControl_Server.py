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
"""The Python implementation of the GRPC helloworld.Greeter server."""

# python3 -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/ground_control.proto

from concurrent import futures
import logging

import grpc
import requests
import json

import ground_control_pb2
import ground_control_pb2_grpc

import pika
from threading import Thread
import pickle

class GroundControl(ground_control_pb2_grpc.GroundControlServicer):

    def getMap(self, request, context):
        with open("map.txt", "r") as f:
            rowsAndColumns = f.readline().split();
            global rows
            rows = rowsAndColumns[0]
            global columns
            columns = rowsAndColumns[1]

            print(rows + " " + columns)
            array = []
            for line in f:
                array = array + line.split()

        print(array)

        #array = ['0', '1', '2']

        return ground_control_pb2.mapReply(map=array, rowsNum=rows, colsNum=columns)

    def getCommands(self, request, context):
        response = requests.get('https://coe892.reev.dev/lab1/rover/' + str(request.commandNum))

        data = response.text

        parse_json = json.loads(data);

        moves = parse_json['data']['moves']

        # print("moves: " + moves)
        return ground_control_pb2.commandsReply(commands=moves)

    def getMineSerialNum(self, request, context):
        with open("serial_numbers.txt", "r") as f:
            position = request.roverPosition.split(" ");
            array = []
            for line in f:
                array.insert(len(array), line.split(" "))

            serial_number = array[int(position[1])][int(position[0])]

        return ground_control_pb2.serialNumReply(serialNum=serial_number)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ground_control_pb2_grpc.add_GroundControlServicer_to_server(GroundControl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def getPIN():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='Defused-Mines')

    def callback(ch, method, properties, body):
        defused_mine = pickle.loads(body)
        print(" [x] Received PIN" + str(defused_mine["PIN"]))
        f = open("defused_mines.txt", "a")
        f.write("Defused mine at (" + str(defused_mine["coordinates"][0]) + ", " + str(defused_mine["coordinates"][0]) + ") with PIN: " + str(defused_mine["PIN"]) +"\n")
        f.close()

    channel.basic_consume(queue='Defused-Mines', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    logging.basicConfig()

    t1 = Thread(target=serve)
    t2 = Thread(target=getPIN)

    t1.start()
    t2.start()
