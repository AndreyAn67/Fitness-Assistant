import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import wx

def record_weight(user_id, weight):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO weight_records (user_id, weight, date) VALUES (?, ?, ?)', (user_id, weight, date))
    conn.commit()
    conn.close()

def get_weight_records(user_id):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT weight, date FROM weight_records WHERE user_id = ? ORDER BY date', (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def plot_weight(records):
    if records:
        dates = [record[1] for record in records]
        weights = [record[0] for record in records]
        plt.figure(figsize=(10, 5))
        plt.plot(dates, weights, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Weight(kg)')
        plt.title('Weight Change Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print('No weight records found')

class WeightDialog(wx.Dialog):
    def __init__(self, parent, title, user_id):
        super(WeightDialog, self).__init__(parent, title=title, size=(800, 600))
        self.user_id = user_id

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.weight_label = wx.StaticText(panel, label='Enter your weight (kg)')
        vbox.Add(self.weight_label, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.weight_text = wx.TextCtrl(panel)
        vbox.Add(self.weight_text, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.submit_button = wx.Button(panel, label='Submit')
        hbox.Add(self.submit_button)
        self.plot_button = wx.Button(panel, label='Show Plot')
        hbox.Add(self.plot_button, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)
        self.plot_button.Bind(wx.EVT_BUTTON, self.on_show_plot)

        panel.SetSizer(vbox)

    def on_submit(self, event):
        try:
            weight = float(self.weight_text.GetValue())
            record_weight(self.user_id, weight)
            wx.MessageBox('Weight recorded successfully', 'Info', wx.OK|wx.ICON_INFORMATION)
        except ValueError:
            wx.MessageBox('Invalid weight value', 'Error', wx.OK|wx.ICON_ERROR)    

    def on_show_plot(self, event):
        records = get_weight_records(self.user_id)
        if records:
            plot_weight(records)
        else:
            wx.MessageBox('No weight records found', 'Info', wx.OK | wx.ICON_INFORMATION)