from Speech_Recognition import *
from threading import Thread
import copy
import Database
import pygame

class VoiceAssistant(object):

    def __init__(self):
        self.has_new_input = False
        self.new_line = None
        self.va_activation_command = ["hey "]
        self.va_exit_command_list = ["nevermind","bye","nothing","reminder","highlight","help","edit","save","create","show","highlight","tracker","calendar"]
        self.exit_command_heard = []
        self.va_activated = False
        self.dl_activated = False
        self.init()
        self.timer = 0
        self.display_text = False
        self.text_displayed = None
        self.initiated = False
        self.UI = None

    def setUI(self,UI):
        self.UI = UI
        self.va_button = self.UI.voiceAssistantButton

    def init(self):
        self.saveDiary_command_list = ['save']
        self.editDiary_command_list = ['edit']
        self.createReminder_command_list = ['reminder']
        self.help_command_list = ['help']
        self.showDiaryCalendar_command_list = ['calendar','show']
        self.showHighlight_command_list = ['show','highlight']
        self.showMoodTracker_command_list = ['show','tracker']
        self.command_list_list = [self.saveDiary_command_list,self.editDiary_command_list,self.createReminder_command_list,\
                                  self.showDiaryCalendar_command_list,self.showHighlight_command_list,self.showMoodTracker_command_list,self.help_command_list]
        self.function_list = [self.SaveDiary,self.EditDiary,self.CreateReminder,self.ShowDiaryCalendar,self.ShowHighlight,self.ShowMoodTracker,self.Help]

    def mousePressed(self,x,y):
        button = self.va_button
        if button.WithinRange(x,y):
            if button.status == False:
                button.color = self.UI.brightGrey
                button.displayed_icon = button.alter_icon
            if button.status == True:
                button.color = self.UI.brightGrey
                button.displayed_icon = button.extra_icon
            button.status = not button.status

    def mouseReleased(self,x,y):
        button = self.va_button
        if button.WithinRange(x, y):
            button.color = self.UI.white
            button.displayed_icon = button.extra_icon
            if self.va_activated == False:
                self.activateVoiceAssisant()
            else:
                self.deactivateVoiceAssistant()

    def mouseMotion(self,x,y):
        button = self.va_button
        if self.va_activated == False:
            if button.WithinRange(x,y):
                button.color = self.UI.white
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.UI.brightGrey
                button.displayed_icon = button.icon

    def timerFired(self):
        if self.display_text == True:
            self.timer += 1
            print(self.timer)
            if self.timer == 100:
                self.display_text = False
                self.timer = 0
###
    def getPixelLength(self,measureFont,text):
        return measureFont.getsize(text)  # this function call originally comes from Pillow documentation

    def separatedText(self,measureFont):
        text = self.text_displayed
        line_pix_len = 105
        result = []
        default_string_len = 1
        while self.getPixelLength(measureFont,text)[0] > line_pix_len:
            length = default_string_len
            new_line = text[:length]
            while self.getPixelLength(measureFont,new_line)[0] < line_pix_len:
                length += 1
                new_line = text[:length]
            text = text[length:]
            if len(text) != 0 and text[0] != " ":
                new_line += "-"
            result.append(new_line)
        result.append(text)
        return result

    def drawText(self,screen):
        if self.display_text == True:
            margin = 10
            y_gap = 20
            canvas_x_left = margin
            canvas_y_up = self.UI.height / 3 * 2
            self.text_list = self.separatedText(self.UI.measureFont15)
            for index in range(len(self.text_list)):
                line = self.text_list[index]
                screen.blit(self.UI.myFont15.render(line, 1, self.UI.brightGrey),
                            (canvas_x_left, canvas_y_up + (index + 1) * y_gap))
###

    def redraw(self,screen):
        self.va_button.Draw(screen)
        if self.display_text:
            self.drawText(screen)

