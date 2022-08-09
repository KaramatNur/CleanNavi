# this code takes a track file (e.g. gpkg or .shp)
# and point data of 'clients' and another of 'truck locations'
# for the sake of demo.
# it works out the distance along the track between the 
# chosen client and current location of truck.
# returned is the distance to reach to client (in m or km)
# and also estimated time to reach there, based on a predefined 
# travel speed (variable 'speed')  
# if the truck already the passed the location of client
# the distance and remaining time (rem_time) is 0  

import geopandas as gpd
import shapely
from shapely.geometry import Point, LineString
import os

# configure our demo
choose_client = 1 # for demo, select one client from the 4 available
choose_time = 3 # for demo, select time (of truck along track: 0 - 5)
speed = 5 # assumed truck speed in m/s (more than 0)


# setup environment and data
os.chdir("C:/Users/user/Documents/CleanNavi/CleanNavi")
clients = gpd.read_file('example_data/example_clients.gpkg')
truck = gpd.read_file("example_data/example_truck.gpkg")
track = gpd.read_file("example_data/example_track_hokudai_4326.gpkg")


# transform to projected coordinate reference system (to have measurement in meters)
clients.to_crs(epsg = 32654, inplace = True)
truck.to_crs(epsg = 32654, inplace = True)
track.to_crs(epsg = 32654, inplace = True)

## setup location and track, as recieved by distance function.
client_location = clients.at[choose_client,'geometry']
truck_location = truck.at[choose_time,'geometry']
track_linestring = track.at[0,'geometry'].geoms[0]


## functions to cut linestring between points. functions from stackEx 
def cut(line, distance):
    # Cuts a line in two at a distance from its starting point
    # This is taken from shapely manual
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]

def split_line_with_points(line, points):
    """Splits a line string in several segments considering a list of points.

    The points used to cut the line are assumed to be in the line string 
    and given in the order of appearance they have in the line string.

    >>> line = LineString( [(1,2), (8,7), (4,5), (2,4), (4,7), (8,5), (9,18), 
    ...        (1,2),(12,7),(4,5),(6,5),(4,9)] )
    >>> points = [Point(2,4), Point(9,18), Point(6,5)]
    >>> [str(s) for s in split_line_with_points(line, points)]
    ['LINESTRING (1 2, 8 7, 4 5, 2 4)', 'LINESTRING (2 4, 4 7, 8 5, 9 18)', 'LINESTRING (9 18, 1 2, 12 7, 4 5, 6 5)', 'LINESTRING (6 5, 4 9)']

    """
    segments = []
    current_line = line
    for p in points:
        d = current_line.project(p)
        seg, current_line = cut(current_line, d)
        segments.append(seg)
    segments.append(current_line)
    return segments

## our remaining distance function:
def remaining_dist(origin,dest,path):
    #nearest_origin = shapely.ops.nearest_points(path,origin)
    #nearest_dest = shapely.ops.nearest_points(path,dest) 

    # is it already past?
    d1 = path.project(origin)
    d2 = path.project(dest)

    if d1 > d2: # if distance to truck is more than client address, the truck past client.
        return 0 
    else:
        split_line = split_line_with_points(line=path,points=[origin,dest])
        active_segment = split_line[1]
        return active_segment.length
    

distance = remaining_dist(origin=truck_location, dest=client_location,path=track_linestring)
rem_time = distance/speed


## variable to use in end:
distance_km = distance/1e3
rem_time_minutes = rem_time/60



 
