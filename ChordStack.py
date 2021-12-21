class ChordStack:
    def __init__(self):
        self.chordList = list()
        self.notes = {'C': 'Am', 'C#': 'A#m', 'D': 'Bm', 'D#': 'Cm', 'E': 'C#m', 'F': 'Dm', 'F#': 'D#m', 'G': 'Em',
                      'G#': 'Fm', 'A': 'F#m', 'A#': 'Gm', 'B': 'G#m', 'Am': 'C', 'A#m': 'C#', 'Bm': 'D', 'Cm': 'D#',
                      'C#m': 'E', 'Dm': 'F', 'D#m': 'F#', 'Em': 'G', 'Fm': 'G#', 'F#m': 'A', 'Gm': 'A#', 'G#m': 'B'}

    def add_chord(self, chord):
        if self.chordList.__len__() == 0:
            self.chordList.append(chord)
            return
        if self.chordList[-1] != chord:
            self.chordList.append(chord)

    def check_chords(self, chords_to_check):
        matches = 0
        M = chords_to_check.__len__()
        N = self.chordList.__len__()
        skip = 0
        for i in range(N - M + 1):
            j = 0
            if skip > 0:
                skip -= 1
                continue

            while j < M:
                if self.chordList[i + j] != chords_to_check[j]:
                    break
                j += 1

            if j == M:
                matches += 1
                skip = M - 1
        return matches

    def get_chord_progression(self):
        total_chords = self.chordList.__len__()

        eight_chords_to_check = self.chordList[0:8]
        if eight_chords_to_check[0:4] != eight_chords_to_check[4:8]:
            eight_matches = self.check_chords(eight_chords_to_check)
            if eight_matches >= (total_chords * 0.8) / 8:
                print(eight_matches.__str__() + ' >= ' + ((total_chords * 0.8) / 8).__str__())
                return eight_chords_to_check

        four_chords_to_check = self.chordList[0:4]
        if four_chords_to_check[0:2] != four_chords_to_check[2:4]:
            four_matches = self.check_chords(four_chords_to_check)
            if four_matches >= (total_chords * 0.7) / 4:
                return four_chords_to_check

        two_chords_to_check = self.chordList[0:2]
        two_matches = self.check_chords(two_chords_to_check)
        if two_matches >= (total_chords * 0.6) / 2:
            return two_chords_to_check

    def get_all_chords(self):
        return self.chordList

    def get_key_signature(self):
        return self.chordList[-1]

    def is_minor(self, chord):
        if chord.find('m') == -1:
            return False
        return True

    def get_avg_tension(self):
        home = self.get_key_signature()
        home_relative = self.notes[home]
        print('This is home: ' + home + ' and this is home relative ' + home_relative)
        tension = 0
        resets = 0
        for chord in self.get_all_chords():
            if chord == home or chord == home_relative:
                resets += 1
            else:
                tension += 1

        if resets == 0:
            return tension

        return tension / resets
