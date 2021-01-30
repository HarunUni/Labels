"""Read the cutting_points file and cut the labels according to those."""

import pandas as pd
import sys
import os

cut_points_path = sys.argv[1]
labels_path = sys.argv[2]
dest_folder = sys.argv[3]

cut_points = pd.read_csv(cut_points_path)
labels = pd.read_csv(labels_path)

pts = cut_points['cutting_point (mm:ss)'].str.split(":", expand=True)
pts = (pts[0].astype(str).astype(int)*60 + pts[1].astype(str).astype(float))*1000 # ms
filt = [labels['Time in ms'] - pts[i] <= 0 for i in range(len(pts))]

labels[filt[0]].to_csv(os.path.join(dest_folder, 'segment_1.csv'))

for i in range(len(filt)-1, 0, -1):
    filt[i][filt[i-1]] = False
    labels[filt[i]].to_csv(os.path.join(dest_folder, 'segment_' + str(i+1) + '.csv'))


