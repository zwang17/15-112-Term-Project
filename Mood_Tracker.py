import Database
import pygame
from datetime import date
from Button import *

class MoodTracker(object):
    def __init__(self):
        self.endDate = Database.todayDate()
        self.startDate = Database.todayDate()
        self.startDate[1] -= 1
        self.datapoint_button_list = []
        self.Y_max = 1
        self.Y_min = -1
        self.drawInfo = False

    def update_display_list(self):
        self.display_list = Database.retreieve_diary_between(self.startDate,self.endDate)

    def update_data_list(self):
        for diary in self.display_list:
            total_span = Database.getDeltaDays(self.endDate,self.startDate)
            diary_span = Database.getDeltaDays(diary.date,self.startDate)
            x_coor = self.X_x_left + self.X_length * diary_span / total_span
            y_coor = self.Y_y_down - (self.Y_length/2 + diary.sentiment_report[0]*self.Y_length/2)
            newDataButton = CircButton("dot",self.UI.orange,x_coor,y_coor,8)
            newDataButton.setDataObject(diary)
            self.datapoint_button_list.append(newDataButton)

    def createAidButton(self):
        width = 30
        height = 20
        self.infoButtonX = RectButton("infoX",self.UI.white,0,0,self.X_y+5,self.X_y+5+height,0,"",self.UI.myFont14,self.UI.brightGrey)
        self.infoButtonY = RectButton("infoY",self.UI.white,self.Y_x-width-10,self.Y_x-10,0,0,0,"",self.UI.myFont14,self.UI.brightGrey)

    def updateAllButtons(self):
        self.update_display_list()
        self.update_data_list()
        self.createAidButton()

    def setUI(self,UI):
        self.UI = UI
        self.X_x_left = self.UI.MainBarButtonWidth + 60
        self.X_x_right = self.UI.width - 60
        self.X_init_x = self.X_x_left
        self.X_length = self.X_x_right - self.X_x_left
        self.X_y = self.Y_y_down = 540
        self.Y_x = self.X_x_left
        self.Y_y_up = 60
        self.Y_init_y = self.Y_y_down
        self.Y_length = self.Y_y_down - self.Y_y_up

# mouseMotion #
    def mouseMotion(self,x,y):
        for datapoint in self.datapoint_button_list:
            if datapoint.WithinRange(x,y):
                datapoint.color = (255, 219, 153)
                self.infoButtonX.x_left = datapoint.center_x
                self.infoButtonX.x_right = datapoint.center_x
                self.infoButtonY.y_up = datapoint.center_y
                self.infoButtonY.y_down = datapoint.center_y
                date = datapoint.data.date
                date_str = str(date[0])+"."+str(date[1])+"."+str(date[2])
                self.infoButtonX.text = date_str
                self.infoButtonY.text = str(int(datapoint.data.sentiment_report[0] * 100) / 100)
                self.drawInfo = True
                break
            else:
                datapoint.color = self.UI.orange
                self.drawInfo = False

# mouseReleased #

# redraw #
    def drawBaseline(self,screen):
        if self.Y_init_y > self.Y_y_up:
            self.Y_init_y -= 10
        if self.X_init_x < self.X_x_right:
            self.X_init_x += 10
        pygame.draw.lines(screen,self.UI.orange,False,[(self.X_x_left,self.X_y),(self.X_init_x,self.X_y)],2)
        pygame.draw.lines(screen, self.UI.orange, False, [(self.Y_x, self.Y_y_down), (self.Y_x, self.Y_init_y)], 2)

    def drawDatapoints(self,screen):
        for datapoint in self.datapoint_button_list:
            datapoint.Draw(screen)

    def drawVisualAid(self,screen):
        if self.drawInfo == True:
            self.infoButtonX.Draw(screen,text_anchor=1)
            self.infoButtonY.Draw(screen,text_anchor=1)
            pygame.draw.lines(screen,self.UI.brightGrey,False,[(self.infoButtonX.x_left,self.X_y),(self.infoButtonX.x_left,self.infoButtonY.y_up)],1)
            pygame.draw.lines(screen, self.UI.brightGrey, False,[(self.Y_x, self.infoButtonY.y_up), (self.infoButtonX.x_left, self.infoButtonY.y_up)],1)

    def redraw(self,screen):
        self.drawBaseline(screen)
        if self.Y_init_y <= self.Y_y_up and self.X_init_x >= self.X_x_right:
            self.drawDatapoints(screen)
            self.drawVisualAid(screen)