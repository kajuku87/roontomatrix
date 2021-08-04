import subprocess
import time

process = subprocess.Popen(["/home/pi/flaschen-taschen/server/ft-server",
                 "--led-gpio-mapping","adafruit-hat-pwm",
                 "--led-slowdown-gpio","2", "--led-rows","64",
                 "--led-cols","64", "--led-brightness","50"],
                           stdout=subprocess.PIPE,
                           stdin=subprocess.PIPE,
                           encoding='utf8')