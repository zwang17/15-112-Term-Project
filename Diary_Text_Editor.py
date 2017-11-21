import pygame
import pygame.font
import pygame.event
import pygame.draw
from pygame.locals import *
from Diary import *
from threading import Thread


class TextEditor(object):
    def __init__(self):
        self.status = False
        self.Diary = Diary([2017,11,21])
        self.skip_line = ""
        self.mute = False

    def updateDiary(self,VoiceAssistant):
        if VoiceAssistant.new_line == self.skip_line:
            return None
        if self.mute: return None
        if VoiceAssistant.new_line == None: return None
        if VoiceAssistant.has_new_input and VoiceAssistant.dl_activated:
            new_line = Sentence(VoiceAssistant.new_line)
            if len(self.Diary.text) == 0 or new_line != self.Diary.text[-1]:
                self.Diary.addSentence(new_line)
            VoiceAssistant.has_new_input = False
            self.skip_line = None

    def deleteLast(self):
        self.Diary.text.pop()

    def get_key(self):
        while True:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass

    def Draw(self, screen, font, UI):
        message = str(self.Diary)
        canvas_x_left = UI.MainBarButtonWidth+15
        canvas_y_up = 15
        canvas_width = UI.width - UI.MainBarButtonWidth - 20
        canvas_height = UI.height - 20
        pygame.draw.rect(screen, UI.whiteSmoke,
                         (canvas_x_left,
                          canvas_y_up,
                          canvas_width,canvas_height), 5)
        if len(message) != 0:
            screen.blit(font.render(message, 1, (0,0,0)),
                        (canvas_x_left, canvas_y_up))
        pygame.display.flip()
