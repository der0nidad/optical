**Readme**
1. How to build and run(ubuntu)

a. Sure that you have all package dependencies
```apt update && sudo apt install -y python3-dev python3-pip libjpeg-dev zlib1g-dev python-gst-1.0```
 
b. make venv, install all python dependencies and run
```
python3 -m venv venv
pip install -r requirements.txt
python MyGame.py
```