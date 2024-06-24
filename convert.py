#!/usr/bin/env python
# In[1]:
import collections

import pygame.midi
import pygame
from midi_file import songName

# In[3]:


import mido



# Load the MIDI file
midi_file = mido.MidiFile(songName)

# Print basic information about the MIDI file
print(f"File type: {midi_file.type}")
print(f"Number of tracks: {len(midi_file.tracks)}")
print(f"Ticks per beat: {midi_file.ticks_per_beat}")

# Print information about each track
for i, track in enumerate(midi_file.tracks):
    print(f"Track {i}: {track.name}")


# In[27]:
def midi_to_note_name(midi_number):
    # MIDI note numbers start at 0 (C-1) and go up to 127 (G9)
    note_names = ['C', 'C_sharp', 'D', 'D_sharp', 'E', 'F', 'F_sharp', 'G', 'G_sharp', 'A', 'A_sharp', 'B']
    octave = (midi_number // 12) - 1
    note = note_names[midi_number % 12]
    return f"{note}{octave}"


def midi_to_frequency(midi_number):
    # A4 is MIDI number 69 and has a frequency of 440 Hz
    a4_midi_number = 69
    a4_frequency = 440.0
    # Calculate the frequency using the formula
    frequency = a4_frequency * (2 ** ((midi_number - a4_midi_number) / 12.0))
    return frequency


import pretty_midi

midi_data = pretty_midi.PrettyMIDI(songName)
# print("duration:", midi_data.get_end_time())
# print(f'{"note":>10} {"start":>10} {"end":>10}')
events = []
for instrument in midi_data.instruments:
    # print("instrument:", instrument.program);
    for note in instrument.notes:
        # print(f'{midi_to_frequency(note.pitch)} {note.start:10} {note.end:10}')
        events.append([note.pitch, note.start, 's'])
        events.append([note.pitch, note.end, 'e'])
events.sort(key=lambda x: x[1])

def checkOnce():
    notes = []
    # sweep line algorithm
    currTime = 0
    eventIdx = 0
    tracks = collections.defaultdict(lambda: [])

    def fill_in_tracks(notes):
        for i in range(7):
            if i < len(notes):
                tracks[i].append(midi_to_frequency(notes[i]))
            else:
                tracks[i].append(0)

    maxLen = 0
    while (eventIdx < len(events)):
        while eventIdx < len(events) and (events[eventIdx][1] <= currTime):
            if events[eventIdx][2] == 's':
                notes.append(events[eventIdx][0])
            else:
                notes.remove(events[eventIdx][0])
            eventIdx += 1
        currTime += 0.05
        fill_in_tracks(notes)
        # print(f'{currTime:.2f}: {notes}')
        maxLen = max(maxLen, len(notes))
        # print same output to result.txt as well
        # with open('result.txt', 'a') as f:
        #     f.write(f'{currTime:.2f}: {notes}\n')
    print(f"{maxLen} notes")
    for i in range(maxLen):
        print('-------------------------------')
        print(tracks[i])

def play():
    import pygame


    def play_music(midi_filename):
        '''Stream music_file in a blocking manner'''
        clock = pygame.time.Clock()
        pygame.mixer.music.load(midi_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30)  # check if playback has finished


    midi_filename = songName

    # mixer config
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)

    # listen for interruptions
    try:
        # use the midi file you just saved
        play_music(midi_filename)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit

checkOnce()