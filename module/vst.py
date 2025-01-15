from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, QLabel)
import dawdreamer as daw
import sounddevice as sd
from scipy.io import wavfile
import os
import time

class Vst():
    def __init__(self, sample_rate=44100, buffer_size=128):
        self.sample_rate = sample_rate
        self.vst_path = (str)
        self.plugin_name = 'None'
        self.engine = daw.RenderEngine(sample_rate, buffer_size)
        self.plugin = (daw.PluginProcessor)
        self.isProcessorExists = False

    '''
    ファインダーでvstファイルを選択
    読み込めたらエディターを開く
    '''
    def load_vst(self):
        file,check = QFileDialog.getOpenFileName(None, "ファイルを選択してください。","/Library/Audio/Plug-Ins","All Files (*);;vst Files (*.vst);;vst3 Files (*.vst3)")

        if check:
            self.vst_path = file
            self.plugin_name = os.path.splitext(os.path.basename(self.vst_path))[0] # パスからプラグイン名取得
            self.plugin = self.engine.make_plugin_processor(self.plugin_name, self.vst_path)

            assert self.plugin.get_name() == self.plugin_name # プラグインが反映されなかった時にエラー投げる

            self.isProcessorExists = True
            self.vst_editer()

    '''
    エディターを開く
    プラグインが読み込まれてなかったらload_vst()
    '''
    def vst_editer(self):
        if self.isProcessorExists == True:
            self.plugin.open_editor()
        else:
            self.load_vst()

    '''
    渡したmidiファイルを読み込んだプラグインで音声出力
    プラグインが読み込まれてなかったらload_vst()を先に呼ぶ
    '''
    def render_audio(self, midi_path, duration):
        if self.isProcessorExists == True:
            self.plugin.load_midi(midi_path, clear_previous=True, beats=False, all_events=True)

            graph = [
            (self.plugin, []),
            ]

            self.engine.load_graph(graph)
            self.engine.render(duration)
            output = self.engine.get_audio()

            # sd.play(output.T, samplerate=self.sample_rate)
            wavfile.write('./output.wav', self.sample_rate, output.transpose())
            

        else:
            self.load_vst()
            self.render_audio(midi_path, duration)

    '''
    音を一つ鳴らす
    note: 音の高さ int
    dur: 長さ(秒) float
    velocity: 強さ int
    '''
    def play_note(self, note, dur, velocity):
        if self.isProcessorExists == True:
            self.plugin.clear_midi()
            self.plugin.add_midi_note(note=note, velocity=velocity, start_time=0, duration=dur, beats=False)

            graph = [
            (self.plugin, []),
            ]

            self.engine.load_graph(graph)

            self.engine.render(dur)
            output = self.engine.get_audio()

            sd.play(output.T, samplerate=self.sample_rate)
        else:
            print("!!!processor isnt exists")


'''
テスト用ウィンドウクラス
'''
class TestWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vst = Vst()

        print(sd.query_devices())

        # デフォルトデバイスの確認
        print("Default Input Device:", sd.default.device[0])
        print("Default Output Device:", sd.default.device[1])

        self.setWindowTitle('vstTest')
        self.resize(300, 300)

        self.load_vst_btn = QPushButton(self)
        self.load_vst_btn.move(10, 10)
        self.load_vst_btn.setText('load vst')
        self.load_vst_btn.pressed.connect(lambda: self.load_vst_btn_pressed())

        self.vst_editer_btn = QPushButton(self)
        self.vst_editer_btn.move(10, 40)
        self.vst_editer_btn.setText('vst editer')
        self.vst_editer_btn.pressed.connect(lambda: self.vst.vst_editer())

        self.render_btn = QPushButton(self)
        self.render_btn.move(10, 70)
        self.render_btn.setText('render')
        self.render_btn.pressed.connect(lambda: self.vst.render_audio('./test.mid', 8))

        self.plugin_name_label = QLabel(self)
        self.plugin_name_label.move(10, 110)
        self.plugin_name_label.setText(f'instrument: {self.vst.plugin_name}')

        self.render_btn = QPushButton(self)
        self.render_btn.move(70, 70)
        self.render_btn.setText('play note')
        self.render_btn.pressed.connect(lambda: self.vst.play_note(60, 1, 100))

    def load_vst_btn_pressed(self):
        self.vst.load_vst()
        self.plugin_name_label.setText(f'instrument: {self.vst.plugin_name}')

if __name__ == "__main__":
    app = QApplication()
    window = TestWindow()
    window.show()
    app.exec()
