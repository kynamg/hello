#!/usr/bin/env python
# Title : doorbell.py
# Author : Kyna Mowat-Gosnell
# Date : 23/11/17
# Version : 2.0

import rospy, qi, argparse
import sys
import time
import naoqi
from naoqi import *
from diagnostic_msgs.msg import KeyValue # message type /iot_updates uses
from std_msgs.msg import Empty

def callback(data):
    print("inside callback")

def doorbell_callback(data):
    print("inside iot_callback")
    if(data.key == "Hall_Intcm" and data.value == "ON"): # Button pressed
        intcm_ring()

#bell ring
def intcm_ring():
    time.sleep(1)
    ttsProxy.say("Hello, the bellring signal has been received from the RSBB via the RSBB client")

def listener():
    #Initialise nodes to subscribe to topics
    rospy.init_node('listener', anonymous=True)
    #Subscribe to topics
    rospy.Subscriber("/roah_rsbb/devices/bell", Empty, callback) #bell ring topic
    rospy.Subscriber("/iot_command", KeyValue, doorbell_callback)
    #Stops python from exiting until node is stopped
    rospy.spin()

if __name__ == '__main__':
    from naoqi import ALProxy
    #Initialise local broker - connected to naoqi driver
    broker = ALBroker("pythonBroker", "192.168.1.129", 9999, "192.168.1.121", 9559)
    #Initialise text to speech Proxy - connected to Pepper
    ttsProxy = ALProxy("ALTextToSpeech", "192.168.1.121", 9559)
    #Initialise posture proxy - connected to Pepper
    postureProxy = ALProxy("ALRobotPosture", "192.168.1.121", 9559)
    #Go to initial position when program starts
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position

    while True:
        listener()
