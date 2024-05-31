import wx
import wx.adv
import sqlite3
from datetime import datetime

def create_body_data_table():
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS body_data (
            user_id INTEGER PRIMARY KEY,
            height INTEGER,
            birth_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def update_body_data(user_id, height, birth_date):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO body_data (user_id, height, birth_date) VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET height=excluded.height, birth_date=excluded.birth_date
    ''', (user_id, height, birth_date))
    conn.commit()
    conn.close()

def get_body_data(user_id):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT height, birth_date FROM body_data WHERE user_id = ?', (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def get_latest_weight(user_id):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT weight, date FROM weight_records WHERE user_id = ? ORDER BY date DESC LIMIT 1', (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data

class BodyDataDialog(wx.Dialog):
    def __init__(self, parent, user_id):
        super(BodyDataDialog, self).__init__(parent, title="Body Data", size=(300, 400))
        self.user_id = user_id

        self.height_label = wx.StaticText(self, label="Height (cm):")
        self.height_text = wx.TextCtrl(self)

        self.birth_date_label = wx.StaticText(self, label="Birth Date:")
        self.birth_date_picker = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN)

        self.age_label = wx.StaticText(self, label="Age: N/A")
        
        self.weight_label = wx.StaticText(self, label="Latest Weight: N/A")

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.height_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.height_text, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.birth_date_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.birth_date_picker, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.age_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.weight_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.save_button, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizer(self.vbox)

        self.load_body_data()
        self.load_latest_weight()

    def load_body_data(self):
        data = get_body_data(self.user_id)
        if data:
            height, birth_date = data
            self.height_text.SetValue(str(height))
            birth_date_dt = datetime.strptime(birth_date, '%Y-%m-%d')
            self.birth_date_picker.SetValue(wx.DateTime.FromDMY(birth_date_dt.day, birth_date_dt.month - 1, birth_date_dt.year))
            self.update_age(birth_date_dt)

    def load_latest_weight(self):
        data = get_latest_weight(self.user_id)
        if data:
            weight, date = data
            self.weight_label.SetLabel(f"Latest Weight: {weight} kg (on {date})")
        else:
            self.weight_label.SetLabel("Latest Weight: No records found")

    def on_save(self, event):
        height = int(self.height_text.GetValue())
        birth_date = self.birth_date_picker.GetValue()
        birth_date_str = f"{birth_date.GetYear()}-{birth_date.GetMonth() + 1:02d}-{birth_date.GetDay():02d}"
        update_body_data(self.user_id, height, birth_date_str)
        self.update_age(datetime(birth_date.GetYear(), birth_date.GetMonth() + 1, birth_date.GetDay()))
        wx.MessageBox('Body data saved!', 'Info', wx.OK | wx.ICON_INFORMATION)

    def update_age(self, birth_date):
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        self.age_label.SetLabel(f"Age: {age}")
