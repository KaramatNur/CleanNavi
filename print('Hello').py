

import requests
import smtplib
import googlemaps

### API key
api_file = open('/Users/karamatnurillaev/Desktop/CleanNavi/apikey.rtf', "r")
api_key = api_file.read()
api_file.close()

# Address of client
homeClient = input("Enter your home adress\n")

# Address of Truck (we will change this variable into live geolocation)
GarbageTruck = input("Enter a location of garbage truck\n") 

# base URL for distance matrix copied from Google Maps 

url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"
 
 # get response 
r = requests.get(url+"origins=" + homeClient + "&destinations=" + GarbageTruck + "&key=" + api_key) 

 #  return time as text and as seconds
 time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
 seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]

 #print the total travel time 
 print("\nThe total travel time from your home to garbage truck is ", time)