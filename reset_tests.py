import sky
from datetime import datetime
import time
      
#Tests

def DEFAULT_TRANSPONDER(box,screen): #Performs Default Transponder test
    box.transponder_change() #changes frequency of tuner
    box.reboot() #powercycles STB to enact settings change
    count=0
    while count<10: #continually check OSM for 'No satellite signal' message for 50s
        box.press("backup home") #refresh menu
        time.sleep(5)
        count=count+1
        results=screen.test('satellite')
        if results==False: #if no NSS error appears, breaks
            break 
    box.transponder_reset() #reverts tuner frequency
    box.reboot() #powercycles STB to enact settings changes
    f=open("test_report.txt", "a")
    if results==False: #if NSS menu doesn't appear, write test has failed to report
        f.write("Default Transponder: Failed\n")
    if results==True: #if NSS menu does appear, write test has passed to report
        f.write("Default Transponder: Passed\n")
    f.flush()
    f.close()

def FACTORY_RESET(box,screen): 
    f=open("test_report.txt", "a")
    box.press("home home home")
    box.setup_recording() #add recordings to HDD
    box.set_200ms_HDMI_delay() #change AV settings from default
    box.set_200ms_optical_delay()
    box.HDMI_DD()
    box.OPTICAL_PCM()
    box.set_1080p() 
    box.set_scr() #set LNB to SCR
    box.wipediskandsettings() #perform factory reset
    box.press("backup home")
    time.sleep(5)
    if not screen.test("satellite"): #LNB type should revert to wideband, so there shouldn't be a 'No satellite signal' OSM
        f.write("SCR Factory Reset: Passed\n")
    else:
        f.write("SCR Factory Reset: Failed\n")  #Fail test if OSM appears
        box.set_wb() #changes back to wideband LNB
        time.sleep(1)
        box.reboot() #powercycles to enact change
    box.recordings_menu()  #open recordings menu
    if screen.test("downloads.") and box.get_audio()==default_audio and box.get_resolution()==default_resolution: #checks audio settings and resolutions revert to default, and that recordings tray is empty checking for "No recordings or downloads." OSM to appear
        f.write("Factory reset: Passed\n") #Pass if settings revert to default and recordings menu empty
    else:
        f.write("Factory reset: Failed\n")#fail if settings don't revert or recordings tray not empty
    f.flush()
    f.close() 

def NVRAM_RESET(box,screen): 
    f=open("test_report.txt", "a") #opens test report
    box.press("home home home")
    box.setup_recording() #adds recordings to HDD
    box.set_200ms_HDMI_delay() #changes AV settings from default
    box.set_200ms_optical_delay()
    box.HDMI_DD()
    box.OPTICAL_PCM()
    box.set_1080p()
    box.set_scr() #sets LNB type to SCR
    box.wipesettings() #perform settings reset
    box.press("backup home")
    time.sleep(5)
    if not screen.test("satellite"): #check for 'No satellite signa' message, should not appear as LNB should have reverted to wideband
        f.write("SCR Settings Reset: Passed\n")
    else:
        f.write("SCR Settings Reset: Failed\n") #if LNB fails to revert, manually sets to wideband
        box.set_wb()
        time.sleep(1)
        box.reboot()   
    box.recordings_menu() #accesses recordings menu
    if ((not screen.test("downloads.")) and box.get_audio()==default_audio and box.get_resolution()==default_resolution): #recordings menu shouldn't be empty (so no "No recordings or downloads." OSM), AV settings should revert to defaults
        f.write("Settings reset: Passed\nSave Settings: Passed\n")
    else:
        f.write("Settings reset: Failed\nSave Settings: Failed\n")
    f.flush()
    f.close() 

def HARD_DISK_RESET(box,screen): 
    f=open("test_report.txt", "a") #opens test report
    box.press("home home home") 
    box.setup_recording() 
    box.HDMI_DD() #change AV settings from default
    box.OPTICAL_PCM()
    box.set_1080p()
    box.set_200ms_HDMI_delay()
    box.set_200ms_optical_delay()
    box.set_scr() #set LNB to SCR
    res=box.get_resolution() #saves current AV settings
    audio=box.get_audio()
    box.wipedisk() #perform disk reset
    box.press("backup home")
    time.sleep(5)
    if screen.test("satellite"): #LNB should stay set SCR to SCR so 'No satellite signal' OSM should appear
        f.write("SCR Hard Disk Reset: Passed\n") #pass if OSM appears
        f.write("LNB set to SCR with WB feeds: Passed\n")
    else:
        f.write("SCR Hard Disk Reset: Failed\n") #fail if OSM doesn't appear
        f.write("LNB set to SCR with WB feeds: Failed\n") 
    box.set_wb() #revert to wb to view recordings tab
    box.reboot()
    box.recordings_menu()
    if (screen.test("You have no recordings or downloads.") and box.get_audio()==audio and box.get_resolution()==res): #recordings menu should be empty so "no recordings or downloads." OSM, AV settings should be the same as before reset
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


open_report()
xwing=sky.STB("192.168.1.101",49160)
card=sky.capturecard(1)
#Sanity Tests

DEFAULT_TRANSPONDER(xwing,card)
time.sleep(60)
HARD_DISK_RESET(xwing,card) 
time.sleep(60)
NVRAM_RESET(xwing,card) 
time.sleep(60)
FACTORY_RESET(xwing,card)
time.sleep(60)


