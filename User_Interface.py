import os
import pygame
from Button import *
from threading import Thread
import Database

class UserInterface(object):

### Init functions ###
    def __init__(self, Voice_Assistant, Text_Editor, Calendar, width=900, height=600, fps=80,title=""):
        self.timer = 0
        self.VA_refresh_time = 1500

        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        pygame.init()
        self.Voice_Assistant = Voice_Assistant
        self.Text_Editor = Text_Editor
        self.Calendar = Calendar

### offline
#        Thread(target=self.initVoiceAssistant).start()

    def initVoiceAssistant(self):
        self.Voice_Assistant.runVoiceAssistant(self.Text_Editor)

    def initColor(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.whiteSmoke = self.hex_to_rgb('#f5f7f7')
        self.lightGreen = self.hex_to_rgb("#6dcfcc")
        self.lightBlue = self.hex_to_rgb("#d7f7fd")
        self.blue = (69,160,217)
        self.deepBlue= (68,118,192)
        self.darkBlue  = (51,87,117)
        self.green = self.hex_to_rgb("#44ab29")
        self.deepGreen = self.hex_to_rgb("#35830a")
        self.red = self.hex_to_rgb("#df1a06")
        self.darkRed = self.hex_to_rgb("#941a06")
        self.blueGray = self.hex_to_rgb("#4b637d")
        self.deepBlueGray = self.hex_to_rgb("#2e3242")
        self.darkBlueGray = self.hex_to_rgb("#1b2331")
        self.grey = self.hex_to_rgb("#2d3235")
        self.brightGrey = self.hex_to_rgb('#777c76')
        self.orange = self.hex_to_rgb("#ff8700")
        self.darkOrange = self.hex_to_rgb("#dd6f0b")
        self.deepOrange = self.hex_to_rgb("#c16112")

        self.bgColor = self.white

    def initFont(self):
        font = "zekton rg.ttf"
        self.myFont12 = pygame.font.Font(os.path.join("font", font), 12)
        self.myFont14 = pygame.font.Font(os.path.join("font", font), 14)
        self.myFont15 = pygame.font.Font(os.path.join("font", font), 15)
        self.myFont25 = pygame.font.Font(os.path.join("font", font), 25)
        self.myFont20 = pygame.font.Font(os.path.join("font", font), 20)

    def initNewDiaryButton(self):
        buttonWidth = self.MainBarButtonWidth * 3 / 4
        buttonHeight = self.MainBarButtonHeight * 4 / 5
        x_left = self.MainBarButtonWidth / 2 - buttonWidth / 2
        y_up = self.MainBarFirstButtonHeight * 3 / 5
        self.newDiaryButton = RectButton("New Diary",self.brightGrey,x_left,x_left+buttonWidth,y_up,y_up+buttonHeight,1,"New Diary",self.myFont15,self.brightGrey)
        self.newDiaryButton.AddIcon("New Diary.png", 35, 35, 1 / 7, 1 / 2, alter_icon_path="New Diary_white.png")


    def initEditDiaryButton(self):
        buttonWidth = self.MainBarButtonWidth * 3 / 4
        buttonHeight = self.MainBarButtonHeight * 4 / 5
        x_left = self.MainBarButtonWidth / 2 - buttonWidth / 2
        y_up = self.MainBarFirstButtonHeight * 3 / 5
        self.editDiaryButton = RectButton("Edit Diary",self.brightGrey,x_left,x_left+buttonWidth,y_up,y_up+buttonHeight,1,"Edit Diary",self.myFont15,self.brightGrey)
        self.editDiaryButton.AddIcon("New Diary.png", 35, 35, 1 / 7, 1 / 2, alter_icon_path="New Diary_white.png")

    def initVoiceAssistantButton(self):
        radius = self.MainBarButtonWidth / 6
        center_x = self.MainBarButtonWidth * 4 / 10
        center_y = self.height * 6 / 7
        self.voiceAssistantButton = CircButton("Voice Assistnat",self.brightGrey,center_x,center_y,radius,margin_width=5)
        self.voiceAssistantButton.AddIcon("Voice Assistant.png",50,50,alter_icon_path="Voice Assistant_white.png")
        self.voiceAssistantButton.AddExtraIcon("Voice Assistant_speaking.png",50,50)
        self.Voice_Assistant.button = self.voiceAssistantButton


    def initDiarySaveButton(self):
        buttonWidth = self.MainBarButtonWidth * 3 / 5
        buttonHeight = self.MainBarButtonHeight * 1 / 2
        x_left = self.width - buttonWidth * 2
        y_up = self.height - 30
        self.diarySaveButton = RectButton("Save", self.brightGrey, x_left, x_left + buttonWidth, y_up,
                                         y_up + buttonHeight, 1, "Save", self.myFont15, self.brightGrey)
        self.diarySaveButton.AddIcon("Save.png", 35, 35, 1 / 4, 1 / 2, alter_icon_path="Save_black.png")

    def initDiaryEditButton(self):
        buttonWidth = self.MainBarButtonWidth * 3 / 5
        buttonHeight = self.MainBarButtonHeight * 1 / 2
        x_left = self.width - buttonWidth * 2
        y_up = self.height - 30
        self.diaryEditButton = RectButton("Edit", self.brightGrey, x_left, x_left + buttonWidth, y_up,
                                         y_up + buttonHeight, 1, "Edit", self.myFont15, self.brightGrey)
        self.diaryEditButton.AddIcon("Edit.png", 35, 35, 1 / 4, 1 / 2, alter_icon_path="Edit_black.png")

    def initEditButton(self):
        self.initDiarySaveButton()

    def initMainBarButtons(self):
        mode = self.modeList
        for index in range(len(mode)-1):
            x_left = 0
            x_right = self.MainBarButtonWidth
            y_up = self.MainBarFirstButtonHeight + index * self.MainBarButtonHeight
            y_down = y_up + self.MainBarButtonHeight
            self.MainBarButtonDict[mode[index]] = RectButton(mode[index],self.grey,x_left,x_right,y_up,y_down,0,mode[index],self.myFont14,self.white)
            self.MainBarButtonDict[mode[index]].AddIcon(mode[index]+".png",35,35,1/6.5,1/2,alter_icon_path=mode[index]+"_white.png")

        self.initNewDiaryButton()
        self.initEditDiaryButton()
        self.initVoiceAssistantButton()

    def init(self):
        self.initColor()
        self.initFont()
        self.MainBarButtonWidth = self.height/4
        self.MainBarButtonHeight = self.height/11
        self.MainBarFirstButtonHeight = self.height/3.5
        self.modeList = ['Dashboard','Diary','Highlight','Mood Tracker','Trash','Edit']
        self.mode = 'Dashboard'
        self.MainBarButtonDict = {}
        self.initMainBarButtons()
        self.initEditButton()

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
    def keyPressed(self,x,y):
        pass

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
                button.color = self.darkOrange
                button.textColor = self.white

    def mousePressed(self,x,y):
        self.mousePressedMainBar(x,y)

### mouseReleased ###
    def mouseReleasedMainBar(self,x,y):
        for buttonName in self.MainBarButtonDict:
            button = self.MainBarButtonDict[buttonName]
            if button.WithinRange(x, y):
                button.color = self.orange
                button.textColor = self.white
                self.mode = buttonName
        if self.voiceAssistantButton.WithinRange(x, y):
            self.voiceAssistantButton.color = self.white
            self.voiceAssistantButton.displayed_icon = self.voiceAssistantButton.extra_icon
            if self.Voice_Assistant.activated == False:
                self.Voice_Assistant.activate()
            else:
                self.Voice_Assistant.deactivate()
        if self.newDiaryButton.WithinRange(x,y):
            self.mode = "Edit"
            self.Text_Editor.mode = "edit"
            Thread(target=self.Voice_Assistant.runDiaryListener).start()
            self.Text_Editor.status = True
            if Database.retrieve_diary(Database.todayDate()) == None:
                self.Text_Editor.createNewDiary()
            else:
                self.Text_Editor.getDiary(Database.todayDate())
        print(self.mode)

    def mouseReleasedEdit(self,x,y):
        if self.Text_Editor.mode == "edit":
            button = self.diarySaveButton
            if button.WithinRange(x, y):
                Database.save_diary(self.Text_Editor.Diary)

    def mouseReleased(self,x,y):
        self.mouseReleasedMainBar(x,y)
        if self.mode == 'Edit':
            self.mouseReleasedEdit(x,y)

### mouseMotion ###

    def mouseMotionMainBar(self,x,y):
        # mouseMotion of mode buttons
        for buttonName in self.MainBarButtonDict:
            button = self.MainBarButtonDict[buttonName]
            if button.WithinRange(x,y):
                button.color = self.orange
                button.textColor = self.white
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.grey
                button.textColor = self.brightGrey
                button.displayed_icon = button.icon

        # mouseMotion of new diary button
        button = self.newDiaryButton
        if button.WithinRange(x,y):
            button.color = self.orange
            button.textColor= self.white
            button.displayed_icon = button.alter_icon
        else:
            button.color = self.brightGrey
            button.textColor = self.brightGrey
            button.displayed_icon = button.icon

        button = self.editDiaryButton
        if button.WithinRange(x, y):
            button.color = self.orange
            button.textColor = self.white
            button.displayed_icon = button.alter_icon
        else:
            button.color = self.brightGrey
            button.textColor = self.brightGrey
            button.displayed_icon = button.icon

        # mouseMotion of voice assistant button
        button = self.voiceAssistantButton
        if button.status == False:
            if button.WithinRange(x,y):
                button.color = self.white
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.brightGrey
                button.displayed_icon = button.icon

    def mouseMotionEdit(self,x,y):
        if self.Text_Editor.mode == "edit":
            button = self.diarySaveButton
            if button.WithinRange(x, y):
                button.color = self.orange
                button.textColor = self.orange
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.brightGrey
                button.textColor = self.brightGrey
                button.displayed_icon = button.icon
        if self.Text_Editor.mode == "display":
            button = self.diaryEditButton
            if button.WithinRange(x, y):
                button.color = self.orange
                button.textColor = self.orange
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.brightGrey
                button.textColor = self.brightGrey
                button.displayed_icon = button.icon


    def mouseMotion(self,x,y):
        self.mouseMotionMainBar(x,y)
        if self.mode == "Edit":
            self.mouseMotionEdit(x,y)

    ### timerFired ###
    def timerFired(self,time):
        self.timer += 1
        if self.VA_refresh_time == self.timer:
            self.Voice_Assistant.refresh()
            self.timer = 0

### redraw ###
    def drawMainBar(self,screen):
        # Draw main bar
        pygame.draw.rect(screen, self.grey, (0, 0, self.MainBarButtonWidth, self.height), 0)

    def drawMainBarButtons(self,screen):
        # Draw each mode button
        for button in self.MainBarButtonDict:
            self.MainBarButtonDict[button].Draw(screen,text_width_coef=1/4)
        # Draw new diary button
        if Database.retrieve_diary(Database.todayDate()) == None:
            self.newDiaryButton.Draw(screen,1,1/1.7)
        else:
            # continuing editing today's diary
            self.editDiaryButton.Draw(screen,1,1/1.7)
        self.voiceAssistantButton.Draw(screen)

    def redrawMainBar(self,screen):
        self.drawMainBar(screen)
        self.drawMainBarButtons(screen)


    def redrawEdit(self,screen):
        if self.Text_Editor.status == True:
            self.Text_Editor.DrawDisplayDiary(screen,self.myFont15,self)
        if self.Text_Editor.mode == "edit":
            self.diarySaveButton.Draw(screen)
        if self.Text_Editor.mode == "display":
            self.diaryEditButton.Draw(screen)

    def redrawDiary(self,screen):
        pass

    def redrawAll(self,screen):
        self.redrawMainBar(screen)
        if self.mode == "Edit":
            self.redrawEdit(screen)
        if self.mode == "Diary":
            self.redrawDiary(screen)

### update ###
    def VoiceAssistantUpdate(self):
        if self.voiceAssistantButton.status == True:
            self.voiceAssistantButton.displayed_icon = self.voiceAssistantButton.extra_icon
        else:
            self.voiceAssistantButton.displayed_icon = self.voiceAssistantButton.icon

    def TextEditorUpdate(self):
        self.Text_Editor.updateDiary(self.Voice_Assistant)

    def UpdateAll(self):
        self.VoiceAssistantUpdate()
        if self.mode == "Diary":
            if self.Text_Editor.status == True and self.Text_Editor.mode == "edit":
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

