#!/bin/bash

echo Removing the virtual environment if already present...
rm -rf RpiVanet 

echo Setting up RpiVanet virtual environment...
python3 -m venv RpiVanet/

echo Activating the RpiVanet virtual environment...
source RpiVanet/bin/activate

echo Installing the required packages...
pip install twisted
pip install pubnub
pip install geopy
pip install pyp2p

echo Removing the code files if already present...
rm -rf VANETrpi4
echo Cloning code files from git...
git clone https://github.com/madaanp/VANETrpi4.git

echo Activating the RpiVanet virtual environment...
source RpiVanet/bin/activate

cd VANETrpi4