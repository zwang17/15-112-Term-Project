from Speech_Recognition import *
from threading import Thread
import copy

class VoiceAssistant(object):

    def __init__(self):

        self.exit_status = False
        self.has_new_input = False

        self.new_line = None
        self.activation_command = ["hey siri"]
        self.exit_command_list = ["nevermind"]
        self.exit_command = []
        self.va_activated = False
        self.dl_activated = False
        self.button = None
        

    def RetreiveWeather(self):
        pass

    def CreateDiary(self):
        pass

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
                if self.dl_activated:
                    Text_Editor.skip_line = self.new_line
                    Text_Editor.mute = False

    def runDiaryListener(self):
        print("run Diary Listener")
        self.dl_activated = True
        self.collectBackgroundText()