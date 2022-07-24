

import pika, sys, os
import pickle
import random
from hashlib import sha256





def main():
    global roverNumber
    roverNumber = input("Enter the Deminer number: ")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='Demine-Queue')

    def callback(ch, method, properties, body):
        demining_task = pickle.loads(body)
        print(" [x] Received %r" % demining_task)

        pin = disarm_mine(demining_task)

        publish_pin(pin, demining_task)


    channel.basic_consume(queue='Demine-Queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for mining tasks. To exit press CTRL+C')
    channel.start_consuming()

def disarm_mine(mine_info):
    number = random.randint(1000, 9999)
    temp_mine_key = str(number) + str(mine_info["serialNum"])
    print("TEMP MINE KEY: ", temp_mine_key)
    hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
    print("HASH: ", hash)
    while (hash[0] != '0'):
        print("pin invalid, try again")
        number = random.randint(1000, 9999)
        temp_mine_key = str(number) + str(mine_info["serialNum"])
        # print("TEMP MINE KEY: ", temp_mine_key)
        hash = sha256(temp_mine_key.encode('utf-8')).hexdigest()
        # print("HASH: ", hash)
    print("pin valid")
    return number

def publish_pin(pin, mine_info):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='Defused-Mines')

    defused_mine_info = {
        "coordinates": mine_info["coordinates"],
        "PIN": pin
        }

    channel.basic_publish(exchange='', routing_key='Defused-Mines', body=pickle.dumps(defused_mine_info))
    print(" [x] Sent PIN: " + str(pin))
    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)