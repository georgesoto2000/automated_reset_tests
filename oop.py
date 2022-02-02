import time



class STB:
    #class atributes
    test_system="George's automation framework"

    def __init__(self, IP, smartplug, mac_address, vnc_port,camera):
        self.IP=IP
        self.smartplug=smartplug
        self.mac_address=mac_address
        self.vnc_port=vnc_port
        self.camera=camera

    def capture(self): #Takes a capture through USB capture card
        capture_card = cv.VideoCapture(self.camera)
        capture_card.set(cv.CAP_PROP_FRAME_WIDTH, 1920) #Takes capture in 1080p
        capture_card.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        return_value, image = capture_card.read() #Opens capture card in read mode
        cv.imwrite('capture.png', image) #Saves image to capture.png file
        del(capture_card) #removes capture device
        if return_value==False: #return_value variable is false if capture card fails to open
            print("failed to open capture device") #prints error

    def test(self, search): #Takes a capture and checks the image for the 'search' string
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
    def press(self,string):
        with open('sky-remote.js','w+') as file:
            js="""var net = require('net');

function SkyRemote(host, port) {

    var that = this;
    this.connectTimeout = 1000;

    function sendCommand(code, cb) {
        var commandBytes = [4,1,0,0,0,0, Math.floor(224 + (code/16)), code % 16];

        var client = net.connect({
            host: host,
            port: port || 49160
        });

        var l = 12;
        client.on('data', function(data) {
            clearTimeout(connectTimeoutTimer)
            // Clear timeout
            if (data.length < 24) {
                client.write(data.slice(0, l))
                l = 1;
            } else {
                client.write(new Buffer(commandBytes), function() {
                    commandBytes[1]=0;
                    client.write(new Buffer(commandBytes), function() {
                        client.destroy();
                        cb(null)
                    });
                });
            }
        });

        client.on('error', function(err) {
            clearTimeout(connectTimeoutTimer)
            cb(err)
        })

        var connectTimeoutTimer = setTimeout(function() {
            client.end()
            var err = new Error('connect timeout '+host+':'+port)
            err.name = 'ECONNTIMEOUT'
            err.address = host
            err.port = port
            cb(err)
        }, that.connectTimeout)
    }

    this.press = function press(sequence, cb) {
        if (typeof sequence !== 'object' || !sequence.hasOwnProperty('length')) {
            return press(sequence.split(','), cb)
        };
        sendCommand(SkyRemote.commands[sequence.shift()],function(err) {
            if (sequence.length) {
                setTimeout(function() {
                    press(sequence, cb);
                },500);
            } else {
                if (typeof cb === 'function') {
                    cb(err);
                }
            }
        });
    }

}


SkyRemote.SKY_Q = """+self.vnc_port+';\n'+"""SkyRemote.commands = {
    power: 0,
    select: 1,
    backup: 2,
    dismiss: 2,
    channelup: 6,
    channeldown: 7,
    interactive: 8,
    sidebar: 8,
    help: 9,
    services: 10,
    search: 10,
    tvguide: 11,
    home: 11,
    i: 14,
    text: 15,
    up: 16,
    down: 17,
    left: 18,
    right: 19,
    red: 32,
    green: 33,
    yellow: 34,
    blue: 35,
    0: 48,
    1: 49,
    2: 50,
    3: 51,
    4: 52,
    5: 53,
    6: 54,
    7: 55,
    8: 56,
    9: 57,
    play: 64,
    pause: 65,
    stop: 66,
    record: 67,
    fastforward: 69,
    rewind: 71,
    boxoffice: 240,
    sky: 241
}

module.exports = SkyRemote;"""
            file.write(js)
            file.close
            string=string.split()
            n=0
            for command in string: #writes each command into js file and executes
                        filename=str(n)+".js"
                        f1 = open(filename,"w+")
                        f1.write("var SkyRemote = require('sky-remote');\nvar RCU = new SkyRemote('"+self.IP+"');\n")
                        f1.write("RCU.press('"+command+"');")
                        f1.flush()
                        f1.close()
                        js_call=str("node "+str(n)+".js")
                        #os.system(js_call)
                        n=n+1
                        #os.remove(filename)
                        time.sleep(1)
            
        
