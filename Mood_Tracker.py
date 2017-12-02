import Database
import pygame
from datetime import date
from Button import *
import copy
from threading import Thread

class MoodTracker(object):
    def __init__(self):
        self.endDate = Database.todayDate()
        self.startDate = Database.todayDate()
        self.startDate[1] -= 1
        self.datapoint_button_list = []
        self.Y_max = 1
        self.Y_min = -1
        self.drawInfo = False
        self.animation_speed = 10
        self.timer = 0

    def initModeButtons(self):
        width = 100
        margin = 10
        height = 20
        self.two_weeks_button = RectButton("two weeks", self.UI.white, self.UI.width - margin - width,
                                         self.UI.width - margin, self.UI.height - margin - height, self.UI.height - margin, text="Past 2 Weeks",font=self.UI.myFont12,textColor=self.UI.brightGrey)
        self.month_button = RectButton("one month", self.UI.white, self.UI.width - margin - 2*width,
                                    self.UI.width - margin-width, self.UI.height - margin - height,
                                    self.UI.height - margin, text="Past Month", font=self.UI.myFont12,
                                    textColor=self.UI.themeColorMain)
        self.month_button.status = True
        self.six_month_button = RectButton("six month", self.UI.white, self.UI.width - margin - 3 * width,
                                             self.UI.width - margin - 2 * width, self.UI.height - margin - height,
                                             self.UI.height - margin , text="Past 6 Month",
                                             font=self.UI.myFont12,
                                             textColor=self.UI.brightGrey)
        self.mode_button_list = [self.two_weeks_button,self.month_button,self.six_month_button]

    def update_display_list(self):
        self.display_list = []
        self.display_list = Database.retreieve_diary_between(self.startDate,self.endDate)

    def update_data_list(self):
        self.datapoint_button_list = []
        for diary in self.display_list:
            total_span = Database.getDeltaDays(self.endDate,self.startDate)
            diary_span = Database.getDeltaDays(diary.date,self.startDate)
            x_coor = self.X_x_left + self.X_length * diary_span / total_span
            y_coor = self.Y_y_down - (self.Y_length/2 + diary.sentiment_report[0]*self.Y_length/2)
            newDataButton = CircButton("dot",self.UI.themeColorMain,x_coor,y_coor,9)
            newDataButton.setDataObject(diary)
            self.datapoint_button_list.append(newDataButton)

    def updateSpan(self):
        date = Database.todayDate()
        if self.two_weeks_button.status == True:
            for i in range(14):
                Database.previous_date(date)
            self.startDate = copy.deepcopy(date)
        elif self.month_button.status == True:
            for i in range(31):
                Database.previous_date(date)
            self.startDate = copy.deepcopy(date)
        elif self.six_month_button.status == True:
            for i in range(365//2):
                Database.previous_date(date)
            self.startDate = copy.deepcopy(date)
        self.updateAllButtons()
        for datapoint in self.datapoint_button_list:
            datapoint.radius = 9

    def createAidButton(self):
        width = 30
        height = 20
        self.infoButtonX = RectButton("infoX",self.UI.white,0,0,self.X_y+5,self.X_y+5+height,0,"",self.UI.myFont14,self.UI.brightGrey)
        self.infoButtonY = RectButton("infoY",self.UI.white,self.Y_x-width-10,self.Y_x-10,0,0,0,"",self.UI.myFont14,self.UI.brightGrey)

    def updateAllButtons(self):
        self.update_display_list()
        self.update_data_list()

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
        self.initModeButtons()
        self.createAidButton()

# mouseMotion #
    def mouseMotion(self,x,y):
        if self.timer < 40:
            return None
        for datapoint in self.datapoint_button_list:
            if datapoint.WithinRange(x,y):
                datapoint.radius = 9
                datapoint.color = self.UI.themeColorMain
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
                datapoint.radius = 5
                datapoint.color = self.UI.themeColorMain
                self.drawInfo = False
        for button in self.mode_button_list:
            if button.WithinRange(x,y) or button.status == True:
                button.textColor = self.UI.themeColorMain
            else:
                button.textColor = self.UI.brightGrey

# mouseReleased #
    def mouseReleased(self,x,y):
        for button in self.mode_button_list:
            if button.WithinRange(x, y):
                for button in self.mode_button_list:
                    if button.WithinRange(x, y):
                        button.status = True
                    else:
                        button.status = False
                self.updateSpan()
                self.timer = 0

# redraw #

    def drawConnectingLines(self,screen):
        for index in range(len(self.datapoint_button_list)-1):
            datapoint1 = self.datapoint_button_list[index]
            datapoint2 = self.datapoint_button_list[index+1]
            pygame.draw.lines(screen,self.UI.themeColorMain,False,[(datapoint1.center_x,datapoint1.center_y),(datapoint2.center_x,datapoint2.center_y)],1)

    def drawBaseline(self,screen):
        if self.Y_init_y > self.Y_y_up:
            self.Y_init_y -= self.animation_speed
        if self.X_init_x < self.X_x_right:
            self.X_init_x += self.animation_speed
        pygame.draw.lines(screen,self.UI.themeColorMain,False,[(self.X_x_left,self.X_y),(self.X_init_x,self.X_y)],2)
        pygame.draw.lines(screen, self.UI.themeColorMain, False, [(self.Y_x, self.Y_y_down), (self.Y_x, self.Y_init_y)], 2)

    def drawDatapoints(self,screen):
        i = 0
        for datapoint in self.datapoint_button_list:
            if self.timer > i*40//len(self.datapoint_button_list):
                datapoint.Draw(screen)
                if datapoint.radius > 5:
                    datapoint.radius -= 1
            i += 1

    def drawVisualAid(self,screen):
        if self.drawInfo == True:
            self.infoButtonX.Draw(screen,text_anchor=1)
            self.infoButtonY.Draw(screen,text_anchor=1)
            pygame.draw.lines(screen,self.UI.brightGrey,False,[(self.infoButtonX.x_left,self.X_y),(self.infoButtonX.x_left,self.infoButtonY.y_up)],1)
            pygame.draw.lines(screen, self.UI.brightGrey, False,[(self.Y_x, self.infoButtonY.y_up), (self.infoButtonX.x_left, self.infoButtonY.y_up)],1)

    def drawModeButtons(self,screen):
        self.two_weeks_button.Draw(screen,text_anchor=1)
        self.month_button.Draw(screen,text_anchor=1)
        self.six_month_button.Draw(screen,text_anchor=1)

    def redraw(self,screen):
        self.drawBaseline(screen)
        if self.Y_init_y <= self.Y_y_up and self.X_init_x >= self.X_x_right:
            screen.blit(self.UI.myFont14.render("Date", 1, self.UI.brightGrey),
                        (self.UI.width-50, self.X_y-10 ))
            screen.blit(self.UI.myFont14.render("Sentiment value", 1, self.UI.brightGrey),
                        (self.Y_x - 40,30))

            self.timerFited()
            self.drawDatapoints(screen)
            self.drawVisualAid(screen)
            self.drawModeButtons(screen)
            self.drawConnectingLines(screen)

# timerFired #
    def timerFited(self):
        self.timer += 1