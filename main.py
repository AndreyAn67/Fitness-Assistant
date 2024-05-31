import wx
from weight import record_weight, get_weight_records, plot_weight
from weather import get_weather, format_weather
from authorization import create_user_table, register_user, login_user
from body_data import create_body_data_table, BodyDataDialog
from training import create_training_table, TrainingDialog
from meal import create_meal_table, MealDialog

class FitnessAssistantApp(wx.Frame):
    def __init__(self, parent, title):
        super(FitnessAssistantApp, self).__init__(parent, title=title, size=(800, 500))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create buttons for different use cases
        self.buttons = []

        use_cases = [
            ('Authorization', self.authorization),
            ('Body Data and Personal Data', self.body_data),
            ('Weather', self.weather),
            ('Weight', self.weight),
            ('Meal', self.meal),
            ('Training', self.training),
            ('Calorie Counting', self.calorie_counting),
            ('Recipe Recommendation', self.recipe_recommendation),
            ('Exit', self.exit_app)
        ]

        for label, handler in use_cases:
            button = wx.Button(panel, label=label)
            vbox.Add(button, flag=wx.EXPAND|wx.ALL, border=5)
            button.Bind(wx.EVT_BUTTON, handler)
            if label != 'Authorization':
                button.Disable() # Disable buttons initially
            self.buttons.append(button)

        panel.SetSizer(vbox)

        self.Centre()
        self.Show()

    def authorization(self, event):
        auth_dialog = AuthDialog(None, title='Authorization')
        if auth_dialog.ShowModal() == wx.ID_OK:
            self.user_id = auth_dialog.user_id
            for button in self.buttons:
                button.Enable() # Enable all buttons after successful authorization
        auth_dialog.Destroy()

    def exit_app(self, event):
        self.Close()

    def body_data(self, event):
        dialog = BodyDataDialog(self, self.user_id)
        dialog.ShowModal()
        dialog.Destroy()


    def weather(self, event):
        dialog = wx.TextEntryDialog(self, 'Enter your location', 'Weather Location')
        if dialog.ShowModal() == wx.ID_OK:
            api_key = 'def384d40c2435f9a16cf1157d25de34'
            city = dialog.GetValue()
            weather_data = get_weather(api_key, city)
            message = format_weather(weather_data, city)
            wx.MessageBox(message, 'Weather', wx.OK | wx.ICON_INFORMATION)
        dialog.Destroy()

    def weight(self, event):
        weight_dialog = WeightDialog(self, 'Weight Record', self.user_id)
        weight_dialog.ShowModal()
        weight_dialog.Destroy

    def meal(self, event):
        meal_dialog = MealDialog(self, self.user_id)
        meal_dialog.ShowModal()
        meal_dialog.Destroy()

    def training(self, event):
        training_dialog = TrainingDialog(self, self.user_id)
        training_dialog.ShowModal()
        training_dialog.Destroy()

    def calorie_counting(self, event):
        wx.MessageBox('Calorie Counting window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def recipe_recommendation(self, event):
        wx.MessageBox('Recipe Recommendation window', 'Info', wx.OK | wx.ICON_INFORMATION)

class AuthDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(AuthDialog, self).__init__(parent, title=title, size=(350, 300))
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

class WeightDialog(wx.Dialog):
    def __init__(self, parent, title, user_id):
        super(WeightDialog, self).__init__(parent, title=title, size=(400, 300))
        self.user_id = user_id

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.weight_label = wx. StaticText(panel, label='Enter your weight (kg)')
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

if __name__ == '__main__':
    create_user_table()
    create_body_data_table()
    create_training_table()
    create_meal_table()
    app = wx.App()
    FitnessAssistantApp(None, title='Fitness Assistant')
    app.MainLoop()