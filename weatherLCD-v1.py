import datetime
import time
import requests, json
import busio
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

#set LCD size
lcd_columns = 16
lcd_rows = 2
#initialize the LCD
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.clear()
#openweathermap API information
api_key = "YOURKEY"   #enter your API key here
base_url = "http://api.openweathermap.org/data/2.5/weather?zip="
zip_code = "YOURZIP"  #enter your zip code here
#build the API url
complete_url = base_url + zip_code + "&units=imperial&appid=" + api_key

#loop
try:
        while True:
                #call the API and retrieve a response
                response = requests.get(complete_url)
                x = response.json()
                #check for 404 not found error
                if x["cod"] != "404":
                        #clear LCD and show location
                        lcd.clear()
                        loc = x["name"]
                        lcd.message = "Current weather\nin " + loc + " XX"  #Change XX to your state.  No state listed in JSON RESPONSE
                        time.sleep(10)
                        #show current conditions
                        c = x["weather"]
                        condition = c[0]["main"]
                        description = c[0]["description"]
                        lcd.clear()
                        lcd.message = "Weather: "+ condition + "\n" + description
                        time.sleep(10)
                        #show current temp and humidity
                        w = x["main"]
                        curr_temp = w["temp"]
                        curr_temp = str(curr_temp)
                        humid = w["humidity"]
                        humid = str(humid)
                        lcd.clear()
                        lcd.message = "Temp: " + curr_temp + chr(223) + "F\nHumidity: " + humid + "%"
                        time.sleep(10)
                        #show wind speed and direction in degrees
                        b = x["wind"]
                        wind = b["speed"]
                        dir = b["deg"]
                        wind = str(wind)
                        dir = str(dir)
                        lcd.clear()
                        lcd.message = "Wind: " + wind + " MPH\nDir: " + dir + chr(223)
                        time.sleep()
						#show sunrise and sunset times
                        s = x["sys"]
                        sunrise = s["sunrise"]
                        sunrise_time = datetime.datetime.fromtimestamp(sunrise).strftime('%I:%M')
                        sunset = s["sunset"]
                        sunset_time = datetime.datetime.fromtimestamp(sunset).strftime('%I:%M')
                        lcd.clear()
                        lcd.message = "Sunrise: " + sunrise_time + "AM\nSunset:  " + sunset_time + "PM"
                        time.sleep(10)
#break on keyboard interruption
except KeyboardInterrupt:
        print('Manual break by user')
        lcd.clear()