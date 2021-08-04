import urllib
import sys
import urllib.request
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import sys,os
import subprocess
from PIL import Image, ImageChops

old_album='none'
old_track='none'
options = Options() 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.headless=True
driver = webdriver.Chrome(options=options)
driver.get('http://192.168.1.106:8080/nowplaying.html')
driver.find_element_by_xpath('//button[normalize-space()="HiFiBerry"]').click()

try:
    while True:
        try:
            track  = driver.find_element_by_id('line1').text
            artist = driver.find_element_by_id('line2').text
            album = driver.find_element_by_id('line3').text
            #check if album has changed
            if old_album!= album:
                print('new album detected: getting art')
                print('Artist: ' + artist)
                print('Album: ' + album)
                img = driver.find_element_by_xpath('//*[@id="containerCoverImage"]/img')
                src = img.get_attribute('src')
                print('Art url: ' + src)
                # download the image
                urllib.request.urlretrieve(src, "/home/pi/roontomatrix/images/art.jpg")
                old_album=album
                print("image downloaded")
                #send image to the server
                
                pi = subprocess.Popen(["/home/pi/flaschen-taschen/client/send-image", "-g","64x64",
                                 "-h", "localhost", "/home/pi/roontomatrix/images/art.jpg"],
                                       stdout=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf8')
            if old_track!=track:
                #send now playing info
                #get inverted image dominant color
                img=Image.open('/home/pi/roontomatrix/images/art.jpg')
                width,height = img.size
                left=0
                top=3*height/4
                right=width
                bottom=height
                img=img.crop((left, top, right, bottom))
                img.resize((1,1), resample=0)
                img=ImageChops.invert(img)
                img.convert("RGB")
                dominant_color=img.getpixel((0,0))
                dominant_color='%02x%02x%02x' % dominant_color
                time.sleep(1)
                string=str(artist + " - " + track)
                pt=subprocess.Popen(["/home/pi/flaschen-taschen/client/send-text", string , "-g","64x12+0+54+1",
                                        "-h", "localhost", "-f", "/home/pi/flaschen-taschen/client/fonts/6x9.bdf", "-O",
                                         "-c", dominant_color],stdout=subprocess.PIPE,stdin=subprocess.PIPE,encoding='utf8')
                time.sleep(20)
                pt.terminate()
                old_track=track
                
        
        except:
            old_album='none'
except KeyboardInterrupt:
    print('Press Ctr-C to terminate getart.py')
    driver.close()
