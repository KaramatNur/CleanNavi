# 




""" import requests
import smtplib
import googlemaps
import gpxpy
 """
import geopandas as gpd
import fiona
import numpy as np
import pandas
import csv
import os


choose_client = 2 # for demo, select one client from the 4 available
choose_time = 3 # for demo, select time (of truck along track: 0 - 5)


# setup
os.chdir("C:/Users/user/Documents/CleanNavi/CleanNavi")
clients = gpd.read_file('example_data/example_clients.gpkg')
truck = gpd.read_file("example_data/example_truck.gpkg")
track = gpd.read_file("example_data/example_track_hokudai_4326.gpkg")

# transform to projected coordinate reference system (to have measurement in meters)
clients.to_crs(epsg = 32654, inplace = True)
truck.to_crs(epsg = 32654, inplace = True)
track.to_crs(epsg = 32654, inplace = True)


clientLoc = clients.at[choose_client,'geometry']
truck_location = truck.at[choose_time,'geometry']

def remaining_dist(client,truck,track):




 
### API key
"""
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
 print("\nThe total travel time from your home to garbage truck is ", time) """
