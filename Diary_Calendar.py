import datetime
from Button import *
import Database

class Calendar(object):
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month_num_day = {'January':31,'February':29,'March':31,'April':30,'May':31,'June':30,'July':31,'August':31,'September':30,'October':31,'November':30,'December':31}
    week_day = ['SUN', 'MON', 'TUE', 'WED', 'THUR', 'FRI', 'SAT']
    def __init__(self):
        self.day_highlighted = [datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day]
        self.current_year_num = datetime.datetime.now().year
        self.current_month_num = datetime.datetime.now().month
        self.current_day_num = datetime.datetime.now().day
        self.current_month = self.months[self.current_month_num-1]
        self.date_button_list = []
        self.weekday_button_list = []
        self.calendarSideBarWidth = 0
        self.title_button = None
        self.left_month_button = None
        self.right_month_button = None
        self.left_year_button = None
        self.right_year_button = None
        self.reminders_button = None

    def setUI(self,UI):
        self.UI = UI
        self.initReminderButton()

    def getCurrentDate(self):
        return [self.current_year_num,self.current_month_num,self.current_day_num]

    def incrementMonth(self,num):
        self.current_month_num += num
        if self.current_month_num == 13:
            self.current_month_num = 1
            self.current_year_num += 1
        if self.current_month_num == 0:
            self.current_month_num = 12
            self.current_year_num -= 1
        self.current_month = self.months[self.current_month_num-1]

    def timerFiredSideBar(self):
        if self.calendarSideBarWidth < self.UI.MainBarButtonWidth:
            self.calendarSideBarWidth += 5

    def initReminderButton(self):
        width = 80
        height = 40
        self.reminders_button = RectButton("Reminders", self.UI.grey, self.UI.width - (self.UI.MainBarButtonWidth- width) / 2-width,
                                           self.UI.width - (self.UI.MainBarButtonWidth - width) / 2, 20, 20 + height, \
                                       margin_width=0,
                                       text="Reminders",
                                       font=self.UI.myFont18Bold, textColor=self.UI.brightGrey)

    def updateTitleButton(self):
        length = 100
        height = 80
        self.current_month = self.months[self.current_month_num-1]
        self.title_button = RectButton("Title",self.UI.white,(self.UI.width-length)/2,(self.UI.width+length)/2,30,30+height,\
                                       margin_width=0,text=self.current_month.upper()+", "+str(self.current_year_num),font=self.UI.myFont18Bold,textColor=self.UI.brightGrey)

    def createTodayButton(self):
        self.todayButton = RectButton("Today",self.UI.white,600,670,550,580,0,"TODAY",self.UI.myFont15Bold,self.UI.brightGrey)

    def createWeekdayButtons(self):
        for index in range(len(self.week_day)):
            button_width = button_height = 50
            x_gap = 600/7
            x_left = 50+self.UI.MainBarButtonWidth + x_gap*index + (x_gap-button_width)/2
            x_right = x_left + button_width
            y_up = 100
            y_down = y_up + button_height
            new_weekday_button = RectButton(self.week_day[index],self.UI.white,x_left,x_right,y_up,y_down,text=self.week_day[index],margin_width=0,font=self.UI.myFont15Bold,textColor=self.UI.brightGrey)
            self.weekday_button_list.append(new_weekday_button)

    def updateSideYearButtons(self):
        button_width = 50
        button_height = 50
        right_offset = (600/7+50)/2
        left_offset = (600/7-50)/2
        self.left_year_button = RectButton("LeftYearButton", self.UI.white, 50+self.UI.MainBarButtonWidth +left_offset, 50+self.UI.MainBarButtonWidth +left_offset+button_width, 30, 30+button_height,
                                        text=str(self.current_year_num-1), margin_width=0, font=self.UI.myFont15,
                                        textColor=self.UI.themeColorMain)
        self.right_year_button = RectButton("RightYearButton", self.UI.white, 1000-(50+self.UI.MainBarButtonWidth)-right_offset, 1000-(right_offset+self.UI.MainBarButtonWidth)+button_width-68, 30, 30+button_height,
                                        text=str(self.current_year_num+1), margin_width=0, font=self.UI.myFont15,
                                        textColor=self.UI.themeColorMain)

    def createSideMonthButtons(self):
        button_width = 50
        button_height = 50
        self.left_month_button = RectButton("LeftMonthButton", self.UI.white, self.UI.MainBarButtonWidth , self.UI.MainBarButtonWidth +button_width, 250, 250+button_height,
                                        text="", margin_width=0, font=self.UI.myFont15,
                                        textColor=self.UI.themeColorMain)
        self.left_month_button.AddIcon('LeftArrow.png',35,35)
        self.right_month_button = RectButton("RightMonthButton", self.UI.white, 1000-self.UI.MainBarButtonWidth-button_width, 1000-self.UI.MainBarButtonWidth, 250, 250+button_height,
                                        text="", margin_width=0, font=self.UI.myFont15,
                                        textColor=self.UI.themeColorMain)
        self.right_month_button.AddIcon('RightArrow.png',35,35)

    def updateDateButtons(self):
        First_day_weekday = (datetime.datetime(self.current_year_num, self.current_month_num, 1).weekday() + 1) % 7
        self.date_button_list = []
        for day in range(self.month_num_day[self.current_month]):
            button_width = 50
            button_height = 50
            x_gap = 600/7
            y_gap = 60
            x_left = 50+self.UI.MainBarButtonWidth + x_gap*((First_day_weekday+day)%7) + (x_gap-button_width)/2
            x_right = x_left + button_width
            y_up = 150 + y_gap*((First_day_weekday+day)//7) + (y_gap-button_height)/2
            y_down = y_up + button_height
            new_date_button = RectButton(str(day+1),self.UI.white,x_left,x_right,y_up,y_down,text=str(day+1),margin_width=0,font=self.UI.myFont15,textColor=self.UI.brightGrey)
            self.date_button_list.append(new_date_button)
        if (self.current_year_num, self.current_month_num) == (datetime.datetime.now().year, datetime.datetime.now().month):
            self.date_button_list[datetime.datetime.now().day-1].color = self.UI.themeColorMain
            self.date_button_list[datetime.datetime.now().day - 1].textColor = self.UI.white

    def createEditDiaryButton(self):
        width = 110
        x_left = self.UI.width - (self.UI.MainBarButtonWidth-width)/2-width
        x_right = x_left + width
        y_up = 500
        y_down = 540
        self.edit_diary_button = RectButton("edit", self.UI.themeColorMain, x_left,
                                       x_right, y_up,y_down, \
                                       margin_width=1,
                                       text="Check Diary",
                                       font=self.UI.myFont15Bold, textColor=self.UI.themeColorMain)

    def updateButtons(self):
        self.updateTitleButton()
        self.updateDateButtons()
        self.updateSideYearButtons()

    def initAllButtons(self):
        self.updateDateButtons()
        self.createWeekdayButtons()
        self.updateTitleButton()
        self.updateSideYearButtons()
        self.createSideMonthButtons()
        self.createEditDiaryButton()
        self.createTodayButton()

# mouseMotion #
    def mouseMotion(self,x,y):
        dateButtonList = self.date_button_list
        for index in range(len(dateButtonList)):
            if ((self.current_year_num,self.current_month_num) == (self.day_highlighted[0],self.day_highlighted[1]) and index + 1 == self.current_day_num):
                dateButtonList[index].color = self.UI.themeColorMain
                dateButtonList[index].textColor = self.UI.white
            elif dateButtonList[index].WithinRange(x,y):
                dateButtonList[index].color = self.UI.themeColorMain
                dateButtonList[index].textColor = self.UI.white
            else:
                dateButtonList[index].color = self.UI.white
                dateButtonList[index].textColor = self.UI.brightGrey
        if self.left_year_button.WithinRange(x,y):
            self.left_year_button.textColor = self.UI.brightGrey
        else:
            self.left_year_button.textColor = self.UI.themeColorMain
        if self.right_year_button.WithinRange(x,y):
            self.right_year_button.textColor = self.UI.brightGrey
        else:
            self.right_year_button.textColor = self.UI.themeColorMain
        if self.left_month_button.WithinRange(x,y):
            self.left_month_button.color = self.UI.brightGrey
        else:
            self.left_month_button.color = self.UI.white
        if self.right_month_button.WithinRange(x,y):
            self.right_month_button.color = self.UI.brightGrey
        else:
            self.right_month_button.color = self.UI.white
        if self.edit_diary_button.WithinRange(x,y):
            self.edit_diary_button.textColor = self.UI.white
        else:
            self.edit_diary_button.textColor = self.UI.themeColorMain
        if self.todayButton.WithinRange(x,y):
            self.todayButton.textColor = self.UI.white
            self.todayButton.color = self.UI.themeColorMain
        else:
            self.todayButton.textColor = self.UI.brightGrey
            self.todayButton.color = self.UI.white

    def mousePressed(self,x,y):
        if self.todayButton.WithinRange(x,y):
            self.todayButton.color = self.UI.themeColorDark

# mouseReleased #
    def mouseReleased(self,x,y):
        dateButtonList = self.date_button_list
        if self.left_month_button.WithinRange(x, y):
            self.incrementMonth(-1)
        if self.right_month_button.WithinRange(x, y):
            self.incrementMonth(1)
        if self.left_year_button.WithinRange(x, y):
            self.current_year_num -= 1
        if self.right_year_button.WithinRange(x, y):
            self.current_year_num += 1
        for index in range(len(dateButtonList)):
            if dateButtonList[index].WithinRange(x, y):
                self.current_day_num = index + 1
                self.day_highlighted[0] = self.current_year_num
                self.day_highlighted[1] = self.current_month_num
                self.mouseMotion(x, y)
                self.UI.updateReminder(self.getCurrentDate())
        self.updateButtons()
        button = self.edit_diary_button
        if button.WithinRange(x, y):
            if Database.retrieve_diary(self.getCurrentDate()) != None:
                self.UI.Text_Editor.getDiary(self.getCurrentDate())
                self.UI.mode = "Edit"
                self.UI.Text_Editor.mode = "display"
        self.mouseMotion(x, y)
        if self.todayButton.WithinRange(x,y):
            now_date = Database.todayDate()
            self.current_year_num,self.current_month_num,self.current_day_num = now_date[0],now_date[1],now_date[2]
            print(self.current_year_num,self.current_month_num,self.current_day_num )
            self.updateButtons()

    # redraw #
    def drawRightBar(self,screen):
        pygame.draw.rect(screen, self.UI.grey, (self.UI.width-self.calendarSideBarWidth, 0, self.UI.width-self.calendarSideBarWidth, self.UI.height), 0)

    def drawEditButton(self,screen):
        self.edit_diary_button.Draw(screen,text_anchor=1)
        
    def drawRemindersButton(self,screen):
        self.reminders_button.Draw(screen,text_anchor=1)

    def redraw(self,screen):
        for dateButton in self.date_button_list:
            dateButton.Draw(screen,text_anchor=1)
        for weekdayButton in self.weekday_button_list:
            weekdayButton.Draw(screen,text_anchor=1)
        self.title_button.Draw(screen,text_anchor=1)
        self.left_year_button.Draw(screen,text_anchor=1)
        self.right_year_button.Draw(screen, text_anchor=1)
        self.left_month_button.Draw(screen)
        self.right_month_button.Draw(screen)
        self.drawRightBar(screen)
        if self.calendarSideBarWidth >= self.UI.MainBarButtonWidth:
            self.drawRemindersButton(screen)
        if self.calendarSideBarWidth >= self.UI.MainBarButtonWidth and Database.retrieve_diary(self.getCurrentDate()) != None:
            self.drawEditButton(screen)
        self.todayButton.Draw(screen,text_anchor=1)


