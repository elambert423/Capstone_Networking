from socket import *
import argparse
#import signal
import sys

# for encoding the image 
import base64
from PIL import Image

# for displaying the time
from datetime import datetime

from time import sleep

#from picamera import PiCamera

picture = "tempPic.jpg"

DATA_SIZE = 497

def encodeImage():
    #Compress the image

    cam_pic = Image.open(picture)
    
    #testing to see if this will work
    #cam_pic = test_camera.picture 

    scaledPic = "pic_scaled.jpg"

    #print(cam_pic.size)
    cam_pic = cam_pic.resize((800,480),Image.ANTIALIAS)
    cam_pic.save(scaledPic,quality=20) 

    image = open(scaledPic,'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)

    return image_64_encode

server_port = 12000
client_socket = socket(AF_INET,SOCK_DGRAM)

parser = argparse.ArgumentParser(description='sending images')
parser.add_argument('-s', dest='server_name', help='specifies the IP of the server, this is required', required=True)
args = parser.parse_args()

#disconnect_str = 'DCNT'

#def signal_handler(signal,frame):
#       print('Ctrl+C pressed')
#       message = disconnect_str
#       client_socket.sendto(message.encode(),(args.server_name,serverPort))
#       client_socket.close()

pic_num = 0

while True:
    sleep(1)
    #camera.capture(picture)

    string = encodeImage()

    encode_msgs = []

    while string:
        encode_msgs.append(string[:DATA_SIZE])
        string = string[DATA_SIZE:]

    i = 0

    while(i < len(encode_msgs)):
        message = encode_msgs[i]

        # for debugging, displaying time
        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        print("sending picture data")
        client_socket.sendto(message, (args.server_name,server_port))
        server_message,serverAddress = client_socket.recvfrom(2048)
        print("recieved server message")
        i = i + 1

    print("sending done msg to server")
    message = 'done'
    client_socket.sendto(message.encode(),(args.server_name,server_port))

    print("client done, waiting for server")
    server_message,serverAddress = client_socket.recvfrom(2048)

    print(server_message.decode())	

#client_socket.close()
