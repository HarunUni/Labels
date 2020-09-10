import contextlib
import csv
import sys
import wave
import webrtcvad
import pandas as pd


class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.

    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.

    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = frame_duration_ms / 1000
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def write_timetable(is_speech, frame_duration, filename, aggressiveness, coordinates_file):
    """Writes the data in a timetable

    is_speech: the list of booleans whether the there is speech or not
    frame_duration: the duration of a frame
    filename: the name of the audiofile
    """

    "Reading the timetable of the video"
    my_csv = pd.read_csv(coordinates_file)
    times_video = list(my_csv['Time in ms'])
    times_video = list((int(times_video[i]) for i in range(len(times_video))))  # converting to integer

    "Calculate the timetable of the VAD"
    times_audio = list((frame_duration * i for i in range(len(is_speech))))

    times = []
    speech = []
    last_k = 0

    for i in range(len(times_video)):
        for k in range(last_k, len(times_audio)):

            if (times_video[i] - times_audio[k]) < frame_duration:

                if k < len(times_audio) - 1 and (times_video[i] - times_audio[k+1]) < (times_video[i] - times_audio[k]):
                        times.append(times_video[i])
                        speech.append(is_speech[k + 1])
                        last_k = k + 2

                else:
                    times.append(times_video[i])
                    speech.append(is_speech[k])
                    last_k = k + 1

                break

            else:
                continue


    with open(filename + ' Aggressiveness ' + str(aggressiveness) + ' speech_Detection.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        rows = zip(times, speech)
        writer.writerow(['Time in ms', 'Is Speech'])
        writer.writerows(rows)

    return times


def export_timetable(args):
    """Writes the timetable

    :return: the times and the list of Booleans whether there is speech or not
    """

    if len(args) != 3:
        sys.stderr.write('Usage: extractTimetable.py <aggressiveness> <path to wav file> <path to coordinates-file>\n'
                         'aggressiveness is an integer from 0 to 3')
        sys.exit(1)

    aggressiveness = int(args[0])
    wavefile = args[1]
    coordinates_file = args[2]

    audio, sample_rate = read_wave(wavefile)
    vad = webrtcvad.Vad(aggressiveness)
    frame_duration = 10  # ms
    frames = frame_generator(frame_duration, audio, sample_rate)

    is_speech = []
    for i, frame in enumerate(frames):
        is_speech.append(vad.is_speech(frame.bytes, sample_rate))

    write_timetable(is_speech, frame_duration, wavefile, aggressiveness, coordinates_file)



    return is_speech


if __name__ == '__main__':
    export_timetable(sys.argv[1:])
