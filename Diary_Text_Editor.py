import pygame
from Diary import *
from threading import Thread
import Database as db
from Button import *
import copy

class TextEditor(object):
    def __init__(self):
        self.skip_line = ""
        self.mute = False
        self.mode = "display"
        self.tag_icon_list = []
        self.old_Diary = None
        self.text_list = None

    def setUI(self,UI):
        self.UI = UI

    def initDiarySaveButton(self):
        buttonWidth = self.UI.MainBarButtonWidth * 3 / 5
        buttonHeight = self.UI.MainBarButtonHeight * 1 / 2
        x_left = self.UI.width - buttonWidth * 2
        y_up = self.UI.height - 30
        self.diarySaveButton = RectButton("Save", self.UI.brightGrey, x_left, x_left + buttonWidth, y_up,
                                         y_up + buttonHeight, 1, "Save", self.UI.myFont15, self.UI.brightGrey)
        self.diarySaveButton.AddIcon("Save.png", 35, 35, 1 / 4, 1 / 2, alter_icon_path="Save_black.png")

    def initDiaryEditButton(self):
        buttonWidth = self.UI.MainBarButtonWidth * 3 / 5
        buttonHeight = self.UI.MainBarButtonHeight * 1 / 2
        x_left = self.UI.width - buttonWidth * 2
        y_up = self.UI.height - 30
        self.diaryEditButton = RectButton("Edit", self.UI.brightGrey, x_left, x_left + buttonWidth, y_up,
                                         y_up + buttonHeight, 1, "Edit", self.UI.myFont15, self.UI.brightGrey)
        self.diaryEditButton.AddIcon("Edit.png", 35, 35, 1 / 4, 1 / 2, alter_icon_path="Edit_black.png")

    def initAllButtons(self):
        self.initDiarySaveButton()
        self.initDiaryEditButton()

    def getDiary(self,date):
        self.Diary = db.retrieve_diary(date)

    def createNewDiary(self):
        today_date = db.todayDate()
        self.Diary = Diary(today_date)

    def updateDiary(self,VoiceAssistant):
        if self.mode == "display":
            return None
        if VoiceAssistant.new_line == self.skip_line:
            return None
        if self.mute:
            return None
        if VoiceAssistant.new_line == None:
            return None
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

# mouseMotion #
    def mouseMotion(self,x,y):
        if self.mode == "edit":
            button = self.diarySaveButton
            if button.WithinRange(x, y):
                button.color = self.UI.themeColorMain
                button.textColor = self.UI.themeColorMain
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.UI.brightGrey
                button.textColor = self.UI.brightGrey
                button.displayed_icon = button.icon
        if self.mode == "display":
            button = self.diaryEditButton
            if button.WithinRange(x, y):
                button.color = self.UI.themeColorMain
                button.textColor = self.UI.themeColorMain
                button.displayed_icon = button.alter_icon
            else:
                button.color = self.UI.brightGrey
                button.textColor = self.UI.brightGrey
                button.displayed_icon = button.icon

# mouseReleased #
    def mouseReleased(self,x,y):
        if self.mode == "display":
            button = self.diaryEditButton
            if button.WithinRange(x, y):
                self.mode = "edit"
                self.UI.Voice_Assistant.has_new_input = False
                return None

        if self.mode == "edit":
            button = self.diarySaveButton
            if button.WithinRange(x, y):
                db.save_diary(self.UI.Text_Editor.Diary, self)
                self.mode = "display"

# keyPressed #
    def keyPressed(self, key, mod):
        if key == pygame.K_BACKSPACE:
            if self.mode == "edit":
                if len(self.Diary.text) == 0:
                    return None
                self.Diary.text.pop()

# redraw #
    def redraw(self,screen):
        """
        :param screen: pygame screen object
        :param font: font for displaying purpose
        :param measureFont: a PIL font object for the purpose of measuring actual pixel length of a string
        """
        margin = 40
        y_gap = 20
        canvas_x_left = self.UI.MainBarButtonWidth + margin
        canvas_y_up = margin
        canvas_width = self.UI.width - self.UI.MainBarButtonWidth - 2*margin
        canvas_height = self.UI.height - 2*margin
        pygame.draw.rect(screen, self.UI.whiteSmoke,
                         (canvas_x_left,
                          canvas_y_up,
                          canvas_width,canvas_height), 5)
        if self.old_Diary != self.Diary:
            self.text_list = self.separatedText(self.UI.measureFont15)
            self.old_Diary = copy.deepcopy(self.Diary)
        for index in range(len(self.text_list)):
            line = self.text_list[index]
            screen.blit(self.UI.myFont15.render(line, 1, (0,0,0)),
                        (canvas_x_left+y_gap, canvas_y_up + (index+1)*y_gap))

        if self.mode == "edit":
            self.diarySaveButton.Draw(screen)
            line = "* use backspace to delete a sentence"
            screen.blit(self.UI.myFont15.render(line, 1, self.UI.grey),
                        (self.UI.MainBarButtonWidth + 60, self.UI.height - 30))
        if self.mode == "display":
            self.diaryEditButton.Draw(screen)


    def loadTags(self):
        # for testing purposes
        tags = self.Diary.tags
        for index in range(len(tags)):
            self.newTagButton = RectButton("tag{}".format(index),self.UI.brightGrey,200,200+100*(index+1),500,550,1,"",self.UI.myFont15,self.UI.brightGrey)
            self.newTagButton.AddIcon("tags\\tag\\"+tags[index], 35, 35, 1 / 2, 1 / 2)
            self.tag_icon_list.append(self.newTagButton)
