class NoteManager:
    def __init__(self, grid_size):
        self.notes = {}  # ノートを管理する辞書: {id: {key, left_x, right_x, y_pos}}
        self.grid_size = grid_size
        self.next_id = 1  # 次に割り当てるID

    def add_note(self, left_x, right_x, y_pos):
        """新しいノートを追加"""
        note_id = self.next_id
        self.notes[note_id] = {
            "id": note_id,
            "left_x": left_x,
            "right_x": right_x,
            "y_pos": y_pos,
        }
        self.next_id += 1

        # デバッグ用表示
        print(f"ノートが追加されました: ID={note_id}, left_x={left_x}, right_x={right_x}, y_pos={y_pos}")
        print("現在のノート一覧:")
        for id, note in self.notes.items():
            print(f"  ID={id}, left_x={note['left_x']}, right_x={note['right_x']}, y_pos={note['y_pos']}")

        return note_id

    def remove_note(self, note_id):
        """ノートを削除"""
        if note_id in self.notes:
            note = self.notes[note_id]
            print(f"ノートを削除: ID={note_id}, left_x={note['left_x']}, right_x={note['right_x']}, y_pos={note['y_pos']}")
            del self.notes[note_id]
            return True
        return False

    def update_note(self, note_id, left_x=None, right_x=None, y_pos=None):
        """既存のノートを更新"""
        if note_id not in self.notes:
            return False
        
        note = self.notes[note_id]
        if left_x is not None:
            note["left_x"] = left_x
        if right_x is not None:
            note["right_x"] = right_x
        if y_pos is not None:
            note["y_pos"] = y_pos
        return True

    def get_note_by_id(self, note_id):
        """指定されたIDのノートを取得"""
        return self.notes.get(note_id)

    def get_notes_by_position(self, x_pos, y_pos):
        """指定された位置に存在するノートを取得"""
        result = []
        for note in self.notes.values():
            if note["y_pos"] == y_pos and note["left_x"] <= x_pos < note["right_x"]:
                result.append(note)
        return result

    def snap_to_grid(self, value):
        """値をグリッドサイズにスナップ"""
        return round(value / self.grid_size) * self.grid_size

    def to_dict(self):
        """ノート情報を辞書として取得"""
        return self.notes

    def from_dict(self, data):
        """辞書からノート情報を読み込み"""
        self.notes = data
        self.next_id = max(data.keys(), default=0) + 1
