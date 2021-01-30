"""
Clear multiple lines of the same vad and pack them to one line.
"""

import numpy as np
import csv

file = "segment_2_corrected"
vad = []
fr = []
to = []

vad2 = []
fr2 = []
to2 = []

with open(file + ".csv", 'r', newline='') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    vad.append(row[0])
    fr.append(row[1])
    to.append(row[2])
    
i = 0
while i < len(vad):
  try:
    if vad[i] == vad[i+1]:
      vad.pop(i+1)
      to[i] = to[i+1]
      fr.pop(i+1)
      to.pop(i+1)
    else:
      i += 1

    if to[i] == to[-1]:
        break
  except IndexError:
    print("IndexError at index " + str(i))
    break


with open(file + "_cleared.csv", 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(["label", "start (s)", "end (s)"])
  for i in range(len(vad)):
    writer.writerow([vad[i], fr[i], to[i]])


