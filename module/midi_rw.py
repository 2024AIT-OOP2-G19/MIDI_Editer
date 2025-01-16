from mido import MidiFile, MidiTrack
from PySide6.QtWidgets import QFileDialog

def create_newMidi():
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    return midi

def load_midi(file_path: str) -> MidiFile:
    midi = MidiFile(file_path)
    print(f"MIDI file loaded: {file_path}")
    return midi

def save_midi(self, midi: MidiFile, file_path=None):
    if file_path is None:
        # ファイル保存ダイアログを開く
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "MIDIファイルを保存",
            "",
            "MIDI Files (*.mid)"
        )
    midi.save(file_path)
    print(f"MIDI file saved: {file_path}")
