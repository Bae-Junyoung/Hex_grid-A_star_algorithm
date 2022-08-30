import hexgrid # han : pip install hexgrid-py
import morton
import numpy as np
from shapely.geometry import Point, Polygon
from hex_coordinate import *
import geopandas as gpd

_map = Polygon([[0,0], [5,0], [5,5], [0,5], [0,0]]) #

startX = np.min(_map.boundary.coords.xy[1])
endX = np.max(_map.boundary.coords.xy[1])
startY = np.min(_map.boundary.coords.xy[0])
endY = np.max(_map.boundary.coords.xy[0])

#-----------------return hex corner ---------------------
center=hexgrid.Point((float(startX)+float(endX))/2,(float(startY)+float(endY))/2)   #중앙
size = hexgrid.Point(10, 10)
grid = hexgrid.Grid(hexgrid.OrientationPointy, center, size, morton.Morton(2, 32))
sPoint=grid.hex_at(Point(float(startX),float(startY)))      # hex_at : point to hex -> 출발지 Point -> hex좌표
ePoint=grid.hex_at(Point(float(endX),float(endY)))          #목적지
map_size=max(abs(sPoint.q),abs(sPoint.r))   #열col(q) 행row(r)



neighbor=[]
neighbor =grid.hex_neighbors(grid.hex_at(center),map_size+0) #hex_neighbor : type(Hex, int) -> list
neighbor.append(hexgrid.Hex(0,0))

print("hexgrid 개수 : ",len(neighbor))
#test make hex to corner
cornerlist = []
for item in neighbor:
    cornerlist.append(grid.hex_corners(item))


polylist =[]
for hex in cornerlist:
    hexPolygon = []
    for corner in hex :
        temp = [corner.y , corner.x]
        hexPolygon.append(temp)

    polylist.append(hexPolygon)

print("hexgrid 꼭지점 개수 : ",len(polylist))

hex_line={"type":"Feature","geometry":{"type":"Polygon","coordinates":polylist}}
hex_polygon = {"type":"FeatureCollection","features":[hex_line]}

cube_coords = list(map(lambda x: qoffset_to_cube(1,x), neighbor))

hex_grid = gpd.GeoDataFrame({'offset':neighbor,'cube':cube_coords,'geometry':list(map(Polygon, polylist))}, crs='epsg:5186')
