from Speech_Recognition import *
from threading import Thread
import copy
import Database

class VoiceAssistant(object):

    def __init__(self):

        self.exit_status = False
        self.has_new_input = False
        self.new_line = None
        self.va_activation_command = ["hey siri"]
        self.va_exit_command_list = ["nevermind","bye","nothing","diary","reminder","highlight","help","edit","save","create","show","highlight","mood","tracker","calendar"]
        self.exit_command_heard = []
        self.va_activated = False
        self.dl_activated = False
        self.init()

    def setUI(self,UI):
        self.UI = UI
        self.va_button = self.UI.voiceAssistantButton

    def init(self):
        self.saveDiary_command_list = ['save','diary']
        self.editDiary_command_list = ['edit','diary']
        self.createReminder_command_list = ['reminder','remind']
        self.help_command_list = ['help']
        self.showDiaryCalendar_command_list = ['calendar','show']
        self.showHighlight_command_list = ['show','highlight']
        self.showMoodTracker_command_list = ['show','mood','tracker']
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
        if button.status == False:
            if button.WithinRange(x,y):
                button.color = self.UI.white
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.UI.brightGrey
                button.displayed_icon = button.icon

    def redraw(self,screen):
        self.va_button.Draw(screen)

# actions #
    def SaveDiary(self):
        self.exit_status = True
        Database.save_diary(self.UI.Text_Editor.Diary)
        self.deactivateVoiceAssistant()
        print("Diary saved")

    def EditDiary(self):
        print("edit diary")
        if Database.retrieve_diary(Database.todayDate()) == None:
            self.UI.Text_Editor.createNewDiary()
        self.UI.mode = "Edit"
        self.UI.Text_Editor.mode = "edit"
        self.deactivateVoiceAssistant()

    def CreateReminder(self):
        print("create reminder")
        print(self.new_line)

    def Help(self):
        print("help")
        self.deactivateVoiceAssistant()

    def ShowDiaryCalendar(self):
        self.UI.mode = "Diary"

    def ShowHighlight(self):
        print("show highlight")
        self.UI.mode = "Highlight"
        self.deactivateVoiceAssistant()

    def ShowMoodTracker(self):
        print("show mood tracker")
        self.UI.mode = "Mood Tracker"
        self.deactivateVoiceAssistant()

#   #

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
        self.va_button.status = True

    def deactivateVoiceAssistant(self):
        self.va_activated = False
        self.va_button.status = False

    def collectBackgroundText(self):
        getText(self)

    def checkActivationCommand(self):
        while not self.exit_status:
            if self.new_line != None:
                over = False
                for command in self.va_activation_command:
                    if command in self.new_line.lower():
                        self.activateVoiceAssisant()
                        print("Voice assistant activated")
                        over = True
                        break
                if over: break

    def checkExitCommand(self):
        while not self.exit_status:
            if self.new_line != None:
                over = False
                for command in self.va_exit_command_list:
                    if command in self.new_line.lower():
                        self.exit_command_heard.append(command)
                        over = True
                if over: break
        print("exit checkvaExitCommand")

    def refresh(self):
        self.exit_status = True
        self.exit_status = False

    def checkCommandsInList(self,commands,command_list):
        for commandToBeChecked in commands:
            exist = False
            for command in command_list:
                if commandToBeChecked.lower() == command.lower():
                    exist = True
            if not exist: return False
        return True

    def runVoiceAssistant(self,Text_Editor):
        while True:
            Thread(target=self.collectBackgroundText).start()
            self.checkActivationCommand()
            if self.va_activated:
                if self.dl_activated:
                    Text_Editor.mute = True
                Thread(target=self.collectBackgroundText).start()
                self.checkExitCommand()
                self.performCommands()
                if self.dl_activated:
                    Text_Editor.skip_line = self.new_line
                    Text_Editor.mute = False

    def runDiaryListener(self):
        print("run Diary Listener")
        self.dl_activated = True
        self.collectBackgroundText()