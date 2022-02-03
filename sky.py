import time, os, requests

import cv2 as cv
from PIL import Image
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\gst63\Documents\projects\OCR\tess\tesseract.exe'
from cv2 import VideoCapture

class STB: #STB class
    #class atributes
    requirements="Node.js required"
    DTH_VNC_port=49160
    SOIP_VNC_port=5800

    def __init__(self, IP, vnc_port): #initilise STB object with IP address of box and VNC port
        self.IP=IP
        self.vnc_port=vnc_port

    def press(self,string): #emulate remote with string of buton presses
        with open('sky-remote.js','r') as file: #rewrite VNC port on sky-remote module
            lines=file.readlines()
            lines[68]="SkyRemote.SKY_Q = "+str(self.vnc_port)+";"
        with open("sky-remote.js",'w') as file:
            file.writelines(lines)
        string=string.split()
        n=0
        for command in string: #for each command, write it into javascript file and execute it
            filename=str(n)+".js"
            f1 = open(filename,"w+")
            f1.write("var SkyRemote = require('sky-remote');\nvar RCU = new SkyRemote('"+self.IP+"');\n")
            f1.write("RCU.press('"+command+"');")
            f1.flush()
            f1.close()
            js_call=str("node "+str(n)+".js")
            os.system(js_call)
            os.remove(filename)
            n=n+1
            time.sleep(1)
    def HDMI_DD(self): #Set HDMI audio output to dolby digital with API call
        data= {
            "HDMIAudioFormat": "Dolby Digital"
        }
        url="http://"+self.IP+":9005/as/audio/setting/HDMIAudioFormat"
        requests.post(url,json=data, params=None)
    def HDMI_PCM(self):#Set HDMI audio output to stereo with API call
        data= {
            "HDMIAudioFormat": "Normal"
        }
        url="http://"+self.IP+":9005/as/audio/setting/HDMIAudioFormat"
        requests.post(url,json=data, params=None)    
    def OPTICAL_PCM(self):#Set optical audio output to stereo with API call
        data= {
            "OpticalAudioFormat": "Normal"
        }
        url="http://"+self.IP+":9005/as/audio/setting/OpticalAudioFormat"
        requests.post(url,json=data, params=None)    
    def OPTICAL_DD(self): #Set optical audio output to dolby digital with API call
        data= {
            "OpticalAudioFormat": "Dolby Digital"
        }
        url="http://"+self.IP+":9005/as/audio/setting/OpticalAudioFormat"
        requests.post(url,json=data, params=None)   
    def set_576p(self):#set resolution to 576p with API call
        url="http://"+self.IP+":9005/as/display/setting/resolution"
        data={
            "resolution": "576p"
        }
        requests.post(url,json=data)
    def set_720p(self): #set resolution to 720p with API call
        url="http://"+self.IP+":9005/as/display/setting/resolution"
        data={
            "resolution": "720p"
        }
        requests.post(url,json=data)
    def set_1080i(self):#set resolution to 1080i with API call
        url="http://"+self.IP+":9005/as/display/setting/resolution"
        data={
            "resolution": "1080i"
        }
        requests.post(url,json=data) 
    def set_1080p(self): #set resolution to 1080p with API call
        url="http://"+self.IP+":9005/as/display/setting/resolution"
        data={
            "resolution": "1080p"
        }
        requests.post(url,json=data)
    def get_audio(self): #gets current audio settings with API call
        url="http://"+self.IP+":9005/as/audio"
        file=requests.get(url, data=None, params=None)
        file=file.json()
        file=str(file)
        return file
    def get_resolution(self): #gets current resolution ith API call
        url="http://"+self.IP+":9005/as/display"
        file=requests.get(url)
        file=file.json()
        file=str(file)
        return file
    def wipedisk(self): #wipes hard disk with API call
        url="http://"+self.IP+":9005/as/system/action/reset?type=wipedisk"
        requests.post(url)
        time.sleep(200)
        self.press("home home home home")
    def wipesettings(self):#clears NVRAM with API call
        url="http://"+self.IP+":9005/as/system/action/reset?type=wipesettings"
        requests.post(url)
        time.sleep(200)
        self.press("home home home home")
    def wipediskandsettings(self):#factory reset with API call
        url="http://"+self.IP+":9005/as/system/action/reset?type=wipediskandsettings"
        requests.post(url)
        time.sleep(200)
        self.press("home home home home")
    def reboot(self):#reboots box with API call
        url="http://"+self.IP+":9005/as/system/action/reset?type=reboot"
        requests.post(url)
        time.sleep(140)
        self.press("home home home home")
    def set_200ms_optical_delay(self): #set optical audio delat to 200ms
        data= {
            "OpticalAudioDelay": 200
        }
        url="http://"+self.IP+":9005/as/audio/setting/OpticalAudioDelay"
        requests.post(url,json=data, params=None)

    def set_200ms_HDMI_delay(self): #set HDMI audio delay to 200ms
        data= {
            "HDMIAudioDelay": 200
        }
        url="http://"+self.IP+":9005/as/audio/setting/HDMIAudioDelay"
        requests.post(url,json=data, params=None)
    
    def secret_menu(self): #open engineering menu through EPG
        self.press("home down down down down down down down down down down down 0 0 1 select")
    
    def transponder_change(self): #Changes tuner frequency through EPG
        self.secret_menu()
        self.press("down down down right select 1 2 5 5 5 select down down down down down down down select")
        time.sleep(1)

    def transponder_reset(self): #reverts tuner frequency to default
        self.secret_menu()
        self.press("down down down right down down down down down down down down select")  

    def set_wb(self): #Sets LNB type to wideband through EPG
        self.secret_menu()
        self.press("select select right up select")

    def set_scr(self): #Sets LNB typeto SCR through EPG
        self.secret_menu()
        self.press("select right right right select")
        time.sleep(2)
        self.press("down select")

    def recordings_menu(self): #Opens recordings menu tab
        self.press("home down down") 

    def setup_recording(self): #set two recordings up on HDD
        self.press("home down right right right record down record") 

class capturecard(VideoCapture): #capturecard class
    requirements="Remove HDCP, attach magwell capture card, try different values for camera (0,1,2,3,4)"
    def __init__(self, camera):
        self.camera=camera
        self.card=VideoCapture(self.camera)
    def capture(self): #Takes a capture through USB capture card
        self.card.set(cv.CAP_PROP_FRAME_WIDTH, 1920) #Takes capture in 1080p
        self.card.set(cv.CAP_PROP_FRAME_HEIGHT, 1080) 
        return_value, image = self.card.read() #Opens capture card in read mode
        cv.imwrite('capture.png', image) #Saves image to capture.png file
        #del(capture_card) #removes capture device
        if return_value==False: #return_value variable is false if capture card fails to open
            print("failed to open capture device") #prints error
    def test(self,search): #Takes a capture and checks the image for the 'search' string
        self.capture()
        self.capture()
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

        
    

