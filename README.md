README

Steps to execute various scenarios

1.	Run the automation script to install all the required dependencies on all PIs.
2.	Activate the venv RpiVanet, that was created by the script.

For Scenario-1 (Traffic Signal)

1.	Run signal_1.py 
2.	Once the signal_1 is up and running, continue to run vehicle_2.py. The vehicle would react according to the message received from the traffic signal.

For Scenario-2 (Parking)

1.	Run parking_3.py. 
2.	Once parking_3 is up, run vehicle_3.py. This will allow the vehicle to move towards parking, check for its status and occupy or move away from the parking slot.

For Scenario-3 (Vehicle-1 Meets with Accident, Vehicle-7 Sends Signal to RSU-1)

1.	Run vehicle_1.py
2.	This will emulate an accident scenario and the vehicle will be down.
3.	Run rsu_1.py.
4.	This will run the rsu, which continuously fetches data from the cloud.
5.	Run vehicle_7.py.
6.	Vehicle 7 moves towards the accident spot, reports this to the rsu_1, which in turn pushes this info to cloud using AWS Lambda. All others RSUs get this information as well.

For Scenario-4 (Vehicle-8 gets information from RSU-2, changes lanes)

1.	Run rsu_2.py. 
2.	It will continuously fetch information from the cloud. It will have received the message that was sent by rsu_1 about the accident to vehicle_1.
3.	Run vehicle_8.py
4.	Vehicle 8 moves towards RSU-2, upon reaching near it, RSU-2 transmits the signal regarding the accident.
5.	Vehicle 8 changes course of journey from the nearby junction and takes a turn.

For Scenario-5 (RSU-5 informs Ambulance of accident, Ambulance goes to accident spot)

1.	Run rsu_5.py
2.	This will continuously fetch information from the cloud. The accident that happened with vehicle 1 will be received here.
3.	Vehicle 10, which is nearby RSU-5 gets the signal, and moves towards the accident spot.

Communication with other pods

1.	Run rsu_4.py
2.	A drone from Team-3 will fly near one of our RSUs (RSU-4) and report an accident that took place on its path. 
3.	This accident information is also circulated among all our RSUs through the use of AWS lambdas. 
