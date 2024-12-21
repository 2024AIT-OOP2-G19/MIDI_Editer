from mido import MidiFile, MidiTrack, Message

def create_midi(file_name: str):
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    return midi

def load_midi(file_path: str) -> MidiFile:
    midi = MidiFile(file_path)
    print(f"MIDI file loaded: {file_path}")
    return midi

def save_midi(midi: MidiFile, file_path: str):
    midi.save(file_path)
    print(f"MIDI file saved: {file_path}")
