import csv


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
                    if len(notes) > 1 and row[0] == '6':    # 3 for sample and 6 for one_of_us
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
                            print('Is triad')
                            if (chord[1].col - chord[0].col) == 4 and (chord[2].col - chord[1].col) == 3:
                                print("Is Major: " + chord[0].name)
                            elif (chord[1].col - chord[0].col) == 3 and (chord[2].col - chord[1].col) == 4:
                                print('Is Minor: '+ chord[0].name + 'm')
                            elif (chord[1].col - chord[0].col) == 4 and (chord[2].col - chord[1].col) == 4:
                                print('Is Augmented: '+ chord[0].name + ' augmented')
                            elif (chord[1].col - chord[0].col) == 3 and (chord[2].col - chord[1].col) == 3:
                                print('Is Diminished: '+ chord[0].name + 'dim')
                            else:
                                print('Not determined')

                            for c in chord:
                                if (c.col - chord[0].col) == 7:
                                    print('Is 7th')
                                elif (c.col - chord[0].col) == 9:
                                    print('Is 9th')

                    notes = []
                    chord = []
                    notes.append(int(row[4]))
                pressure += int(row[5]) 
                on_notes_track += 1
                current_time = int(row[1])
            else:
                track = track_switch(row,track)

    print('\n')
    print("Tempo: " + str(csv_tempo))
    print("BPM: " + str(bpm))
    print('\n')
    print("Tracks")
    print('\n')
    for t in tracks:
        print("Title:" + t.title)
        print("Instrument:" + str(t.instrument))
        print("Pressure: " + str(t.avg_pressure))  
        print('\n')     