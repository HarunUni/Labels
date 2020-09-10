FPS = 29.97002997002997
frame_count = 32785.0

oneFrame = (1 / FPS) * 1000
time_of_video = (frame_count / FPS) * 1000 - oneFrame

print(time_of_video)
