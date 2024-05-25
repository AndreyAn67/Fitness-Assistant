import wx
from weather import get_weather, format_weather

class FitnessAssistantApp(wx.Frame):
    def __init__(self, parent, title):
        super(FitnessAssistantApp, self).__init__(parent, title=title, size=(400, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create buttons for different use cases
        buttons = [
            ('Authorization', self.authorization),
            ('Settings', self.settings),
            ('Exit', self.exit_app),
            ('Body Data and Personal Data', self.body_data),
            ('Local Database', self.local_database),
            ('Weather', self.weather),
            ('Weight', self.weight),
            ('Meal', self.meal),
            ('Training', self.training),
            ('Calorie Counting', self.calorie_counting),
            ('Recipe Recommendation', self.recipe_recommendation)
        ]

        for label, handler in buttons:
            button = wx.Button(panel, label=label)
            vbox.Add(button, flag=wx.EXPAND|wx.ALL, border=5)
            button.Bind(wx.EVT_BUTTON, handler)

        panel.SetSizer(vbox)

        self.Centre()
        self.Show()

    def authorization(self, event):
        wx.MessageBox('Authorization process', 'Info', wx.OK | wx.ICON_INFORMATION)

    def settings(self, event):
        wx.MessageBox('Settings window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def exit_app(self, event):
        self.Close()

    def body_data(self, event):
        wx.MessageBox('Body Data and Personal Data window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def local_database(self, event):
        wx.MessageBox('Local Database window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def weather(self, event):
        api_key = 'def384d40c2435f9a16cf1157d25de34'
        city = 'Novosibirsk'
        weather_data = get_weather(api_key, city)
        message = format_weather(weather_data, city)
        wx.MessageBox(message, 'Weather', wx.OK | wx.ICON_INFORMATION)

    def weight(self, event):
        wx.MessageBox('Weight window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def meal(self, event):
        wx.MessageBox('Meal window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def training(self, event):
        wx.MessageBox('Training window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def calorie_counting(self, event):
        wx.MessageBox('Calorie Counting window', 'Info', wx.OK | wx.ICON_INFORMATION)

    def recipe_recommendation(self, event):
        wx.MessageBox('Recipe Recommendation window', 'Info', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    FitnessAssistantApp(None, title='Fitness Assistant')
    app.MainLoop()