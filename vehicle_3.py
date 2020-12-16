from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sched,time
import os
import threading
from geopy.distance import geodesic
import socket


pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-cbac1ba8-84b2-469d-a59b-7d66d9b4cb2a'
pnconfig.subscribe_key = 'sub-c-88b6488e-3adb-11eb-b6eb-96faa39b9528'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
   # Check whether request successfully completed or not
    if not status.is_error():
        pass
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        print("From Parking Slot: ",message.message)
        if(message.message == "EMPTY"):
            towards_parking()
        if(message.message == "OCCUPIED"):
            away_from_parking()
        if(message.message == "Currently_Occupied"):
            print("Changing the parking Status to Occupied")
        

def my_publish_callback_1(envelope, status):
   # Check whether request successfully completed or not
    if not status.is_error():
        pass
class MySubscribeCallback1(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        print("Parking Slot is currently occupied")

#Parking Signal 3 coords
parking_coords = [53.3719403591678, -6.253026535629358]
vehicle_1_start_coords = [53.371586821586234, -6.253264784211931]
vehicle_1_stop_coords = (53.37246883770986, -6.252641672534433)



def towards_parking():
    print("Vehicle is moving towards Parking")
    pubnub.unsubscribe().channels("parking-3").execute()
    while(vehicle_1_start_coords[0] <= vehicle_1_stop_coords[0] and vehicle_1_start_coords[1] <= vehicle_1_stop_coords[1]):
        vehicle_1_start_coords[0] += 0.00001
        vehicle_1_start_coords[1] += 0.00001
        print("Current Coordinates", vehicle_1_start_coords[0],vehicle_1_start_coords[1])
        print("Distance to Parking (metres): ",geodesic(vehicle_1_start_coords,parking_coords).m)
        if((geodesic(vehicle_1_start_coords,parking_coords).m) < 25):
        	print("Vehicle at the Parking Area")
        	pubnub.add_listener(MySubscribeCallback1())
        	#pubnub.subscribe().channels("parking-3").execute()
        	pubnub.publish().channel("parking-3").message(str("Currently_Occupied")).pn_async(my_publish_callback_1)
        	pubnub.unsubscribe().channels("parking-3").execute()
        	break
        	
        time.sleep(1)
        
def away_from_parking():
    pubnub.unsubscribe().channels("parking-3").execute()
    print("Vehicle is moving away from Parking")
    for i in range(5):
    	vehicle_1_start_coords[0] += 0.00001
    	vehicle_1_start_coords[1] += 0.00001
    	print("Current Coordinates", vehicle_1_start_coords[0],vehicle_1_start_coords[1])
    	time.sleep(1)
    

def moving_vehicle():
    while((geodesic(vehicle_1_start_coords,parking_coords).m) > 38):
        print("Parking Area Co-ordinates: (3.3719403591678, -6.253026535629358)")
        print("Distance to Parking (metres): ",geodesic(vehicle_1_start_coords,parking_coords).m)
        time.sleep(1)
        vehicle_1_start_coords[0] += 0.00001
        vehicle_1_start_coords[1] += 0.00001
        print("Current Coordinates:\n", vehicle_1_start_coords[0],vehicle_1_start_coords[1])
    print("Checking for the parking slot availability")
        
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("parking-3").execute()


moving_vehicle()






