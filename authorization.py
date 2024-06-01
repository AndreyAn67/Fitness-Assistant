import sqlite3
import wx

def create_user_table():
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weight_records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight REAL,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = sqlite3.connect('fitness_assistant.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = sqlite3.connect('fitness_assistant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

class AuthDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(AuthDialog, self).__init__(parent, title=title, size=(500, 300))
        self.user_id = None

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.username_label = wx.StaticText(panel, label="Username")
        vbox.Add(self.username_label, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.username_text = wx.TextCtrl(panel)
        vbox.Add(self.username_text, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.password_label = wx.StaticText(panel, label="Password")
        vbox.Add(self.password_label, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.password_text = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        vbox.Add(self.password_text, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.register_button = wx.Button(panel, label='Register')
        hbox.Add(self.register_button)
        self.login_button = wx.Button(panel, label='Login')
        hbox.Add(self.login_button, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.register_button.Bind(wx.EVT_BUTTON, self.on_register)
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)

        panel.SetSizer(vbox)

    def on_register(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()
        if register_user(username, password):
            wx.MessageBox('Registration successful', 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Registration failed: Username already exists', 'Error', wx.OK | wx.ICON_ERROR)

    def on_login(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()
        user = login_user(username, password)
        if user:
            self.user_id = user[0]
            wx.MessageBox('Login successful', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox('Login failed: Invalid username or password', 'Error', wx.OK | wx.ICON_ERROR)