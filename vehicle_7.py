from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import sched,time
import os
import threading
from geopy.distance import geodesic
import socket
from datetime import datetime, timedelta
import json

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-cbac1ba8-84b2-469d-a59b-7d66d9b4cb2a'
pnconfig.subscribe_key = 'sub-c-88b6488e-3adb-11eb-b6eb-96faa39b9528'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

accidentDataPostResponse = None

class PostAccidentSignalData:
    def __init__(self, rsuId, accidentLongitude, accidentLatitude, accidentVehicleId):
        self.rsuId = rsuId
        self.accidentLongitude = accidentLongitude
        self.accidentLatitude = accidentLatitude
        self.accidentVehicleId = accidentVehicleId

class FetchAccidentSignalData:
    def __init__(self, timestamp, rsuId, accidentLongitude, accidentLatitude, accidentVehicleId):
        self.timestamp = timestamp        
        self.rsuId = rsuId
        self.accidentLongitude = accidentLongitude
        self.accidentLatitude = accidentLatitude
        self.accidentVehicleId = accidentVehicleId

def storeAccidentData(message):
    accidentDataFetched = []
    if "body" in message:
        output = message['body']
        print(output)
        for acccidentSignal in output:
            timestamp = acccidentSignal['timeStamp']
            date_time_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            if abs(datetime.now() - date_time_obj) < timedelta(minutes=200):
                accidentDataFetched.append(acccidentSignal)
            print("******")
        return accidentDataFetched
    else:
        return accidentDataFetched



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
        if message.message == None:
            continue_moving()
        else:
            print("From RSU-1 : ",message.message)
            continue_moving(message.message)


#RSU 1 Lattitude
RSU_coords = [53.372776, -6.239909]
accidentSignalData1 = PostAccidentSignalData("X", "Vehicle-1", "-6.239719", "53.372867")
vehicle_7_start_coords = [53.373863, -6.243059]
vehicle_7_stop_coords = [53.371403, -6.235603]

def continue_moving(message):
    accidentDataFetched = storeAccidentData(message)
    print(accidentDataFetched)
    pubnub.unsubscribe().channels("RSU-1").execute()
    if(checkAccidentDistance(accidentDataFetched) & len(accidentDataFetched) > 0):
        changeLanes(accidentDataFetched)
    else:
        while(vehicle_7_start_coords[0] >= vehicle_7_stop_coords[0] and vehicle_7_start_coords[1] <= vehicle_7_stop_coords[1]):
            vehicle_7_start_coords[0] = round((vehicle_7_start_coords[0] - 0.0005),6)
            vehicle_7_start_coords[1] = round((vehicle_7_start_coords[1] + 0.0005),6)
            print("Current Coordinates", vehicle_7_start_coords[0],vehicle_7_start_coords[1])
            # time.sleep(1)
        print("Vehicle-7 reached destination ! ")

def checkAccidentDistance(accidentDataFetched):
    print("Checking if route change is needed on the basis of accident location !")
    accidentCount = len(accidentDataFetched)
    print(accidentCount, "accidents detected ! ")
    vehicle_lane_change_coords = []
    arrayCounter = 0
    for accidentLoc in accidentDataFetched:
        print("Accident detected at ", accidentLoc['accidentLongitude'] + ", " +accidentLoc['accidentLatitude'])
        vehicle_lane_change_coords.append([accidentLoc['accidentLongitude'], accidentLoc['accidentLatitude']])
        distanceToAccident = geodesic([vehicle_7_start_coords[0],vehicle_7_start_coords[1]],[accidentLoc['accidentLongitude'], accidentLoc['accidentLatitude']]).m        
        print("Distance to Accident Spot (metres): ",distanceToAccident)
        if distanceToAccident < 10:
            # Adding 10 metres for vehicle 7 
            print("Need to change route !")
            return True
    print("No need to change routes as this vehicle is moving in other direction !")
    return False


def changeLanes(accidentDataFetched):
    accidentCount = len(accidentDataFetched)
    print(accidentCount, "accidents detected ! ")
    vehicle_lane_change_coords = []
    arrayCounter = 0
    for accidentLoc in accidentDataFetched:
        vehicle_lane_change_coords.append([accidentLoc['accidentLongitude'], accidentLoc['accidentLatitude']])
    print(vehicle_7_start_coords)
    print(vehicle_7_stop_coords)
    while(vehicle_7_start_coords[0] >= vehicle_7_stop_coords[0] and vehicle_7_start_coords[1] <= vehicle_7_stop_coords[1]):
            vehicle_7_start_coords[0] = round((vehicle_7_start_coords[0] - 0.00001),6)
            vehicle_7_start_coords[1] = round((vehicle_7_start_coords[1] + 0.00001),6)
            print("Current Coordinates", vehicle_7_start_coords[0],vehicle_7_start_coords[1])
            time.sleep(1)


def moving_vehicle():
    while((geodesic(vehicle_7_start_coords,RSU_coords).m) > 15):
        print("Distance to RSU-1 (metres): ",geodesic(vehicle_7_start_coords,RSU_coords).m)
        time.sleep(1)
        vehicle_7_start_coords[0] = round((vehicle_7_start_coords[0] - 0.000123),6)
        vehicle_7_start_coords[1] = round((vehicle_7_start_coords[1] + 0.0003728),6)
        print("Current Coordinates", vehicle_7_start_coords[0],vehicle_7_start_coords[1])
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("RSU-1").execute()
    pubnub.publish().channel("RSU-1").message({
      "rsuId": accidentSignalData1.rsuId,
      "accidentVehicleId": accidentSignalData1.accidentVehicleId,
      "accidentLongitude": accidentSignalData1.accidentLongitude,
      "accidentLatitude": accidentSignalData1.accidentLatitude
    }).pn_async(my_publish_callback)
moving_vehicle()
