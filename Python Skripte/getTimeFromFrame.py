import sys


FPS = float(sys.argv[1])
frame = int(sys.argv[2])

seconds = frame / FPS
minutes = int(seconds/60)
milliseconds = int((seconds - int(seconds)) * 1000)
seconds = int(seconds) - minutes * 60

print("{:02d}".format(minutes) + ":" + "{:02d}".format(seconds) + ":" + "{:03d}".format(milliseconds))
