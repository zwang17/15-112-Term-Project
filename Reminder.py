from Button import *
import Database

class Reminder(object):
    def __init__(self,date,content_list=None):
        self.content_list = content_list
        if self.content_list == None:
            self.content_list = []
        self.width = 120
        self.height = 50
        self.date = date
        self.button_list = []
        self.helper_button_dict = {}
        self.status_list = []

    def addContent(self,content):
        self.content_list.append(content)
        self.status_list.append(False)

    def getPixelLength(self,measureFont,text):
        return measureFont.getsize(text)

    # def updateReminderButtons(self,color,x_left,y_up,font,measureFont,textColor,available_pixel_len):
    #     self.button_list = []
    #     self.helper_button_list = []
    #     self.delete_button_list = []
    #
    #     for content in self.content_list:
    #         if self.getPixelLength(measureFont,content)[0] > available_pixel_len:
    #             init_string_len = 2
    #             first_line = content[:init_string_len]
    #             while self.getPixelLength(measureFont,first_line)[0] < available_pixel_len:
    #                 init_string_len += 1
    #                 first_line = content[:init_string_len]
    #             second_line = content[init_string_len:]
    #             button = RectButton("Reminder",color,x_left,x_left+self.width,y_up,y_up+self.height,0,first_line,font,textColor)
    #             button.AddIcon("Incomplete.png",35,35,1/10,alter_icon_path="Tocomplete.png")
    #             button.AddExtraIcon("Complete.png",35,35)
    #             y_up += self.height*2/3
    #             self.button_list.append(button)
    #             helper_button = RectButton("Reminder",color,x_left,x_left+self.width,y_up,y_up+self.height,0,second_line,font,textColor)
    #             self.helper_button_list.append(helper_button)
    #         else:
    #             button = RectButton("Reminder", color, x_left, x_left + self.width, y_up, y_up + self.height, 0,
    #                                 content, font, textColor)
    #             button.AddIcon("Incomplete.png", 35, 35, 1 / 10, alter_icon_path="Tocomplete.png")
    #             button.AddExtraIcon("Complete.png", 35, 35)
    #             self.button_list.append(button)
    #         y_up += self.height/2
    #         button = RectButton("Reminder", color, x_left+available_pixel_len , x_left+available_pixel_len*1.2, y_up-10, y_up+10, 0, "X",
    #                             font, textColor)
    #         self.delete_button_list.append(button)
    #         y_up += self.height/2

### experiment
    def updateReminderButtons(self,color,x_left,y_up,font,measureFont,textColor,available_pixel_len):
        self.button_list = []
        self.helper_button_dict = {}
        self.delete_button_list = []

        for content in self.content_list:
            content_string = content
            num_helper = 0
            while self.getPixelLength(measureFont,content_string)[0] > available_pixel_len:
                init_string_len = 1
                line = content_string[:init_string_len]
                while self.getPixelLength(measureFont,line)[0] < available_pixel_len:
                    init_string_len += 1
                    line = content_string[:init_string_len]
                content_string = content_string[init_string_len:]
                if line[-1] != " " and len(content_string) > 0 and content_string[0] != " ":
                    line += "-"
                if num_helper == 0:
                    button = RectButton(content,color,x_left,x_left+self.width,y_up,y_up+self.height,0,line,font,textColor)
                    button.AddIcon("Incomplete.png",35,35,1/10,alter_icon_path="Tocomplete.png")
                    button.AddExtraIcon("Complete.png",35,35)
                    self.button_list.append(button)
                    num_helper += 1
                else:
                    y_up += self.height * 2 /3
                    helper_button = RectButton("Reminder",color,x_left,x_left+self.width,y_up,y_up+self.height,0,line,font,textColor)
                    if content in self.helper_button_dict:
                        self.helper_button_dict[content].append(helper_button)
                    else:
                        self.helper_button_dict[content] = [helper_button]
            if len(content_string) > 0:
                if num_helper == 0:
                    button = RectButton(content,color,x_left,x_left+self.width,y_up,y_up+self.height,0,content_string,font,textColor)
                    button.AddIcon("Incomplete.png",35,35,1/10,alter_icon_path="Tocomplete.png")
                    button.AddExtraIcon("Complete.png",35,35)
                    self.button_list.append(button)
                if num_helper != 0:
                    y_up += self.height* 2 /3
                    helper_button = RectButton("Reminder", color, x_left, x_left + self.width, y_up, y_up + self.height, 0,
                                               content_string, font, textColor)
                    if content in self.helper_button_dict:
                        self.helper_button_dict[content].append(helper_button)
                    else:
                        self.helper_button_dict[content] = [helper_button]
            y_up += self.height/2
            button = RectButton("Reminder", color, x_left+available_pixel_len*1.4 , x_left+available_pixel_len*1.5, y_up-10, y_up+10, 0, "X",
                                font, textColor)
            self.delete_button_list.append(button)
            y_up += self.height/2

###

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
            button = self.delete_button_list[index]
            if button.WithinRange(x,y):
                button.textColor = (223, 26, 6)
            else:
                button.textColor = (119, 124, 118)

    def mouseReleased(self,x,y):
        for index in range(len(self.button_list)):
            button = self.button_list[index]
            if button.WithinRange(x, y):
                self.status_list[index] = not self.status_list[index]
        for index in range(len(self.delete_button_list)):
            button = self.delete_button_list[index]
            if button.WithinRange(x, y):
                self.button_list.pop(index)
                self.delete_button_list.pop(index)
                try:
                    del self.helper_button_dict[self.content_list[index]]
                except:
                    pass
                self.content_list.pop(index)
                self.status_list.pop(index)
                break
        self.mouseMotion(x,y)
        Database.save_reminder(self)

    def Draw(self,screen,text_width_coef=1/4):
        for button in self.button_list:
            button.Draw(screen,text_width_coef=text_width_coef)
        for key in self.helper_button_dict:
            for button in self.helper_button_dict[key]:
                button.Draw(screen, text_width_coef=text_width_coef)
        for button in self.delete_button_list:
            button.Draw(screen)
