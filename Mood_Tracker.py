import Database
import pygame
from datetime import date
from Button import *

class MoodTracker(object):
    def __init__(self):
        self.endDate = Database.todayDate()
        self.startDate = Database.todayDate()
        self.startDate[1] -= 1

    def update_display_list(self):
        self.display_list = Database.retreieve_diary_between(self.startDate,self.endDate)

    def updateAllButtons(self):
        pass

    def setUI(self,UI):
        self.UI = UI
        self.X_x_left = self.UI.MainBarButtonWidth + 60
        self.X_x_right = self.UI.width - 60
        self.X_init_x = self.X_x_left
        self.X_length = self.X_x_right - self.X_x_left
        self.X_y = self.Y_y_down = 540
        self.Y_x = self.X_x_left
        self.Y_y_up = 60
        self.Y_init_y = self.Y_y_down
        self.update_display_list()

# mouseMotion #

# mouseReleased #

# redraw #
    def drawBaseline(self,screen):
        if self.Y_init_y > self.Y_y_up:
            self.Y_init_y -= 5
        if self.X_init_x < self.X_x_right:
            self.X_init_x += 5
        pygame.draw.lines(screen,self.UI.orange,False,[(self.X_x_left,self.X_y),(self.X_init_x,self.X_y)],2)
        pygame.draw.lines(screen, self.UI.orange, False, [(self.Y_x, self.Y_y_down), (self.Y_x, self.Y_init_y)], 2)

    def redraw(self,screen):
        self.drawBaseline(screen)