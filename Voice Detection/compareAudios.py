import exportTimetable
import os
import sys
import matplotlib.pyplot as plt
import numpy as np


def search_audios(folder, extension):
    """Searches for the audios in the folder

    :param folder: the folder to be searched
    :param extension: the extension
    :return: the paths of the audios
    """
    dir = os.path.join(os.path.dirname(__file__), folder)
    for file in os.listdir(dir):
        if file.endswith(extension):
            yield os.path.join(folder, file)


def compare_audios(args):
    folder = args[0]
    extension = args[1]
    startcorner = 0
    endcorner = -1
    paths = list(search_audios(folder, extension))
    plt.figure(str(startcorner/100) + ' - ' + str(endcorner/100))

    for i, audio in enumerate(paths):
        index = i + 1
        print(audio)

        for aggressiveness in range(4):
            is_speech = exportTimetable.export_timetable([aggressiveness, audio])
            times = list(0.01 * i for i in range(len(is_speech)))[startcorner:endcorner]
            is_speech = np.multiply(is_speech[startcorner:endcorner], 1)

            plt.subplot(4, len(paths), index)
            plt.subplots_adjust(left=0.01, right=0.99, bottom=0.03, top=0.98, wspace=0.05, hspace=0.3)
            plt.xticks(np.arange(times[0], times[-1], 1))
            plt.tick_params(axis='x', rotation=90, labelsize=6)
            plt.yticks([])
            plt.plot(times, is_speech, linewidth=0.5)
            filename = audio.replace(folder, '').replace('\\new ', 'A: ' + str(aggressiveness) + ' ').replace(extension, '')
            plt.title(filename, {'fontsize': 6})
            # plt.xlabel('Time')
            # plt.ylabel('is speech?')
            index = index + len(paths)

    plt.show()


if __name__ == '__main__':
    compare_audios(sys.argv[1:])
