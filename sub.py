#final sub.py
import paho.mqtt.client as mqttClient
import time
import sys

c=0
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\n\tConnected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
        #client.publish("toAddSubCar",str(toApend))
    else:
        print("Connection failed")


def on_message(client, userdata, message):  
    print("\n" + (message.payload).decode())
    if message.topic == "carlocation/pub":
        client.unsubscribe("carlocation/pub")

    if message.topic == "location/pub":
        client.unsubscribe("location/pub")

    if message.topic == "Parking.message/pub":
        client.unsubscribe("Parking.message/pub")
     
    k = (message.payload).decode().split(",")
    if message.topic == "free.space/pub":
        Allocate();
    time.sleep(2)
    #print("Message Received on Topic " + str(message.topic))

def Allocate():
    client.unsubscribe("free.space/pub")
    c = input("\nEnter your choice for parking slot: ")
    client.publish("free.space2/pub",str(choice+","+c+","+car_number))


#def printCarLoc():
    #print((message.payload).decode())


Connected = False  # global variable for the state of the connection
#client_name="sub" #client name should be unique

broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port
user = "admin"  # Connection username
password = "hivemq"  # Connection password
print("\n-------------------- Welcome to Smart Parking System Demo!! --------------------")
print("\n")
userName=input("Enter your Name: ")
toApend = input("Please enter a valid car number: ")
#print(toApend)
client_name=toApend
print("\n")
print("\tHi! "+userName)
print("\tPress 1 to find parking space")
print("\tPress 2 to find your car")
print("\tPress 3 to exit parking space\n")
choice=input("Enter your choice: ")

if int(choice)==1:
	car_number=toApend
	choice_car_number=choice+","+car_number

elif int(choice)==2:
	vehicle_num=input("Enter last 4 digit of your car: ")
	choice_vehicle_num=choice+","+vehicle_num

elif int(choice)==3:
    vehicle_number=input("Enter your car number: ")
    choice_vehicle_number=choice+","+vehicle_number
		
client = mqttClient.Client(client_name)  # create new instance

client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.subscribe("Parking.message/pub")
client.loop_start()  # start the loop

while Connected != True:  # Wait for connection
   time.sleep(0.1)

try:
    while True:
        if(int(choice)==1):
            client.subscribe("free.space/pub")
            client.publish("location/sub",str(choice_car_number))
            
           
        elif(int(choice)==2):
            client.subscribe("carlocation/pub")
            client.publish("location/sub55",str(choice_vehicle_num))
            
        elif(int(choice)==3):
            client.subscribe("location/pub")
            client.publish("location/sub3",str(choice_vehicle_number))
            
        time.sleep(10)
        check=input("\n\tDo you want to continue(Y/N): ")
        if check == 'N' or check == 'n':
        	exit(1)
        #print("Press 1 to Find parking space")
        print("\n\tPress 2 to Find your car")
        print("\tPress 3 to exit parking space")
        choice=input("\nEnter your choice: ")
        if int(choice)==1:
            client.subscribe("free.space/pub")
            car_number=input("Enter your car number: ")
            choice_car_number=choice+","+car_number
            
            
        elif int(choice)==2:
            client.subscribe("carlocation/pub")
            vehicle_num=input("Enter last 4 digit of your car: ")
            choice_vehicle_num=choice+","+vehicle_num
            #client.publish("location/sub",str(choice_vehicle_num))
            

        elif(int(choice)==3):
            client.subscribe("location/pub")
            vehicle_number=input("Enter your car number: ")
            choice_vehicle_number=choice+","+vehicle_number
            #client.publish("location/sub3",str(choice_vehicle_number))
            
        time.sleep(3)   


except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
