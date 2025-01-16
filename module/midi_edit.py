import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from .midi_rw import create_newMidi

SEMIQUAVER_VALUE = 120  # 音の長さをmidi用に変換するための定数
MIDI_PITCH_ADJUST= 48  # 音の高さをmidi用に調整するための定数
VELOCITY = 100 # 音の強さの定数

    
'''XY座標の値からnoteに変換してmidファイルを生成する関数'''    
def note2midi(note_manager, bpm):
    # 初めのx座標、終わりのx座標でそれぞれ(on/off, y座標, x座標)のセットに変える
    # 座標の値をそれぞれy座標→note, x座標→time用の長さに変換したものに変える
    datas_noteXY =[]
    for key, data_xy in note_manager.items():
        entryLeft = {"noteEnable": "note_on", "y": data_xy["y_pos"] + MIDI_PITCH_ADJUST, "x": data_xy["left_x"] * SEMIQUAVER_VALUE}
        entryRight = {"noteEnable": "note_off", "y": data_xy["y_pos"] + MIDI_PITCH_ADJUST, "x": data_xy["right_x"] * SEMIQUAVER_VALUE}
        datas_noteXY.append(entryLeft)
        datas_noteXY.append(entryRight)
        
    # x座標の値を基準にしてソート
    datas_noteXY.sort(key=lambda x: x["x"])
    
    # 一つ前の値との差をとり、x座標の値の部分をそれ用に書き換える
    datas_note = []
    for i, data_noteXY in enumerate(datas_noteXY):
        if i == 0:
            entry = {"noteEnable": data_noteXY["noteEnable"], "note": data_noteXY["y"], "time": data_noteXY["x"]}
            datas_note.append(entry)
        else:
            entry = {"noteEnable": data_noteXY["noteEnable"], "note": data_noteXY["y"], "time": datas_noteXY[i]["x"] - datas_noteXY[i-1]["x"]}
            datas_note.append(entry)
    
    # 新しいmidiデータを入れるため一度midiデータを初期化
    mid = []
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # midのtrackにデータを入れる
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    for data_note in datas_note:
        track.append(Message(data_note["noteEnable"], note = data_note["note"], velocity = VELOCITY, time = data_note["time"]))
    
    return mid

'''midiデータからxy座標へ変換する関数'''
def midi2note(midi):
    # midデータを取り出して辞書型の配列に直す
    datas_mid = []
    for midMessage in midi.tracks[0]:
        if hasattr(midMessage, 'note'):  # hasattrはオブジェクトに指定した属性(今回はnote)が存在するか確かめる関数
            entry = {"noteEnable": midMessage.type, "note": midMessage.note, "time": midMessage.time}
            datas_mid.append(entry)
            
    # timeの値を絶対的な値に修正
    for i, data_mid in enumerate(datas_mid):
        if i >= 1:
            data_mid["time"] += datas_mid[i-1]["time"]
            
    # midsの値をそれぞれnote→y座標, time用の長さ→x座標に変換したものに変える
    for data_mid in datas_mid:
        data_mid["time"] //= SEMIQUAVER_VALUE
        data_mid["note"] -= MIDI_PITCH_ADJUST
    
    # midsの値からGUIのブロックにするための変換
    # noteの値, on/offごとにソート
    datas_mid.sort(key=lambda x: (x["note"], x["time"]))
    
    # note_managerを初期化
    note_manager = {}
    
    # on側とoff側を合体
    for i, data_mid in enumerate(datas_mid):
        if(data_mid["noteEnable"] == "note_on"):
            entry = {"id": i//2 + 1, "left_x": datas_mid[i]["time"], "right_x": datas_mid[i+1]["time"], "y_pos": data_mid["note"]}
            note_manager[i//2 + 1] = {"id":entry["id"], "left_x": entry["left_x"], "right_x": entry["right_x"], "y_pos": entry["y_pos"]}
            
    return note_manager

'''y座標から音の高さに変換する関数'''
def y2pitch(y):
    pitch = y + MIDI_PITCH_ADJUST
    return pitch
    