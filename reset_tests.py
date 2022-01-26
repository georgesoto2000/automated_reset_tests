#automating tests and setting

#functions
import numpy as np
import os, time, string
from pyHS100 import SmartPlug, Discover
from datetime import datetime
from types import NoneType
import cv2 as cv
from PIL import Image, ImageGrab
import pytesseract as tess
import string
import requests
from telnetlib import Telnet
tess.pytesseract.tesseract_cmd = r'C:\Users\gst63\Documents\projects\OCR\tess\tesseract.exe'


#Change AV settings

def set_200ms_optical_delay(): #Uses API call to set optical delay to 200ms
    data= {
        "OpticalAudioDelay": 200
    }
    url="http://"+IP+":9005/as/audio/setting/OpticalAudioDelay"
    file=requests.post(url,json=data, params=None)

def set_200ms_HDMI_delay(): #Uses API call to set HDMI delay to 200ms
    data= {
        "HDMIAudioDelay": 200
    }
    url="http://"+IP+":9005/as/audio/setting/HDMIAudioDelay"
    file=requests.post(url,json=data, params=None)
    
def HDMI_DD(): #Uses API call to set HDMI audio mode to Dolby Digital
    data= {
        "HDMIAudioFormat": "Dolby Digital"
    }
    url="http://"+IP+":9005/as/audio/setting/HDMIAudioFormat"
    file=requests.post(url,json=data, params=None)
    
def HDMI_PCM(): #Uses API call to set HDMI audio mode to stereo
    data= {
        "HDMIAudioFormat": "Normal"
    }
    url="http://"+IP+":9005/as/audio/setting/HDMIAudioFormat"
    file=requests.post(url,json=data, params=None) 

def OPTICAL_PCM(): #Uses API call to set optical audio mode to stereo
    data= {
        "OpticalAudioFormat": "Normal"
    }
    url="http://"+IP+":9005/as/audio/setting/OpticalAudioFormat"
    file=requests.post(url,json=data, params=None) 

def OPTICAL_DD(): #Uses API call to set Optical audio mode to Dolby Digital
    data= {
        "OpticalAudioFormat": "Dolby Digital"
    }
    url="http://"+IP+":9005/as/audio/setting/OpticalAudioFormat"
    file=requests.post(url,json=data, params=None) 

def set_576p(): #Uses API call to set resolution to 576p
    url="http://"+IP+":9005/as/display/setting/resolution"
    data={
        "resolution": "576p"
    }
    file=requests.post(url,json=data)

def set_720p(): #Uses API call to set resolution to 720p
    url="http://"+IP+":9005/as/display/setting/resolution"
    data={
        "resolution": "720p"
    }
    file=requests.post(url,json=data)

def set_1080i(): #Uses API call to set resolution to 1080i
    url="http://"+IP+":9005/as/display/setting/resolution"
    data={
        "resolution": "1080i"
    }
    file=requests.post(url,json=data) 

def set_1080p(): #Uses API call to set resolution to 1080p
    url="http://"+IP+":9005/as/display/setting/resolution"
    data={
        "resolution": "1080p"
    }
    file=requests.post(url,json=data)

def get_audio():##Uses API call to get current audio settings
    url="http://"+IP+":9005/as/audio"
    file=requests.get(url, data=None, params=None)
    file=file.json()
    file=str(file)
    return file

def get_resolution(): #Uses API call to get the current resolution
    url="http://"+IP+":9005/as/display"
    file=requests.get(url)
    file=file.json()
    file=str(file)
    return file


#settings menus and changes

def secret_menu(): #open engineering menu through EPG
    send_command("home down down down down down down down down down down down 0 0 1 select")

def audio_visual_menu(): #open audio visual menu
    send_command("home down down down down down down down down down down down select down down down down select down down down select") 

def turn_on_wireless(): #Turn on 2.4GHz an 5GHz wireless ports
    secret_menu()
    send_command("down")
    if test("On") ==False: #Checks On Screen Menu (OSM) for string 'On', checking if wireless ports are on
        send_command("right select down select down down select") #if ports are off ('On' not found in OSM), turns wireless off through EPG
        time.sleep(10)

def turn_off_wireless():
    secret_menu()
    send_command("down select")
    if test("Off")==False:#Checks On Screen Menu (OSM) for string 'Off', checking if wireless ports are off
        send_command("right select down select down down select") #if ports are on ('Off' not found in OSM), turns wireless on through EPG
        time.sleep(10)

def disk_reset(): #Performs a HDD reset through the EPG and wakes STB after its been performed
    secret_menu()
    send_command("down down right down select left select")  
    time.sleep(180)
    send_command("home home home")  

