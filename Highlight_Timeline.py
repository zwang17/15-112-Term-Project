import Database
import pygame
from datetime import date
import random
from Button import *
import copy

class TimeLine(object):
    def __init__(self):
        self.animation_speed = 6

    def setUI(self,UI):
        self.UI = UI
        self.timelineXLeft = self.UI.MainBarButtonWidth + 60
        self.timelineXRight = self.UI.width - 60
        self.timelineInitX = self.timelineXLeft
        self.timelineLength = self.timelineXRight - self.timelineXLeft
        self.startDate = Database.todayDate()
        self.startDate[1] -= 1
        self.update_display_list(10)
        self.updateBranches()
        self.initModeButtons()
        self.initLeftEndDateButton()

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
                                             self.UI.height - margin , text="Past 6 Months",
                                             font=self.UI.myFont12,
                                             textColor=self.UI.brightGrey)
        self.mode_button_list = [self.two_weeks_button,self.month_button,self.six_month_button]

    def initLeftEndDateButton(self):
        date = self.startDate
        date_str = str(date[0])+"."+str(date[1])+"."+str(date[2])
        self.left_end_data_button = RectButton("left_end_data",self.UI.white,self.timelineXLeft,self.timelineXLeft,self.UI.height/2-20,self.UI.height/2-20,0,date_str,self.UI.myFont12,self.UI.themeColorDark)

    def updateLeftEndDateButton(self):
        date = self.startDate
        date_str = str(date[0]) + "." + str(date[1]) + "." + str(date[2])
        self.left_end_data_button.text = date_str

    def update_display_list(self,num_to_display):
        allDiaries = Database.retreieve_diary_between(self.startDate,Database.todayDate())
        self.display_list = Database.getDiariesWithHighestSentiments(allDiaries,num_to_display)

    def updateSpan(self):
        date = Database.todayDate()
        if self.two_weeks_button.status == True:
            for i in range(14):
                Database.previous_date(date)
                self.startDate = copy.deepcopy(date)
        if self.month_button.status == True:
            for i in range(31):
                Database.previous_date(date)
                self.startDate = copy.deepcopy(date)
        if self.six_month_button.status == True:
            for i in range(365//2):
                Database.previous_date(date)
                self.startDate = copy.deepcopy(date)

        self.update_display_list(10)
        self.updateBranches()
        self.updateLeftEndDateButton()

# mouseMotion #
    def mouseMotion(self,x,y):
        for branch in self.branch:
            branch.mouseMotion(x,y)
        for button in self.mode_button_list:
            if button.WithinRange(x,y) or button.status == True:
                button.textColor = self.UI.themeColorMain
            else:
                button.textColor = self.UI.brightGrey

    def updateBranches(self):
        now = Database.todayDate()
        init = self.startDate
        self.branch = []
        for index in range(len(self.display_list)):
            diary = self.display_list[index]
            total_span = Database.getDeltaDays(now,init)
            diary_span = Database.getDeltaDays(diary.date,init)
            x = self.timelineXLeft + self.timelineLength * diary_span / total_span
            height = random.randint(-200,200)
            if height > 0:
                height += 30
            else:
                height -= 30
            if index > 0:
                while (height>0 and self.branch[index-1].height > 0) or (height<0 and self.branch[index-1].height < 0) :
                    height = random.randint(-200,200)
                    if height > 0: height += 30
                    else:
                        height -= 30
            branch = TimelineBranch(x,diary,height,self.UI)
            self.branch.append(branch)

# mouseReleased #
    def mouseReleased(self,x,y):
        for branch in self.branch:
            branch.mouseReleased(x,y)
        for button in self.mode_button_list:
            if button.WithinRange(x, y):
                for button in self.mode_button_list:
                    if button.WithinRange(x, y):
                        button.status = True
                    else:
                        button.status = False
                self.updateSpan()

# redraw #
    def drawCircle(self,screen,color,x,y,radius,thickness=0):
        pygame.draw.circle(screen,color,(int(x),int(y)),radius,thickness)

    def drawModeButtons(self,screen):
        self.two_weeks_button.Draw(screen,text_anchor=1)
        self.month_button.Draw(screen,text_anchor=1)
        self.six_month_button.Draw(screen,text_anchor=1)

    def drawBaseLine(self,screen):
        circle_radius = 10
        line_y = self.UI.height/2
        if self.timelineInitX < self.timelineXRight:
            self.timelineInitX += self.animation_speed
        self.drawCircle(screen,self.UI.themeColorMain,self.timelineXLeft,line_y,circle_radius,0)
        pygame.draw.lines(screen,self.UI.themeColorMain,False,[(self.timelineXLeft,line_y),(self.timelineInitX,line_y)],2)
        self.drawCircle(screen,self.UI.themeColorMain,self.timelineInitX,line_y,circle_radius,0)
        self.left_end_data_button.Draw(screen,text_anchor=1)

    def redraw(self,screen):
        self.drawBaseLine(screen)
        if self.timelineInitX >= self.timelineXRight:
            for branch in self.branch:
                branch.redraw(screen)
            self.drawModeButtons(screen)

class TimelineBranch(TimeLine):
    def __init__(self,x,diary,height,UI):
        super().__init__()
        self.x = x
        self.diary = diary
        self.height = height
        self.init_height = 0
        self.tags = diary.tags
        self.UI = UI
        self.tag_icon_list = []
        self.loadTags(self.UI)
        self.lineColor = self.UI.themeColorMain
        self.display_date = False
        self.createDateButton()

    def createDateButton(self):
        self.date_width = 30
        self.date_height = 10
        if self.height > 0:
            self.date_y = 300 - 30
        else:
            self.date_y = 300 + 20
        date = self.diary.date
        date_str = str(date[0])+"."+str(date[1])+"."+str(date[2])
        self.hanging_button = RectButton("date_button", self.UI.white, self.x - self.date_width / 2,
                                         self.x + self.date_width / 2, self.date_y, self.date_y + self.date_height, text=date_str,font=self.UI.myFont12,textColor=self.UI.black)
# mouseMotion #
    def mouseMotion(self,x,y):
        for tag in self.tag_icon_list:
            if tag.WithinRange(x,y):
                self.lineColor = (255, 219, 153)
                self.display_date = True
                break
            else:
                self.lineColor = self.UI.themeColorMain
                self.display_date = False

# mouseReleased #
    def mouseReleased(self,x,y):
        for tag in self.tag_icon_list:
            if tag.WithinRange(x, y):
                self.UI.mode = "Edit"
                self.UI.Text_Editor.getDiary(self.diary.date)
                self.UI.Text_Editor.mode = "display"
        # redraw #

    def redraw(self,screen):
        if 0 <= self.init_height <= self.height or self.height <= self.init_height <= 0:
            self.init_height += self.height/15
        self.drawCircle(screen,self.lineColor,self.x,300,8)
        pygame.draw.lines(screen, self.lineColor, False, [(self.x, 300), (self.x, 300+self.init_height)],2)
        self.drawDate(screen)
        if abs(self.init_height) >= abs(self.height)-5:
            for tag in self.tag_icon_list:
                tag.Draw(screen)


    def drawDate(self,screen):
        if self.display_date == True:
            self.hanging_button.Draw(screen,text_anchor=1)

    def loadTags(self, UI):
        tags = self.tags
        tag_size = 35
        init_pos = len(tags)/2

        for index in range(len(tags)):
            x_left = self.x+(-init_pos+index)*tag_size
            x_right = x_left + tag_size
            if self.height > 0:
                y_up = 300 + self.height
                y_down = y_up + tag_size
            else:
                y_down = 300 + self.height
                y_up = y_down - tag_size
            self.newTagButton = RectButton("tag{}".format(index), UI.white, x_left, x_right, y_up, y_down,
                                           0, "", UI.myFont15, UI.brightGrey)
            self.newTagButton.AddIcon("tags\\tag\\" + tags[index], 30, 30, 1 / 2, 1 / 2)
            self.tag_icon_list.append(self.newTagButton)

    def __repr__(self):
        return str(self.x)+','+str(self.diary.date)+','+str(self.height)

