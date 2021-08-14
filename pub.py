#Fnal pub.py

import paho.mqtt.client as mqttClient
import time
import ast
import random

global b
Parking_loc={}
Parking_loc={'default':'0'}
size=20
i=1
location_val=[]
loc_val_str=[]
free_space=[]*22
s=0
Parking_space_occupied=[0]*22

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
       # client.subscribe("toAddSubCar")
        
    else:
        print("Connection failed Return Code : ",rc)


def on_message(client, userdata, message):
    Received=(message.payload).decode()
    print("\n\tMessage Received is : " +Received)
    k1=1
    k2=2
    toApend=""
    if message.topic=="free.space2/pub":
        b=(message.payload).decode().split(",")
        k1,k2=b[2],b[1]
        Parking_loc[k1]=k2
        print("\n")
        print(Parking_loc)
        client.publish("Parking.message/pub",str("You can park your vehicle at: "+str(b[1])))


    #if message.topic=="toAddSubCar":
     #   toApend=(message.payload).decode()
      #  client.subscribe(toApend+"location/sub")
        
         
    if message.topic=="location/sub" or message.topic=="location/sub55" or message.topic=="location/sub3": 
        Choice_number=Received.split(',')
        ch=Choice_number[0]
        value=Choice_number[1] 
        
        if(int(ch)==1):
            print("\n")
            print(Parking_loc)
            if(len(Parking_loc)<=size):#check if 20 parking space is filled or not(Parking_loc=Dictionary)
                free_space.clear()
                for val in Parking_loc.values():#find the value in dictionary
                    Parking_space_occupied[int(val)]=1 
           
                #print(Parking_space_occupied)
                for j in range(1,21):
                	if Parking_space_occupied[j] == 0:
                		free_space.append(j)		
                client.publish("free.space/pub",str("Available free parking space are: "+str(free_space)))
        	    
            else:
                #print("No parking space available")
                client.publish("location/pub",str("No Parking space is available"))

        elif(int(ch)==2 and message.topic=="location/sub55"):
            location_val.clear()
            for key, val in Parking_loc.items():
                if key.endswith(value):
                    location_val.append(val)
            if len(location_val)==0:
            	client.publish("carlocation/pub",str("Your car is not parked here."))
            else:
                loc_val_str=str(location_val)
                client.publish("carlocation/pub", str("Location of car is: "+loc_val_str))
            
        elif(int(ch)==3):
            if value in Parking_loc:
                del Parking_loc[(value)]   
                print("\nDeleted car number is: "+str(value))
                print("Dictionary After Deleting above car number details is: ")
                print(Parking_loc)
                client.publish("location/pub",str("Thank You for using our system, Happy Journey!!"+value))
            else:
                client.publish("location/pub",str("Incorrect car number")) 
            

    #time.sleep(2)


Connected = False  # global variable for the state of the connection
client_name="pub"
broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port
#curr=location_generator()

client = mqttClient.Client(client_name)  # create new instance


client.on_connect = on_connect  # attach function to callback
client.on_message = on_message
client.connect(broker_address, port=port)  # connect to broker

client.loop_start()  # start the loop



client.subscribe("free.space2/pub")
client.subscribe("location/sub55")
client.subscribe("location/sub3")
client.subscribe("location/sub")
while Connected != True:  # Wait for connection
    time.sleep(0.1)


try:
    while True:
        #client.publish("location/pub",str("Hi"))
        time.sleep(2)
        #curr=location_generator()

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
