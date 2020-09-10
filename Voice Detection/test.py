import pandas as pd

coordinates_file = "audios/Coordinates.csv"

my_csv = pd.read_csv(coordinates_file)
times_video = list(my_csv['Time in ms'])
times_video = list((int(times_video[i]) for i in range(len(times_video))))

print(times_video)