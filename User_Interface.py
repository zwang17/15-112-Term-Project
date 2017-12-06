import os
import pygame
from Button import *
from threading import Thread
import Database
from PIL import ImageFont
from Reminder import *
import random

class UserInterface(object):

### Init functions ###
    def __init__(self, Voice_Assistant, Text_Editor, Calendar, Timeline, MoodTracker, width=1000, height=600, fps=50,title="Lingo"):
        self.modeList = ['Dashboard','Diary','Highlight','Mood Tracker','Edit']
        self.mode = 'Dashboard'

        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        pygame.init()

        self.Voice_Assistant = Voice_Assistant
        self.Text_Editor = Text_Editor
        self.Calendar = Calendar
        self.Timeline = Timeline
        self.MoodTracker = MoodTracker

        Thread(target=self.initVoiceAssistant).start()
        Thread(target=self.Voice_Assistant.collectBackgroundText).start()

        self.initColor()
        self.initFont()
        self.MainBarButtonWidth = int(self.height/4)
        self.MainBarButtonHeight = int(self.height/11)
        self.MainBarFirstButtonY = self.height/3.5

        self.MainBarButtonDict = {}
        self.initMainBarButtons()
        self.MainBarInitX = 0

    def initVoiceAssistant(self):
        while True:
            try:
                self.Voice_Assistant.runVoiceAssistant(self.Text_Editor)
            except Exception as e:
                print("!!!",end="")
                print(e)
                print("Reinitiating voice assistnat")

    def initColor(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.whiteSmoke = self.hex_to_rgb('#f5f7f7')

        self.blue = (69,160,217)
        self.darkBlue  = (51,87,117)

        self.orange = self.hex_to_rgb("#ff8700")
        self.darkOrange = self.hex_to_rgb("#dd6f0b")

        self.red = self.hex_to_rgb("#df1a06")
        self.darkRed = self.hex_to_rgb("#941a06")

        self.green = (102,204,128)
        self.darkGreen = (0,204,0)

        self.grey = (45, 50, 53)
        self.brightGrey = self.hex_to_rgb('#777c76')

        self.bgColor = self.white

        self.themeColorMain = self.orange
        self.themeColorDark = self.darkOrange

        self.change_color = list(self.grey)
        self.LogoColorDirection = 1
        self.LogoColorSpeed = 3

    def initFont(self):
        font = "zekton rg.ttf"
        self.myFont12 = pygame.font.Font(os.path.join("font", font), 12)
        self.measureFont12 = ImageFont.truetype(os.path.join("font", font),12)  # this function call originally comes from Pillow documentation
        self.myFont14 = pygame.font.Font(os.path.join("font", font), 14)
        self.measureFont14 = ImageFont.truetype(os.path.join("font", font), 14) # this function call originally comes from Pillow documentation
        self.myFont14Bold = pygame.font.Font(os.path.join("font", font), 14)
        self.myFont14Bold.set_bold(True)

        self.myFont15 = pygame.font.Font(os.path.join("font", font), 15)
        self.measureFont15 = ImageFont.truetype(os.path.join("font", font), 15) # this function call originally comes from Pillow documentation
        self.myFont15Bold = pygame.font.Font(os.path.join("font", font), 15)
        self.myFont15Bold.set_bold(True)
        self.myFont18 = pygame.font.Font(os.path.join("font", font), 18)
        self.myFont18Bold = pygame.font.Font(os.path.join("font", font), 18)
        self.myFont18Bold.set_bold(True)
        self.myFont25 = pygame.font.Font(os.path.join("font", font), 25)
        self.myFont20 = pygame.font.Font(os.path.join("font", font), 20)
        self.LogoFont = pygame.font.Font(os.path.join("font", font), 20)
        self.LogoFont.set_bold(True)

    def initThemeButton(self):
        width = height = 40
        gap = 50
        right_offset = 250
        bottom_offset = 80
        self.themeButtonList = []

        self.orangeThemeButton = RectButton("Orange Theme",self.orange,self.width-right_offset,self.width-right_offset+width,self.height-bottom_offset,self.height-bottom_offset+height,0,"",self.myFont14,self.white)
        self.orangeThemeButton.extraColor = self.darkOrange
        marginButton = RectButton("Orange Theme Margin",self.black,self.width-right_offset,self.width-right_offset+width,self.height-bottom_offset,self.height-bottom_offset+height,3,"",self.myFont14,self.white)
        self.orangeThemeButton.marginButton = marginButton
        self.themeButtonList.append(self.orangeThemeButton)

        self.blueThemeButton = RectButton("Blue Theme", self.blue, self.width - right_offset+gap, self.width - right_offset + width+gap,
                                            self.height - bottom_offset, self.height - bottom_offset + height,0,"",self.myFont14,self.white)
        self.blueThemeButton.extraColor = self.darkBlue
        marginButton = RectButton("Blue Theme Margin", self.blue, self.width - right_offset+gap, self.width - right_offset + width+gap,
                                            self.height - bottom_offset, self.height - bottom_offset + height,3,"",self.myFont14,self.white)
        self.blueThemeButton.marginButton = marginButton
        self.themeButtonList.append(self.blueThemeButton)

        self.greenThemeButton = RectButton("Green Theme", self.green, self.width - right_offset+2*gap, self.width - right_offset + width+2*gap,
                                            self.height - bottom_offset, self.height - bottom_offset + height,0,"",self.myFont14,self.white)
        marginButton = RectButton("Green Theme Margin", self.green, self.width - right_offset+2*gap, self.width - right_offset + width+2*gap,
                                            self.height - bottom_offset, self.height - bottom_offset + height,3,"",self.myFont14,self.white)
        self.greenThemeButton.marginButton = marginButton
        self.greenThemeButton.extraColor = self.darkGreen
        self.themeButtonList.append(self.greenThemeButton)

        self.redThemeButton = RectButton("Red Theme", self.red, self.width - right_offset+3*gap, self.width - right_offset + width+3*gap,
                                            self.height - bottom_offset, self.height - bottom_offset + height,0,"",self.myFont14,self.white)
        marginButton = RectButton("Red Theme Margin", self.red, self.width - right_offset+3*gap, self.width - right_offset + width+3*gap,
                                            self.height - bottom_offset, self.height - bottom_offset + height,3,"",self.myFont14,self.white)
        self.redThemeButton.marginButton = marginButton
        self.redThemeButton.extraColor = self.darkRed
        self.themeButtonList.append(self.redThemeButton)

    def initLogoButton(self):
        buttonWidth = self.MainBarButtonWidth * 3 / 4
        buttonHeight = self.MainBarButtonHeight * 4 / 5
        x_left = self.MainBarButtonWidth / 2 - buttonWidth / 2
        y_up = self.MainBarFirstButtonY * 1 / 5
        self.LogoButton = RectButton("LINGO", self.grey, x_left, x_left + buttonWidth, y_up, y_up + buttonHeight,
                                         0, "LINGO", self.LogoFont, self.change_color)

    def initNewDiaryButton(self):
        buttonWidth = self.MainBarButtonWidth * 3 / 4
        buttonHeight = self.MainBarButtonHeight * 4 / 5
        x_left = self.MainBarButtonWidth / 2 - buttonWidth / 2
        y_up = self.MainBarFirstButtonY * 3 / 5
        self.newDiaryButton = RectButton("New Diary",self.brightGrey,x_left,x_left+buttonWidth,y_up,y_up+buttonHeight,1,"New Diary",self.myFont15,self.brightGrey)
        self.newDiaryButton.AddIcon("New Diary.png", 35, 35, 1 / 7, 1 / 2, alter_icon_path="New Diary_white.png")

    def initEditDiaryButton(self):
        buttonWidth = self.MainBarButtonWidth * 3 / 4
        buttonHeight = self.MainBarButtonHeight * 4 / 5
        x_left = self.MainBarButtonWidth / 2 - buttonWidth / 2
        y_up = self.MainBarFirstButtonY * 3 / 5
        self.editDiaryButton = RectButton("Edit Diary",self.brightGrey,x_left,x_left+buttonWidth,y_up,y_up+buttonHeight,1,"Edit Diary",self.myFont15,self.brightGrey)
        self.editDiaryButton.AddIcon("New Diary.png", 35, 35, 1 / 7, 1 / 2, alter_icon_path="New Diary_white.png")

    def initVoiceAssistantButton(self):
        radius = self.MainBarButtonWidth / 6
        center_x = self.MainBarButtonWidth / 2
        center_y = self.height * 6 / 7
        self.voiceAssistantButton = CircButton("Voice Assistnat",self.brightGrey,center_x,center_y,radius,margin_width=5)
        self.voiceAssistantButton.AddIcon("Voice Assistant.png",50,50,alter_icon_path="Voice Assistant_white.png")
        self.voiceAssistantButton.AddExtraIcon("Voice Assistant_speaking.png",50,50)

    def initMainBarButtons(self):
        mode = self.modeList
        for index in range(len(mode)-1):
            x_left = 0
            x_right = self.MainBarButtonWidth
            y_up = self.MainBarFirstButtonY + index * self.MainBarButtonHeight
            y_down = y_up + self.MainBarButtonHeight
            self.MainBarButtonDict[mode[index]] = RectButton(mode[index],self.grey,x_left,x_right,y_up,y_down,0,mode[index],self.myFont14,self.white)
            self.MainBarButtonDict[mode[index]].AddIcon(mode[index]+".png",35,35,1/6.5,1/2,alter_icon_path=mode[index]+"_white.png")

        self.initLogoButton()
        self.initNewDiaryButton()
        self.initEditDiaryButton()
        self.initVoiceAssistantButton()


    def initDashboardReminder(self):
        date = Database.todayDate()
        self.today_reminder = Database.retrieve_reminder(date)
        if self.today_reminder == None:
            self.today_reminder = Reminder(Database.todayDate())
        self.today_reminder.updateReminderButtons(self.white, self.MainBarButtonWidth + 50, 80, self.myFont14Bold, self.measureFont14, self.brightGrey,180)

    def initReminder(self):
        date = Database.todayDate()
        self.reminder = Database.retrieve_reminder(date)
        if self.reminder != None:
            self.reminder.updateReminderButtons(self.grey, self.width - self.MainBarButtonWidth + 5, 50,
                                    self.myFont12, self.measureFont12, self.brightGrey, 90)
        else:
            self.reminder = Reminder(date)

    def updateReminder(self,date):
        self.reminder = Database.retrieve_reminder(date)
        if self.reminder != None:
            self.reminder.updateReminderButtons(self.grey, self.width - self.MainBarButtonWidth + 5, 50,
                                            self.myFont12, self.measureFont12, self.brightGrey, 90)

    def initTodayTags(self):
        self.today_diary = Database.retrieve_diary(Database.todayDate())
        self.today_tag_list = []
        if self.today_diary == None:
            return None
        tags = self.today_diary.tags
        tag_size = 35
        init_pos = len(tags)/2
        for index in range(len(tags)):
            x_left = self.width-200+(-init_pos+index)*tag_size
            x_right = x_left + tag_size
            y_up = 100
            y_down = y_up + tag_size
            self.newTagButton = RectButton("tag{}".format(index), self.white, x_left, x_right, y_up, y_down,
                                           0, "", self.myFont15, self.brightGrey)
            self.newTagButton.AddIcon("tags\\tag\\" + tags[index], 30, 30, 1 / 2, 1 / 2)
            self.today_tag_list.append(self.newTagButton)

    def init(self):
        self.Text_Editor.initAllButtons()
        self.Calendar.initAllButtons()
        self.MoodTracker.updateAllButtons()
        self.initDashboardReminder()
        self.initReminder()
        self.initTodayTags()
        self.initThemeButton()
    
### Helper functions ###
    def click_within(self,x_left,x_right,y_up,y_down,x,y):
        return x_left<x<x_right and y_up<y<y_down

    def hex_to_rgb(self, value):
        """
        This helper function is cited from stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
        """
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#########################
### Main Framework ######
#########################

### keyPressed ###
    def keyPressed(self,key,mod):
        if self.mode == "Diary":
            self.Calendar.keyPressed(key,mod)
        if self.mode == "Edit":
            self.Text_Editor.keyPressed(key,mod)
### keyReleased ###
    def keyReleased(self,x,y):
        pass

### mouseDrag ###
    def mouseDrag(self,x,y):
        pass

### mousePressed ###

    def mousePressedMainBar(self,x,y):
        # mousePressed of mode buttons
        for buttonName in self.MainBarButtonDict:
            button = self.MainBarButtonDict[buttonName]
            if button.WithinRange(x,y):
                button.color = self.themeColorDark
                button.textColor = self.white
        self.Voice_Assistant.mousePressed(x,y)

    def mousePressedDiary(self,x,y):
        self.Calendar.mousePressed(x,y)

    def mousePressed(self,x,y):
        self.mousePressedMainBar(x,y)
        if self.mode == "Diary":
            self.mousePressedDiary(x,y)

### mouseReleased ###
    def mouseReleasedNewDiaryButton(self):
        self.mode = "Edit"
        self.Text_Editor.mode = "edit"
        self.Voice_Assistant.runDiaryListener()
        if Database.retrieve_diary(Database.todayDate()) == None:
            self.Text_Editor.createNewDiary()
        else:
            self.Text_Editor.getDiary(Database.todayDate())

    def mouseReleasedMainBar(self,x,y):
        for buttonName in self.MainBarButtonDict:
            button = self.MainBarButtonDict[buttonName]
            if button.WithinRange(x, y):
                button.color = self.themeColorMain
                button.textColor = self.white
                self.mode = buttonName
                if self.mode == "Diary":
                    if self.Calendar.getCurrentDate() == Database.todayDate():
                        self.updateReminder(self.Calendar.getCurrentDate())
                if self.mode == "Dashboard":
                    self.initDashboardReminder()

        self.Voice_Assistant.mouseReleased(x,y)
        if self.newDiaryButton.WithinRange(x,y):
            self.mouseReleasedNewDiaryButton()
        self.mouseMotionMainBar(x,y)
        print(self.mode)

    def mouseReleasedDashboard(self,x,y):
        for button in self.themeButtonList:
            if button.WithinRange(x,y):
                self.themeColorMain = button.color
                self.themeColorDark = button.extraColor
                self.MoodTracker.update_data_list()
                self.MoodTracker.initModeButtons()
                self.Calendar.createEditDiaryButton()
                self.Timeline.initLeftEndDateButton()
        self.mouseMotionDashboard(x,y)

        if self.today_reminder == None: return None
        self.today_reminder.mouseReleased(x,y)
        self.mouseMotionDashboard(x,y)

    def mouseReleasedEdit(self,x,y):
        self.Text_Editor.mouseReleased(x,y)

    def mouseReleasedDiary(self,x,y):
        if self.reminder != None:
            self.reminder.mouseReleased(x,y)
        self.Calendar.mouseReleased(x,y)
        self.mouseMotionDiary(x,y)

    def mouseReleasedHighlight(self,x,y):
        self.Timeline.mouseReleased(x,y)

    def mouseReleasedMoodTracke(self,x,y):
        self.MoodTracker.mouseReleased(x,y)

    def mouseReleased(self,x,y):
        self.mouseReleasedMainBar(x,y)
        if self.mode == 'Edit':
            self.mouseReleasedEdit(x,y)
        if self.mode == "Diary":
            self.mouseReleasedDiary(x,y)
        if self.mode == "Dashboard":
            self.mouseReleasedDashboard(x,y)
        if self.mode == "Highlight":
            self.mouseReleasedHighlight(x,y)
        if self.mode == "Mood Tracker":
            self.mouseReleasedMoodTracke(x,y)

### mouseMotion ###

    def mouseMotionMainBar(self,x,y):
        # mouseMotion of mode buttons
        for buttonName in self.MainBarButtonDict:
            button = self.MainBarButtonDict[buttonName]
            if button.WithinRange(x,y):
                button.color = self.themeColorMain
                button.textColor = self.white
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.grey
                button.textColor = self.brightGrey
                button.displayed_icon = button.icon

        # mouseMotion of new diary button
        button = self.newDiaryButton
        if button.WithinRange(x,y):
            button.color = self.themeColorMain
            button.textColor= self.white
            button.displayed_icon = button.alter_icon
        else:
            button.color = self.brightGrey
            button.textColor = self.brightGrey
            button.displayed_icon = button.icon

        button = self.editDiaryButton
        if button.WithinRange(x, y):
            button.color = self.themeColorMain
            button.textColor = self.white
            button.displayed_icon = button.alter_icon
        else:
            button.color = self.brightGrey
            button.textColor = self.brightGrey
            button.displayed_icon = button.icon

        # mouseMotion of voice assistant button
        self.Voice_Assistant.mouseMotion(x,y)

    def mouseMotionDashboard(self,x,y):
        for button in self.themeButtonList:
            if button.color == self.themeColorMain:
                button.marginButton.color = self.black
            elif button.WithinRange(x,y):
                button.marginButton.color = self.brightGrey
            else:
                button.marginButton.color = button.color

        if self.today_reminder == None: return None
        self.today_reminder.mouseMotion(x,y)

    def mouseMotionEdit(self,x,y):
        self.Text_Editor.mouseMotion(x,y)

    def mouseMotionDiary(self,x,y):
        self.Calendar.mouseMotion(x,y)
        if self.reminder == None: return None
        self.reminder.mouseMotion(x,y)

    def mouseMotionHighlight(self,x,y):
        self.Timeline.mouseMotion(x,y)

    def mouseMotionMoodTracker(self,x,y):
        self.MoodTracker.mouseMotion(x,y)

    def mouseMotion(self,x,y):
        self.mouseMotionMainBar(x,y)
        if self.mode == "Dashboard":
            self.mouseMotionDashboard(x,y)
        if self.mode == "Edit":
            self.mouseMotionEdit(x,y)
        if self.mode == "Diary":
            self.mouseMotionDiary(x,y)
        if self.mode == 'Highlight':
            self.mouseMotionHighlight(x,y)
        if self.mode == 'Mood Tracker':
            self.mouseMotionMoodTracker(x,y)

### timerFired ###

    def timerFired(self,time):
        self.Voice_Assistant.timerFired()
        index = random.randint(0, 2)
        if self.change_color[index] > 254:
            self.LogoColorDirection = -1
        if self.change_color[index] < 1:
            self.LogoColorDirection = 1
        self.change_color[index] += self.LogoColorDirection * self.LogoColorSpeed
        if self.change_color[index] > 255:
            self.change_color[index] = 255
        if self.change_color[index] < 0:
            self.change_color[index] = 0
        if self.mode == 'Diary':
            self.Calendar.timerFiredSideBar()
        # if self.mode == "Mood Tracker":
        #     self.MoodTracker.timerFited()

### redraw ###
    def drawMainBar(self,screen):
        # Draw main bar
        if self.MainBarInitX < self.MainBarButtonWidth:
            self.MainBarInitX += 5
        pygame.draw.rect(screen, self.grey, (0, 0, self.MainBarInitX, self.height), 0)

    def drawMainBarButtons(self,screen):
        # Draw each mode button
        for button in self.MainBarButtonDict:
            self.MainBarButtonDict[button].Draw(screen,text_width_coef=1/4)
        # Draw new diary button
        if self.today_diary == None:
            self.newDiaryButton.Draw(screen,1,1/1.7)
        else:
            # continuing editing today's diary
            self.editDiaryButton.Draw(screen,1,1/1.7)
        self.LogoButton.Draw(screen,text_anchor=1)

    def redrawMainBar(self,screen):
        self.drawMainBar(screen)
        if self.MainBarInitX < self.MainBarButtonWidth:
            return None
        self.drawMainBarButtons(screen)
        self.Voice_Assistant.redraw(screen)
        last_button_y = self.MainBarButtonDict["Mood Tracker"].y_down + 5
        pygame.draw.line(screen,self.brightGrey,(self.MainBarButtonWidth*0.15,last_button_y),(self.MainBarButtonWidth*0.85,last_button_y),1)

    def drawDashboardTitles(self,screen):
        line = "To-do List"
        screen.blit(self.myFont18Bold.render(line, 1, self.themeColorMain),
                    (self.MainBarButtonWidth+60, 50))
        line = "Today's Diary"
        screen.blit(self.myFont18Bold.render(line, 1, self.themeColorMain),
                    (self.width - 260, 50))

    def redrawDashboard(self,screen):
        self.drawDashboardTitles(screen)
        for button in self.themeButtonList:
            button.Draw(screen)
            button.marginButton.Draw(screen)
        for tag in self.today_tag_list:
            tag.Draw(screen)
        if self.today_reminder == None: return None
        self.today_reminder.Draw(screen)

    def redrawEdit(self,screen):
        self.Text_Editor.redraw(screen)

    def redrawHighlight(self,screen):
        self.Timeline.redraw(screen)

    def redrawDiary(self,screen):
        self.Calendar.redraw(screen)
        if self.Calendar.calendarSideBarWidth >= self.MainBarButtonWidth and self.reminder != None:
            self.reminder.Draw(screen,1/5)

    def redrawMoodTracker(self,screen):
        self.MoodTracker.redraw(screen)

    def redrawAll(self,screen):
        self.redrawMainBar(screen)
        if self.mode == "Dashboard":
            self.redrawDashboard(screen)
        if self.mode == "Edit":
            self.redrawEdit(screen)
        if self.mode == "Diary":
            self.redrawDiary(screen)
        if self.mode == "Highlight":
            self.redrawHighlight(screen)
        if self.mode == "Mood Tracker":
            self.redrawMoodTracker(screen)

### update ###
    def VoiceAssistantButtonUpdate(self):
        button = self.voiceAssistantButton
        if self.Voice_Assistant.va_activated == True:
            button.color = self.white
            button.displayed_icon = button.extra_icon

    def TextEditorUpdate(self):
        if self.mode == "Edit":
            if self.Text_Editor.mode == "edit":
                self.Voice_Assistant.dl_activated = True
                self.Text_Editor.updateDiary(self.Voice_Assistant)
        if self.mode != "Edit":
            self.Text_Editor.mode = "display"
        if self.Text_Editor.mode == "display":
            self.Voice_Assistant.dl_activated = False

    def UpdateAll(self):
        self.VoiceAssistantButtonUpdate()
        self.TextEditorUpdate()

    def run(self):
        """
        This function is cited from a HACK112 project that I was a part of
        """
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
        self.init()

        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            self.UpdateAll()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                              event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()

