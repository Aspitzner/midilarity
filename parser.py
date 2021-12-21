import csv
import ChordStack

class Track(object):
    title = ""
    instrument = 0
    avg_pressure = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, title, instrument, avg_pressure):
        self.title = title
        self.instrument = instrument
        self.avg_pressure = avg_pressure

class Note(object):
    name = ""
    octave = 0
    number = 0
    col = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, octave, number, col):
        self.name = name
        self.octave = octave
        self.number = number
        self.col = col



def header_switch(row):
    if row[2] == ' Title_t':
        title = row[3]
        print(title)
    elif row[2] == ' Time_signature':
        time_signature = row[3]+row[4]+row[5]+row[6]
        print(time_signature)
    


def track_switch(row,track):
    if row[2] == ' Title_t':
        track.title = row[3]
    elif row[2] == ' Program_c':
        track.instrument = row[4]
    return track

note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
print("String:\t" + str(int(' 45')))
with open('sample.csv') as csv_file:
    tracks = []
    track = Track("",0,0)
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    track_count = 1
    on_notes_track = 0
    pressure = 0
    current_time = -1
    notes = []
    chord = []
    bpm = 0
    chordStack = ChordStack.ChordStack()
    for row in csv_reader:
        line_count += 1
        if row[2] == ' End_track':
                if track_count>1:
                    if on_notes_track != 0:
                        track.avg_pressure = pressure/on_notes_track
                    tracks.append(track)
                    on_notes_track = 0
                    pressure = 0
                track_count +=1
        if track_count == 1:
            if row[2] == ' Tempo':
                csv_tempo = int(row[3])
                bpm = 60000000/csv_tempo
            else:
                header_switch(row)
            
        else:
            if row[2] == ' Start_track':
                track = Track("",0,0)
            elif row[2] == ' Note_on_c':
                if current_time == int(row[1]):
                    notes.append(int(row[4]))
                else:
                    if len(notes) > 1 and row[0] == '3':    # 3 for sample and 6 for one_of_us
                        # search_chord(chord)
                        print('\n')
                        print(current_time)
                        print(notes)
                        for i in range(0, len(notes)):
                            num = notes[i]
                            col = num%12
                            octave = 0
                            while num >= 12:
                                octave += 1
                                num -= 12
                            
                            note = Note(note_names[col],octave,notes[i],col)
                            chord.append(note)
                            print('Num\t'+str(note.number))
                            print('Note\t'+str(note.name))
                            print('Octave\t'+str(note.octave))
                            print('Col ' + str(note.col))
                        print('Chord')
                        for c in chord:
                            print(c.name)
                        if len(chord) == 3:
                            print(chord[0].col)

                            print('Is triad')
                            for i in range(3):
                                base = chord[(i) % 3].col
                                third = chord[(i + 1) % 3].col
                                fifth = chord[(i + 2) % 3].col
                                if(third < base):
                                    third = third + 12
                                if( fifth < base):
                                    fifth = fifth + 12
                                if(fifth - base) == 7:
                                    if (third - base) == 4:
                                        print("Is Major: " + chord[i].name)
                                        chordStack.add_chord(chord[i].name)
                                    elif (third - base) == 3:
                                        print('Is Minor: '+ chord[i].name + 'm')
                                        chordStack.add_chord(chord[i].name)
#                                    elif (chord[1].col - chord[0].col) == 4 and (chord[2].col - chord[1].col) == 4:
#                                        print('Is Augmented: '+ chord[0].name + ' augmented')
#                                    elif (chord[1].col - chord[0].col) == 3 and (chord[2].col - chord[1].col) == 3:
#                                        print('Is Diminished: '+ chord[0].name + 'dim')
                                else:
                                    print('Not determined for this rotation')

                            #for c in chord:
                            #    if (c.col - chord[0].col) == 11:
                            #        print('Is 7th')
                            #    elif (c.col - chord[0].col) == 9:
                            #        print('Is 9th')

                    notes = []
                    chord = []
                    notes.append(int(row[4]))
                pressure += int(row[5]) 
                on_notes_track += 1
                current_time = int(row[1])
            else:
                track = track_switch(row,track)

    print('\n')
    print("Tracks")
    for t in tracks:
        print("Title:" + t.title)
        print("Instrument:" + str(t.instrument))
        print("Pressure: " + str(t.avg_pressure))
        print('\n')
    print("Tempo: " + str(csv_tempo))
    print("BPM: " + str(bpm))
    print('All chords: ' + chordStack.get_all_chords().__str__())
    print('Chord progression: ' + chordStack.get_chord_progression().__str__())
    print('Key signature: ' + chordStack.get_key_signature())
    print('Avg. Tension: ' + chordStack.get_avg_tension().__str__())