def factory_reset(): #Performs a factory reset through the EPG and wakes STB after its been performed
    secret_menu()
    send_command("down down right down down select left select")
    time.sleep(300)
    send_command("home home home")
    
def settings_reset(): #Performs a settings reset through the EPG and wakes STB after its been performed
    secret_menu()
    send_command("down down right select left select") 
    time.sleep(180)
    send_command("home home home")   
  
def transponder_change(): #Changes tuner frequency through EPG
    secret_menu()
    send_command("down down down right select 1 2 5 5 5 select down down down down down down down select")
    time.sleep(1)

def transponder_reset(): #reverts tuner frequency to default
    secret_menu()
    send_command("down down down right down down down down down down down down select")  

def set_wb(): #Sets LNB type to wideband through EPG
    secret_menu()
    send_command("select select right up select")

def set_scr(): #Sets LNB typeto SCR through EPG
    secret_menu()
    send_command("select right right right select")
    time.sleep(2)
    send_command("down select")

def recordings_menu(): #Opens recordings menu tab
    send_command("home down down") 

def setup_recording(): #set two recordings up on HDD
    send_command("home down right right right record down record") 

#Test functions

def capture(): #Takes a capture through USB capture card
    capture_card = cv.VideoCapture(1)
    capture_card.set(cv.CAP_PROP_FRAME_WIDTH, 1920) #Takes capture in 1080p
    capture_card.set(cv.CAP_PROP_FRAME_HEIGHT, 1080) 
    return_value, image = capture_card.read() #Opens capture card in read mode
    cv.imwrite('capture.png', image) #Saves image to capture.png file
    del(capture_card) #removes capture device
    if return_value==False: #return_value variable is false if capture card fails to open
        print("failed to open capture device") #prints error

def test(search): #Takes a capture and checks the image for the 'search' string
        capture()
        capture()
        text=tess.image_to_string(Image.open('capture.png')) #extracts string from image
        text=text.split() 
        search=search.split()
        matches=0
        words=len(search)
        for word in search: #Looks for each word, in search, within image_to_string
            for i in text:
                if i==word:
                    matches=matches+1
                    break
        if matches==words: #if all the words in search are found, returns true
            return True
        else:
            return False

def powercycle(): #powercycles STB using HS100 smartplug
    plug=SmartPlug(smartIP)
    try:
        plug.turn_on()
        time.sleep(1)
        plug.turn_off()
        time.sleep(1)
        plug.turn_on()
        time.sleep(140) #waits for STB to reboot
        send_command("home home home home") #wakes STB
        return 0
    except:
        print('error connecting')
        return 1
      
def send_command(string): #emulates RCU presses through Node.js moule sky-remote
    string=string.split()
    n=0
    for command in string: #writes each command into js file and executes
            filename=str(n)+".js"
            f1 = open(filename,"w+")
            f1.write("var SkyRemote = require('sky-remote');\nvar RCU = new SkyRemote('"+IP+"');\n")
            f1.write("RCU.press('"+command+"');")
            f1.flush()
            f1.close()
            js_call=str("node "+str(n)+".js")
            os.system(js_call)
            n=n+1
            os.remove(filename)
            time.sleep(1)
#Tests

def DEFAULT_TRANSPONDER(): #Performs Default Transponder test
    transponder_change() #changes frequency of tuner
    powercycle() #powercycles STB to enact settings change
    count=0
    while count<10: #continually check OSM for 'No satellite signal' message for 50s
        send_command("backup home") #refresh menu
        time.sleep(5)
        count=count+1
        results=test('satellite')
        if results==False: #if no NSS error appears, breaks
            break 
    transponder_reset() #reverts tuner frequency
    powercycle() #powercycles STB to enact settings changes
    f=open("test_report.txt", "a")
    if results==False: #if NSS menu doesn't appear, write test has failed to report
        f.write("Default Transponder: Failed\n")
    if results==True: #if NSS menu does appear, write test has passed to report
        f.write("Default Transponder: Passed\n")
    f.flush()
    f.close()

