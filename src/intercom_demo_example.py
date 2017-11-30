#!/usr/bin/env python
# Title : intercom_demo.py
# Author : Kyna Mowat-Gosnell
# Date : 09/10/17
# Version : 1.0

import rospy, qi, argparse
import sys
import time
import naoqi
from naoqi import *
from diagnostic_msgs.msg import KeyValue # message type /iot_updates uses
from std_msgs.msg import Empty

def callback(data):
	print("inside callback")

def iot_callback(data):
    if(data.key == "Hall_Intcm" and data.value == "ON"): # Button pressed
		intcm_ring()

def intcm_ring():
    tabletProxy.showImage("http://198.18.0.1/apps/dragone-51a938/Dragone.jpg")
    animatedProxy.say("Hello, your friend Mauro is at the door, you have agreed to go for a walk together this afternoon.")
    #ttsProxy.say("Someone just rang the doorbell")
    #tabletProxy.showWebview("http://192.168.1.99/jpg/image.jpg")
    time.sleep(5)
    animatedProxy.say("You're welcome.")
    time.sleep(5)
    tabletProxy.hideImage()
    #tabletProxy.hideWebview()

def listener():
    rospy.init_node('intcm_listener', anonymous=True) # initialise node to subscribe to topic
    rospy.Subscriber("/devices/bell", Empty, callback) # subscribe to topic /iot_updates
    rospy.Subscriber("/iot_updates", KeyValue, iot_callback)
    rospy.spin() # keeps python from exiting until node is stopped


if __name__ == '__main__':
    from naoqi import ALProxy
    # Create a local broker, connected to the remote naoqi
    broker = ALBroker("pythonBroker", "192.168.1.129", 9999, "pepper.local", 9559)
    animatedProxy = ALProxy("ALAnimatedSpeech", "pepper.local", 9559) # initialise animated speech proxy
    #ttsProxy = ALProxy("ALTextToSpeech", "pepper.local", 9559) # initialise text to speech proxy
    tabletProxy = ALProxy("ALTabletService", "pepper.local", 9559) # initialise tablet proxy
    tabletProxy.getWifiStatus()
    print tabletProxy.getWifiStatus()
    postureProxy = ALProxy("ALRobotPosture", "pepper.local", 9559) # initialise posture proxy
    postureProxy.goToPosture("StandInit", 0.5) # return to initial position

    while True:
        listener()
