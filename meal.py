import wx
import wx.adv
import sqlite3
#from datetime import datetime

def create_meal_table():
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            weight REAL,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def add_meal(user_id, name, weight, date):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO meals (user_id, name, weight, date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, name, weight, date))
    conn.commit()
    conn.close()

def delete_meal(meal_id):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM meals WHERE id = ?', (meal_id,))
    conn.commit()
    conn.close()

def get_meals_for_date(user_id, date):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, weight FROM meals WHERE user_id = ? AND date = ?', (user_id, date))
    meals = cursor.fetchall()
    conn.close()
    return meals

class MealDialog(wx.Dialog):
    def __init__(self, parent, user_id):
        super(MealDialog, self).__init__(parent, title="Meals", size=(1200, 800))
        self.user_id = user_id

        self.calendar = wx.adv.CalendarCtrl(self, style=wx.adv.CAL_SHOW_HOLIDAYS)
        self.Bind(wx.adv.EVT_CALENDAR, self.on_date_selected, self.calendar)
        
        self.meal_list = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.meal_list.InsertColumn(0, 'Name', width=140)
        self.meal_list.InsertColumn(1, 'Weight (kg)', width=100)

        self.add_button = wx.Button(self, label="Add Meal")
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_meal)

        self.delete_button = wx.Button(self, label="Delete Meal")
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_meal)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.calendar, 0, wx.EXPAND | wx.ALL, 5)
        self.vbox.Add(self.meal_list, 1, wx.EXPAND | wx.ALL, 5)
        self.vbox.Add(self.add_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.vbox.Add(self.delete_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(self.vbox)

        self.current_date = self.calendar.GetDate().FormatISODate()
        self.load_meals_for_date(self.current_date)

    def on_date_selected(self, event):
        self.current_date = event.GetDate().FormatISODate()
        self.load_meals_for_date(self.current_date)

    def load_meals_for_date(self, date):
        self.meal_list.DeleteAllItems()
        meals = get_meals_for_date(self.user_id, date)
        for meal in meals:
            index = self.meal_list.InsertItem(self.meal_list.GetItemCount(), meal[1])
            self.meal_list.SetItem(index, 1, str(meal[2]))
            self.meal_list.SetItemData(index, meal[0])

    def on_add_meal(self, event):
        dialog = AddMealDialog(self, self.user_id, self.current_date)
        if dialog.ShowModal() == wx.ID_OK:
            self.load_meals_for_date(self.current_date)
        dialog.Destroy()

    def on_delete_meal(self, event):
        selected_item = self.meal_list.GetFirstSelected()
        if selected_item != -1:
            meal_id = self.meal_list.GetItemData(selected_item)
            delete_meal(meal_id)
            self.load_meals_for_date(self.current_date)
        else:
            wx.MessageBox('Please select a meal to delete.', 'Error', wx.OK | wx.ICON_ERROR)

class AddMealDialog(wx.Dialog):
    def __init__(self, parent, user_id, date):
        super(AddMealDialog, self).__init__(parent, title="Add Meal", size=(300, 200))
        self.user_id = user_id
        self.date = date

        self.name_label = wx.StaticText(self, label="Meal Name:")
        self.name_text = wx.TextCtrl(self)

        self.weight_label = wx.StaticText(self, label="Weight (kg):")
        self.weight_text = wx.TextCtrl(self)

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.name_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.name_text, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.weight_label, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.weight_text, flag=wx.EXPAND | wx.ALL, border=5)
        self.vbox.Add(self.save_button, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizer(self.vbox)

    def on_save(self, event):
        name = self.name_text.GetValue()
        try:
            weight = float(self.weight_text.GetValue())
            add_meal(self.user_id, name, weight, self.date)
            self.EndModal(wx.ID_OK)
        except ValueError:
            wx.MessageBox('Invalid weight value', 'Error', wx.OK | wx.ICON_ERROR)