# actions #
    def Initiate(self):
        print("initiating...")
        temp = self.new_line
        self.display_text = True
        self.text_displayed = "Say your name is ___"
        while self.new_line == None or ("your" not in self.new_line) or ("name" not in self.new_line) or ("is" not in self.new_line):
            if not self.va_activated:
                return None
        str_list = self.new_line.split(" ")
        self.name = str_list[-1].lower()[:-1]
        self.va_activation_command[0] = self.va_activation_command[0] + self.name
        self.deactivateVoiceAssistant()
        self.initiated = True
        self.display_text = True
        self.timer = 0
        self.text_displayed = "My name is {}".format(self.name)

    def SaveDiary(self):
        self.display_text = True
        self.text_displayed = "Saving Diary..."
        self.UI.Text_Editor.mode = "display"
        Database.save_diary(self.UI.Text_Editor.Diary)
        self.deactivateVoiceAssistant()
        self.UI.Text_Editor.mouseMotion(0,0)
        print("Diary saved!")

    def EditDiary(self):
        print("edit diary...")
        if self.UI.mode == "Edit":
            self.UI.Text_Editor.mode = "edit"
        else:
            today_diary = Database.retrieve_diary(Database.todayDate())
            if today_diary == None:
                self.UI.Text_Editor.createNewDiary()
            else:
                self.UI.Text_Editor.Diary = today_diary
        self.UI.mode = "Edit"
        self.UI.Text_Editor.mode = "edit"
        self.deactivateVoiceAssistant()

    def CreateReminder(self):
        print("create reminder...")
        temp = self.new_line
        self.deactivateVoiceAssistant()
        self.display_text = True
        self.text_displayed = "Remind you to?"
        while self.new_line.strip() == temp.strip():
            pass
        content = self.new_line
        self.UI.today_reminder.addContent(content)
        self.UI.today_reminder.updateReminderButtons(self.UI.white, self.UI.MainBarButtonWidth + 50, 80, self.UI.myFont15Bold, self.UI.measureFont15, self.UI.brightGrey,600)
        Database.save_reminder(self.UI.today_reminder)
        self.deactivateVoiceAssistant()

    def Help(self):
        print("help")
        self.display_text = True
        self.text_displayed = "Say \"hey "+ self.name +"\""
        self.deactivateVoiceAssistant()

    def ShowDiaryCalendar(self):
        self.display_text = True
        self.text_displayed = "Showing Calendar..."
        self.UI.mode = "Diary"

    def ShowHighlight(self):
        self.display_text = True
        self.text_displayed = "Showing Highlight..."
        self.UI.mode = "Highlight"
        self.deactivateVoiceAssistant()

    def ShowMoodTracker(self):
        self.display_text = True
        self.text_displayed = "Showing Mood Tracker..."
        self.UI.mode = "Mood Tracker"
        self.deactivateVoiceAssistant()

#####
    def performCommands(self):
        exit_command = copy.deepcopy(self.exit_command_heard)
        print("Command to be executed:"+str(exit_command))
        for index in range(len(self.command_list_list)):
            command_list = self.command_list_list[index]
            if self.checkCommandsInList(command_list,exit_command) or self.checkCommandsInList(command_list,exit_command):
                self.function_list[index]()
        self.deactivateVoiceAssistant()

    def activateVoiceAssisant(self):
        self.va_activated = True

    def deactivateVoiceAssistant(self):
        self.va_activated = False
        self.va_button.displayed_icon = self.va_button.icon
        self.va_button.color = self.UI.brightGrey

    def collectBackgroundText(self):
        while True:
            try:
                getText(self)
            except:
                print("Reinitiating background listening")

    def checkActivationCommand(self):
        exit = False
        while not exit:
            for command in self.va_activation_command:
                if command in self.new_line.lower():
                    self.activateVoiceAssisant()
                    print("Voice assistant activated")
                    self.has_new_input = False
                    exit = True
                    break

    def checkExitCommand(self):
        print("checking exit command")
        exit = False
        while not exit:
            if self.va_activated == False:
                return None
            for command in self.va_exit_command_list:
                if command in self.new_line.lower():
                    self.exit_command_heard.append(command)
                    exit = True
            self.has_new_input = False
        print("exit checkExitCommand")

    def checkCommandsInList(self,commands,command_list):
        for commandToBeChecked in commands:
            exist = False
            for command in command_list:
                if commandToBeChecked.lower() == command.lower():
                    exist = True
            if not exist: return False
        return True

    def runVoiceAssistant(self,Text_Editor):
        if self.initiated == False:
            if self.UI == None:
                return None
            elif self.va_button.status == True:
                self.Initiate()
            else:
                return None
        self.checkActivationCommand()
        if self.va_activated:
            if self.dl_activated:
                Text_Editor.mute = True
            self.checkExitCommand()
            self.performCommands()
            if self.dl_activated:
                Text_Editor.skip_line = self.new_line
                Text_Editor.mute = False
            self.exit_command_heard = []
            self.has_new_input = False

    def runDiaryListener(self):
        print("run Diary Listener")
        self.dl_activated = True
