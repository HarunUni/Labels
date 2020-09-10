import csv
from readCoordinates import read_coordinates

h = "inputs1/Coordinates.csv"
l = "inputs1/Info.csv"
info, coordinates = read_coordinates(l, h)

print(coordinates)