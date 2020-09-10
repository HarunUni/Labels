import csv

with open("inputs/Info.csv", "r", newline='') as file:
    reader = csv.DictReader(file)

    for info in reader:
        frame_count = int(float(info['frame_count']))
        FPS = float(info['FPS'])

timetable = list((1 / FPS * 1000 * i for i in range(frame_count)))

with open("outputs/TimeTable.csv", "w", newline='') as file:

    writer = csv.writer(file)
    for row in timetable:
        writer.writerow([row])
