#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 20:32:47 2023

@author: sambarnhart
"""
import requests
import time



print("Hello")
adress = input("Enter Full Adress: ")
radius = input("Enter Radius: ")
t = time.time()

api_key = "682a8f9e5a3d4923a012def2aa6ae673"


def geocode(address, api_key):
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {"q": address, "key": api_key}
    response = requests.get(base_url, params=params)
    return response.json()

result = geocode("1600 Amphitheatre Parkway, Mountain View, CA", api_key)
# print(result)

latitude = result['results'][0]['geometry']['lat']
longitude = result['results'][0]['geometry']['lng']
#print(latitude, longitude)




from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles. use 6371 for kilometers. Determines return value units.
    return c * r





def generate_points(lat, lon, radius, step):
    points = []
    # Convert radius from kilometers to degrees
    try:
        radius_in_degrees = radius / 111.045
    except:
        radius_in_degrees = float(radius) / 111.045
        
    num_steps = int(radius_in_degrees / step)
    for i in range(-num_steps, num_steps + 1):
        for j in range(-num_steps, num_steps + 1):
            new_lat = lat + i * step
            new_lon = lon + j * step / cos(radians(lat))  # Adjust for latitude
            try:
                if haversine(lon, lat, new_lon, new_lat) <= radius:
                    points.append((new_lat, new_lon))
                    
            except:
                if haversine(lon, lat, new_lon, new_lat) <= float(radius):
                    points.append((new_lat, new_lon))
                    
    return points



pointslist = generate_points(latitude, longitude, radius, 0.01)


def get_elevation(lat, long):
    query = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{long}"
    r = requests.get(query).json() # Send the request to the API
    elevation = r['results'][0]['elevation'] # Parse the result

    return elevation


# Initialize highest elevation and corresponding point to none as a start
highest_elevation = None
highest_point = None

# Iterate over points and check their elevation
for point in pointslist:
    lat, lon = point
    elevation = get_elevation(lat, lon)
    #print(f"Elevation at {point} is {elevation} meters")

    # If this point has a higher elevation than the current highest, update the highest
    if highest_elevation is None or elevation > highest_elevation:
        highest_elevation = elevation
        highest_point = point

    # Respect API rate limits by sleeping, protects api
    time.sleep(1)

print(f"\nThe highest point is {highest_point} with an elevation of {highest_elevation} meters")
tf = time.time()
tt = tf - t
print("\nRun time: " + str(tt) + " seconds")
