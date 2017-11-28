from Button import *

class Reminder(object):
    def __init__(self,date,content_list=None):
        self.content_list = content_list
        if self.content_list == None:
            self.content_list = []
        self.width = 200
        self.height = 50
        self.date = date
        self.button_list = []
        self.helper_button_list = []
        self.status_list = []

    def addContent(self,content):
        self.content_list.append(content)
        self.status_list.append(False)

    def getPixelLength(self,measureFont,text):
        return measureFont.getsize(text)  # this function call originally comes from Pillow documentation

    def createReminderButtons(self,color,x_left,y_up,font,measureFont,textColor,available_pixel_len):
        self.button_list = []
        self.helper_button_list = []

        for content in self.content_list:
            if self.getPixelLength(measureFont,content)[0] > available_pixel_len:
                init_string_len = 2
                first_line = content[:init_string_len]
                while self.getPixelLength(measureFont,first_line)[0] < available_pixel_len:
                    init_string_len += 1
                    first_line = content[:init_string_len]
                second_line = content[init_string_len:]
                button = RectButton("Reminder",color,x_left,x_left+self.width,y_up,y_up+self.height,0,first_line,font,textColor)
                button.AddIcon("Incomplete.png",35,35,1/10,alter_icon_path="Tocomplete.png")
                button.AddExtraIcon("Complete.png",35,35)
                y_up += self.height*2/3
                self.button_list.append(button)
                helper_button = RectButton("Reminder",color,x_left,x_left+self.width,y_up,y_up+self.height,0,second_line,font,textColor)
                y_up += self.height
                self.helper_button_list.append(helper_button)
            else:
                button = RectButton("Reminder", color, x_left, x_left + self.width, y_up, y_up + self.height, 0,
                                    content, font, textColor)
                button.AddIcon("Incomplete.png", 35, 35, 1 / 10, alter_icon_path="Tocomplete.png")
                button.AddExtraIcon("Complete.png", 35, 35)
                y_up += self.height
                self.button_list.append(button)

    def mouseMotion(self,x,y):
        for index in range(len(self.button_list)):
            button = self.button_list[index]
            if button.WithinRange(x,y):
                if self.status_list[index] == True:
                    button.displayed_icon = button.extra_icon
                else:
                    button.displayed_icon = button.alter_icon
            else:
                if self.status_list[index] == True:
                    button.displayed_icon = button.extra_icon
                else:
                    button.displayed_icon = button.icon

    def Draw(self,screen,text_width_coef=1/4):
        for button in self.button_list:
            button.Draw(screen,text_width_coef=text_width_coef)
        for button in self.helper_button_list:
            button.Draw(screen, text_width_coef=text_width_coef)

