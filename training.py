import wx
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

def create_training_table():
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            type TEXT,
            duration TEXT, -- For aerobic exercise
            sets INTEGER, -- For anaerobic exercise
            reps INTEGER, -- For anaerobic exercise
            weight REAL, -- For anaerobic exercise
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def record_aerobic_exercise(user_id, name, hours, minutes):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    duration = f"{hours}h {minutes}m"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO training (user_id, name, type, duration, date) 
        VALUES (?, ?, 'aerobic', ?, ?)
    ''', (user_id, name, duration, date))
    conn.commit()
    conn.close()

def record_anaerobic_exercise(user_id, name, sets, reps, weight):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO training (user_id, name, type, sets, reps, weight, date) 
        VALUES (?, ?, 'anaerobic', ?, ?, ?, ?)
    ''', (user_id, name, sets, reps, weight, date))
    conn.commit()
    conn.close()

def get_training_data(user_id):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, type, date FROM training WHERE user_id = ?', (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def delete_training_record(record_id):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM training WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def get_training_records(user_id, name):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, weight FROM training 
        WHERE user_id = ? AND name = ? AND type = 'anaerobic' ORDER BY date
    ''', (user_id, name))
    records = cursor.fetchall()
    conn.close()
    return records

def plot_weight_changes(records):
    if records:
        dates = [record[0] for record in records]
        weights = [record[1] for record in records]
        plt.figure(figsize=(10, 5))
        plt.plot(dates, weights, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Weight (kg)')
        plt.title('Weight Change Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print('No training records found')

class TrainingDialog(wx.Dialog):
    def __init__(self, parent, user_id):
        super(TrainingDialog, self).__init__(parent, title="Training", size=(800, 800))
        self.user_id = user_id

        self.training_list = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.training_list.InsertColumn(0, 'Name', width=140)
        self.training_list.InsertColumn(1, 'Type', width=100)
        self.training_list.InsertColumn(2, 'Date', width=140)

        self.load_training_data()

        self.add_button = wx.Button(self, label="Add")
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add)

        self.delete_button = wx.Button(self, label="Delete")
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete)

        self.plot_button = wx.Button(self, label="Plot")
        self.plot_button.Bind(wx.EVT_BUTTON, self.on_plot)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.training_list, 1, wx.EXPAND | wx.ALL, 5)
        self.vbox.Add(self.add_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.vbox.Add(self.delete_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.vbox.Add(self.plot_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(self.vbox)

    def load_training_data(self):
        self.training_list.DeleteAllItems()
        records = get_training_data(self.user_id)
        for record in records:
            index = self.training_list.InsertItem(self.training_list.GetItemCount(), record[1])
            self.training_list.SetItem(index, 1, record[2])
            self.training_list.SetItem(index, 2, record[3])
            self.training_list.SetItemData(index, record[0])

    def on_add(self, event):
        dialog = AddTrainingDialog(self, self.user_id)
        if dialog.ShowModal() == wx.ID_OK:
            self.load_training_data()
        dialog.Destroy()

    def on_delete(self, event):
        selected_item = self.training_list.GetFirstSelected()
        if selected_item != -1:
            record_id = self.training_list.GetItemData(selected_item)
            delete_training_record(record_id)
            self.load_training_data()
        else:
            wx.MessageBox('Please select a training record to delete.', 'Error', wx.OK | wx.ICON_ERROR)

    def on_plot(self, event):
        selected_item = self.training_list.GetFirstSelected()
        if selected_item != -1:
            name = self.training_list.GetItemText(selected_item)
            records = get_training_records(self.user_id, name)
            plot_weight_changes(records)
        else:
            wx.MessageBox('Please select an anaerobic training record to plot.', 'Error', wx.OK | wx.ICON_ERROR)

class AddTrainingDialog(wx.Dialog):
    def __init__(self, parent, user_id):
        super(AddTrainingDialog, self).__init__(parent, title="Add Training", size=(400, 400))
        self.user_id = user_id

        self.name_label = wx.StaticText(self, label="Exercise Name:")
        self.name_text = wx.TextCtrl(self)

        self.type_label = wx.StaticText(self, label="Exercise Type:")
        self.type_choice = wx.Choice(self, choices=["Aerobic", "Anaerobic"])
        self.type_choice.Bind(wx.EVT_CHOICE, self.on_type_choice)

        self.duration_label = wx.StaticText(self, label="Duration:")
        self.hour_choice = wx.Choice(self, choices=[str(i) for i in range(24)])
        self.minute_choice = wx.Choice(self, choices=[str(i) for i in range(60)])

        self.sets_label = wx.StaticText(self, label="Sets:")
        self.sets_choice = wx.Choice(self, choices=[str(i) for i in range(1, 11)])

        self.reps_label = wx.StaticText(self, label="Reps per Set:")
        self.reps_choice = wx.Choice(self, choices=[str(i) for i in range(1, 31)])

        self.weight_label = wx.StaticText(self, label="Weight (kg):")
        self.weight_choice = wx.Choice(self, choices=[str(i) for i in range(1, 101)])

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.name_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.name_text, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.type_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.type_choice, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.duration_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.hour_choice, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.minute_choice, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.sets_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.sets_choice, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.reps_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.reps_choice, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.weight_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.weight_choice, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.save_button, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizer(self.vbox)
        self.update_ui()

    def on_type_choice(self, event):
        self.update_ui()

    def update_ui(self):
        exercise_type = self.type_choice.GetStringSelection()
        if exercise_type == "Aerobic":
            self.duration_label.Show()
            self.hour_choice.Show()
            self.minute_choice.Show()
            self.sets_label.Hide()
            self.sets_choice.Hide()
            self.reps_label.Hide()
            self.reps_choice.Hide()
            self.weight_label.Hide()
            self.weight_choice.Hide()
        elif exercise_type == "Anaerobic":
            self.duration_label.Hide()
            self.hour_choice.Hide()
            self.minute_choice.Hide()
            self.sets_label.Show()
            self.sets_choice.Show()
            self.reps_label.Show()
            self.reps_choice.Show()
            self.weight_label.Show()
            self.weight_choice.Show()
        self.Layout()

    def on_save(self, event):
        name = self.name_text.GetValue()
        exercise_type = self.type_choice.GetStringSelection()
        if exercise_type == "Aerobic":
            hours = self.hour_choice.GetStringSelection()
            minutes = self.minute_choice.GetStringSelection()
            record_aerobic_exercise(self.user_id, name, hours, minutes)
        elif exercise_type == "Anaerobic":
            sets = self.sets_choice.GetStringSelection()
            reps = self.reps_choice.GetStringSelection()
            weight = self.weight_choice.GetStringSelection()
            record_anaerobic_exercise(self.user_id, name, sets, reps, weight)
        self.EndModal(wx.ID_OK)
