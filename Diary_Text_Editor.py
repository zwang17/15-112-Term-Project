import pygame
import pygame.font
import pygame.event
import pygame.draw
from pygame.locals import *
from Diary import *
from threading import Thread
import Database as db
from Button import *
import copy

class TextEditor(object):
    def __init__(self):
        self.status = False
        self.skip_line = ""
        self.mute = False
        self.mode = "display"
        self.tag_icon_list = []
        self.old_Diary = None
        self.text_list = None

    def getDiary(self,date):
        self.Diary = db.retrieve_diary(date)

    def createNewDiary(self):
        today_date = db.todayDate()
        self.Diary = Diary(today_date)

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

    def getPixelLength(self,measureFont,text):
        return measureFont.getsize(text)  # this function call originally comes from Pillow documentation

    def separatedText(self,measureFont):
        text = str(self.Diary)
        line_pix_len = 730
        result = []
        default_string_len = 100
        while self.getPixelLength(measureFont,text)[0] > line_pix_len:
            length = default_string_len
            new_line = text[:length]
            while self.getPixelLength(measureFont,new_line)[0] < line_pix_len:
                length += 1
                new_line = text[:length]
            text = text[length:]
            if text[0] != " ":
                new_line += "-"
            result.append(new_line)
        result.append(text)
        return result

    def DrawDisplayDiary(self, screen, font, measureFont, UI):
        """
        :param screen: pygame screen object
        :param font: font for displaying purpose
        :param measureFont: a PIL font object for the purpose of measuring actual pixel length of a string
        """
        margin = 40
        y_gap = 20
        canvas_x_left = UI.MainBarButtonWidth + margin
        canvas_y_up = margin
        canvas_width = UI.width - UI.MainBarButtonWidth - 2*margin
        canvas_height = UI.height - 2*margin
        pygame.draw.rect(screen, UI.whiteSmoke,
                         (canvas_x_left,
                          canvas_y_up,
                          canvas_width,canvas_height), 5)
        if self.old_Diary != self.Diary:
            self.text_list = self.separatedText(measureFont)
            self.old_Diary = copy.deepcopy(self.Diary)
        for index in range(len(self.text_list)):
            line = self.text_list[index]
            screen.blit(font.render(line, 1, (0,0,0)),
                        (canvas_x_left+y_gap, canvas_y_up + (index+1)*y_gap))
        for tag_icon in self.tag_icon_list:
            tag_icon.Draw(screen)


    def loadTags(self,UI):
        # for testing purposes
        tags = self.Diary.tags
        for index in range(len(tags)):
            self.newTagButton = RectButton("tag{}".format(index),UI.brightGrey,200,200+100*(index+1),500,550,1,"",UI.myFont15,UI.brightGrey)
            self.newTagButton.AddIcon("tags\\tag\\"+tags[index], 35, 35, 1 / 2, 1 / 2)
            self.tag_icon_list.append(self.newTagButton)
        print(self.tag_icon_list)