def FACTORY_RESET(): 
    f=open("test_report.txt", "a")
    send_command("home home home")
    setup_recording() #add recordings to HDD
    set_200ms_HDMI_delay() #change AV settings from default
    set_200ms_optical_delay()
    HDMI_DD()
    OPTICAL_PCM()
    set_1080p() 
    set_scr() #set LNB to SCR
    factory_reset() #perform factory reset
    send_command("backup home")
    time.sleep(5)
    if not test("satellite"): #LNB type should revert to wideband, so there shouldn't be a 'No satellite signal' OSM
        f.write("SCR Factory Reset: Passed\n")
    else:
        f.write("SCR Factory Reset: Failed\n")  #Fail test if OSM appears
        set_wb() #changes back to wideband LNB
        time.sleep(5)
        powercycle() #powercycles to enact change
    recordings_menu()  #open recordings menu
    if test("downloads.") and get_audio()==default_audio and get_resolution()==default_resolution: #checks audio settings and resolutions revert to default, and that recordings tray is empty checking for "No recordings or downloads." OSM to appear
        f.write("Factory reset: Passed\n") #Pass if settings revert to default and recordings menu empty
    else:
        f.write("Factory reset: Failed\n")#fail if settings don't revert or recordings tray not empty
    f.flush()
    f.close() 

def NVRAM_RESET(): 
    f=open("test_report.txt", "a") #opens test report
    send_command("home home home")
    setup_recording() #adds recordings to HDD
    set_200ms_HDMI_delay() #changes AVsettings from default
    set_200ms_optical_delay()
    HDMI_DD()
    OPTICAL_PCM()
    set_1080p()
    set_scr() #sets LNB type to SCR
    settings_reset() #perform settings reset
    send_command("backup home")
    time.sleep(5)
    if not test("satellite"): #check for 'No satellite signa' message, should not appear as LNB should have reverted to wideband
        f.write("SCR Settings Reset: Passed\n")
    else:
        f.write("SCR Settings Reset: Failed\n") #if LNB fails to revert, manually sets to wideband
        set_wb()
        time.sleep(5)
        powercycle()   
    recordings_menu() #accesses recordings menu
    if ((not test("downloads.")) and get_audio()==default_audio and get_resolution()==default_resolution): #recordings menu shouldn't be empty (so no "No recordings or downloads." OSM), AV settings should revert to defaults
        f.write("Settings reset: Passed\nSave Settings: Passed\n")
    else:
        f.write("Settings reset: Failed\nSave Settings: Failed\n")
    f.flush()
    f.close() 

def HARD_DISK_RESET(): 
    f=open("test_report.txt", "a") #opens test report
    send_command("home home home") 
    setup_recording() 
    HDMI_DD() #change AV settings from default
    OPTICAL_PCM()
    set_1080p()
    set_200ms_HDMI_delay()
    set_200ms_optical_delay()
    set_scr() #set LNB to SCR
    res=get_resolution() #saves current AV settings
    audio=get_audio()
    disk_reset() #perform disk reset
    time.sleep(5)
    send_command("backup home")
    time.sleep(5)
    if test("satellite"): #LNB should stay set SCR to SCR so 'No satellite signal' OSM should appear
        f.write("SCR Hard Disk Reset: Passed\n") #pass if OSM appears
        f.write("LNB set to SCR with WB feeds: Passed\n")
    else:
        f.write("SCR Hard Disk Reset: Failed\n") #fail if OSM doesn't appear
        f.write("LNB set to SCR with WB feeds: Failed\n") 
    set_wb() #revert to wb to view recordings tab
    powercycle()
    recordings_menu()
    if (test("You have no recordings or downloads.") and get_audio()==audio and get_resolution()==res): #recordings menu should be empty so "no recordings or downloads." OSM, AV settings should be the same as before reset
        f.write("Hard Disk reset: Passed\n")
    else:
        f.write("Hard Disk reset: Failed\n")
    f.flush()
    f.close() 


def open_report(): #opens a new test report with current time
    f=open("test_report.txt", "w+")
    f.write("Automated tests results ")
    f.write(str(datetime.now()))
    f.write("\n")
    f.flush()
    f.close




#main 
#os.system("npm install sky-remote") 
default_audio=str("{'DolbyDigitalPlusDecodeCapable': False, 'HDMIAudioDelay': 0, 'HDMIAudioFormat': {'current': 'Normal', 'options': ['Normal', 'Dolby Digital']}, 'OpticalAudioDelay': 0, 'OpticalAudioFormat': {'current': 'Dolby Digital', 'options': ['Normal', 'Dolby Digital']}}")
default_resolution=str("{'resolution': {'current': '1080i', 'options': ['576p', '720p', '1080i', '1080p']}}")

IP = input("Enter the IP address of the STB")
smartIP = input("enter ip address of smart plug")
open_report()



#Sanity Tests

DEFAULT_TRANSPONDER()
time.sleep(60)
HARD_DISK_RESET() 
time.sleep(60)
NVRAM_RESET() 
time.sleep(60)
FACTORY_RESET()
time.sleep(60)


