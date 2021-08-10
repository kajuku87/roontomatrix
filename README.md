# roontomatrix

![alt text](https://github.com/kajuku87/roontomatrix/blob/main/sample.gif)

This code uses the adafruit hat and rgb screen to display the art of the current album and track information.
Main is the code you have to launch in your raspberry, you'll need a folder "images" inside the roontomatrix folder
loadserver.py loads the server for the hat. Check this first:https://github.com/hzeller/flaschen-taschen
getart.py 
downloads the art of the track from the roon web controller extension url http://192.168.1.106:8080/nowplaying.html (update the code with your local url)
