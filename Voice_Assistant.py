from Speech_Recognition import *
from threading import Thread
import copy
import Database

class VoiceAssistant(object):

    def __init__(self):

        self.exit_status = False
        self.has_new_input = False
        self.UI = None
        self.new_line = None
        self.activation_command = ["hey siri"]
        self.exit_command_list = ["nevermind","bye","nothing"]
        self.exit_command = []
        self.va_activated = False
        self.dl_activated = False
        self.button = None
        
    def setUI(self,UI):
        self.UI = UI

    def RetreiveWeather(self):
        pass

    def SaveDiary(self,Diary):
        self.exit_status = True
        Database.save_diary(Diary)

    def EditDiary(self):
        self.UI.mouseReleasedNewDiaryButton()

    def CreateReminder(self):
        pass

    def Help(self):
        pass

    def ShowHighlight(self):
        pass

    def activateVoiceAssisant(self):
        self.va_activated = True
        self.button.status = True

    def deactivateVoiceAssistant(self):
        self.va_activated = False
        self.button.status = False

    def collectBackgroundText(self):
        getText(self)

    def checkActivationCommand(self):
        while not self.exit_status:
            if self.new_line != None:
                over = False
                for command in self.activation_command:
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
                for command in self.exit_command_list:
                    if command in self.new_line.lower():
                        self.exit_command.append(command)
                        over = True
                        break
                if over: break
        print("exit checkExitCommand")

    def refresh(self):
        self.exit_status = True
        self.exit_status = False

    def performCommands(self):
        exit_command = copy.deepcopy(self.exit_command)
        print("Command to be executed:"+exit_command)


    def runVoiceAssistant(self,Text_Editor):
        while True:
            Thread(target=self.collectBackgroundText).start()
            self.checkActivationCommand()
            if self.va_activated:
                if self.dl_activated:
                    Text_Editor.mute = True
                Thread(target=self.collectBackgroundText).start()
                self.checkExitCommand()
                self.deactivateVoiceAssistant()
                self.performCommands()
                if self.dl_activated:
                    Text_Editor.skip_line = self.new_line
                    Text_Editor.mute = False

    def runDiaryListener(self):
        print("run Diary Listener")
        self.dl_activated = True
        self.collectBackgroundText()