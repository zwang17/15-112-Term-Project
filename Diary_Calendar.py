import datetime
from Button import *

class Calendar(object):
    months = ['December','January','February','March','April','May','June','July','August','September','October','November']
    month_num_day = {'December':31,'January':31,'February':29,'March':31,'April':30,'May':31,'June':30,'July':31,'August':31,'September':30,'October':31,'November':30}
    week_day = ['SUN', 'MON', 'TUE', 'WED', 'THUR', 'FRI', 'SAT']
    def __init__(self):
        self.day_highlighted = [datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day]
        self.current_year_num = datetime.datetime.now().year
        self.current_month_num = datetime.datetime.now().month
        self.current_month = self.months[self.current_month_num]
        self.current_day_num = datetime.datetime.now().day
        self.date_button_list = []
        self.weekday_button_list = []
        self.title_button = None
        self.left_month_button = None
        self.right_month_button = None
        self.left_year_button = None
        self.right_year_button = None

    def getYear(self,diary_name):
        date = diary_name.split('.')
        return date[0]

    def getMonth(self,diary_name):
        date = diary_name.split('.')
        return date[1]

    def getDay(self,diary_name):
        date = diary_name.split('.')
        return date[2]

    def incrementMonth(self,num):
        self.current_month_num += num
        self.current_month_num = self.current_month_num % 12
        self.current_month = self.months[self.current_month_num]

    def createTitleButton(self,UI):
        length = 100
        height = 80
        self.title_button = RectButton("Title",UI.white,(UI.width-length)/2,(UI.width+length)/2,30,30+height,\
                                       margin_width=0,text=self.current_month.upper()+", "+str(self.current_year_num),font=UI.myFont18Bold,textColor=UI.brightGrey)

    def createWeekdayButtons(self,UI):
        for index in range(len(self.week_day)):
            button_width = button_height = 50
            x_gap = 600/7
            x_left = 50+UI.MainBarButtonWidth + x_gap*index + (x_gap-button_width)/2
            x_right = x_left + button_width
            y_up = 100
            y_down = y_up + button_height
            new_weekday_button = RectButton(self.week_day[index],UI.white,x_left,x_right,y_up,y_down,text=self.week_day[index],margin_width=0,font=UI.myFont15Bold,textColor=UI.brightGrey)
            self.weekday_button_list.append(new_weekday_button)

    def createSideYearButtons(self,UI):
        button_width = 50
        button_height = 50
        right_offset = (600/7+50)/2
        left_offset = (600/7-50)/2
        self.left_year_button = RectButton("LeftYearButton", UI.white, 50+UI.MainBarButtonWidth +left_offset, 50+UI.MainBarButtonWidth +left_offset+button_width, 30, 30+button_height,
                                        text=str(self.current_year_num-1), margin_width=0, font=UI.myFont15,
                                        textColor=UI.orange)
        self.right_year_button = RectButton("RightYearButton", UI.white, 1000-(50+UI.MainBarButtonWidth)-right_offset, 1000-(right_offset+UI.MainBarButtonWidth)+button_width-68, 30, 30+button_height,
                                        text=str(self.current_year_num+1), margin_width=0, font=UI.myFont15,
                                        textColor=UI.orange)

    def createSideMonthButtons(self,UI):
        button_width = 50
        button_height = 50
        self.left_month_button = RectButton("LeftMonthButton", UI.white, UI.MainBarButtonWidth , UI.MainBarButtonWidth +button_width, 250, 250+button_height,
                                        text="", margin_width=0, font=UI.myFont15,
                                        textColor=UI.orange)
        self.left_month_button.AddIcon('LeftArrow.png',35,35)
        self.right_month_button = RectButton("RightMonthButton", UI.white, 1000-UI.MainBarButtonWidth-button_width, 1000-UI.MainBarButtonWidth, 250, 250+button_height,
                                        text="", margin_width=0, font=UI.myFont15,
                                        textColor=UI.orange)
        self.right_month_button.AddIcon('RightArrow.png',35,35)


    def createDateButtons(self,UI):
        First_day_weekday = (datetime.datetime(self.current_year_num, self.current_month_num, 1).weekday() + 1) % 7
        self.date_button_list = []
        for day in range(self.month_num_day[self.current_month]):
            button_width = 50
            button_height = 50
            x_gap = 600/7
            y_gap = 60
            x_left = 50+UI.MainBarButtonWidth + x_gap*((First_day_weekday+day)%7) + (x_gap-button_width)/2
            x_right = x_left + button_width
            y_up = 150 + y_gap*((First_day_weekday+day)//7) + (y_gap-button_height)/2
            y_down = y_up + button_height
            new_date_button = RectButton(str(day+1),UI.white,x_left,x_right,y_up,y_down,text=str(day+1),margin_width=0,font=UI.myFont15,textColor=UI.brightGrey)
            self.date_button_list.append(new_date_button)
        if (self.current_year_num, self.current_month_num) == (datetime.datetime.now().year, datetime.datetime.now().month):
            self.date_button_list[datetime.datetime.now().day-1].color = UI.orange
            self.date_button_list[datetime.datetime.now().day - 1].textColor = UI.white

    def Draw(self,screen):
        for dateButton in self.date_button_list:
            dateButton.Draw(screen,text_anchor=1)
        for weekdayButton in self.weekday_button_list:
            weekdayButton.Draw(screen,text_anchor=1)
        self.title_button.Draw(screen,text_anchor=1)
        self.left_year_button.Draw(screen,text_anchor=1)
        self.right_year_button.Draw(screen, text_anchor=1)
        self.left_month_button.Draw(screen)
        self.right_month_button.Draw(screen)

