import wx
from weight import WeightDialog
from weather import get_weather, format_weather
from authorization import create_user_table, AuthDialog
from body_data import create_body_data_table, BodyDataDialog
from training import create_training_table, TrainingDialog
from meal import create_meal_table, MealDialog

class FitnessAssistantApp(wx.Frame):
    def __init__(self, parent, title):
        super(FitnessAssistantApp, self).__init__(parent, title=title, size=(1600, 900))

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        #Add image to the panel
        image = wx.Image('logo.jpeg', wx.BITMAP_TYPE_JPEG)
        image_bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(image))
        main_sizer.Add(image_bitmap, flag=wx.CENTER | wx.TOP, border=10)

        #create header
        header = wx.StaticText(panel, label="Fitness Assistant", style=wx.ALIGN_CENTER)
        font = header.GetFont()
        font.PointSize += 10
        font = font.Bold()
        header.SetFont(font)
        main_sizer.Add(header, flag=wx.CENTER | wx.ALL, border=10)

        # Create buttons for different use cases
        self.buttons = []

        use_cases = [
            ('Authorization', self.authorization),
            ('Body Data and Personal Data', self.body_data),
            ('Weather', self.weather),
            ('Weight', self.weight),
            ('Meal', self.meal),
            ('Training', self.training),
            ('Exit', self.exit_app)
        ]

        grid_sizer = wx.GridBagSizer(hgap=10, vgap=10)

        for i, (label, handler) in enumerate(use_cases):
            button = wx.Button(panel, label=label, size=(300,100))
            grid_sizer.Add(button, pos=(i//4, i%4), flag=wx.ALIGN_CENTER)
            button.Bind(wx.EVT_BUTTON, handler)
            if label != 'Authorization':
                button.Disable() # Disable buttons initially
            self.buttons.append(button)

        main_sizer.Add(grid_sizer, proportion=1 ,flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=10)
        panel.SetSizer(main_sizer)

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


if __name__ == '__main__':
    create_user_table()
    create_body_data_table()
    create_training_table()
    create_meal_table()
    app = wx.App()
    FitnessAssistantApp(None, title='Fitness Assistant')
    app.MainLoop()