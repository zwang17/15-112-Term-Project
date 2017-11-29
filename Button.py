import pygame
import os

class Button(object):
    def __init__(self,name,color,text='',font=None,textColor=None):
        self.name = name
        self.color = color
        self.text = text
        self.font = font
        self.textColor = textColor
        self.has_icon = False
        self.status = False

    def WithinRange(self,x,y):
        pass
    def Draw(self,screen):
        pass

    def loadIcon(self,path,icon_width,icon_height):
        icon = pygame.image.load(os.path.join('icon', path))
        return pygame.transform.scale(icon, (icon_width, icon_height))

    def AddIcon(self,path,icon_width,icon_height,width_coef=1/2,height_coef=1/2,alter_icon_path=None):
        self.icon_width, self.icon_height = icon_width, icon_height
        self.icon_width_coef, self.icon_height_coef = width_coef,height_coef
        self.icon = self.loadIcon(path,icon_width,icon_height)
        self.has_icon = True
        self.displayed_icon = self.icon
        if alter_icon_path != None:
            self.alter_icon = self.loadIcon(alter_icon_path,icon_width,icon_height)

    def AddExtraIcon(self,path,icon_width,icon_height):
        self.extra_icon = self.loadIcon(path,icon_width,icon_height)
        self.has_icon = True

class RectButton(Button):
    def __init__(self,name,color,x_left,x_right,y_up,y_down,margin_width=0,text='',font=None,textColor=None):
        super().__init__(name,color,text,font,textColor)
        self.x_left = x_left
        self.x_right = x_right
        self.y_up = y_up
        self.y_down = y_down
        self.width = self.x_right - self.x_left
        self.height = self.y_down - self.y_up
        self.margin_width = margin_width

    def WithinRange(self,x,y):
        return self.x_left<x<self.x_right and self.y_up<y<self.y_down

    def Draw(self,screen,text_anchor=0,text_width_coef=1/2,text_height_coef=1/2):
        # text_anchor 0 means text is aligned midleft, 1 means text is centered
        pygame.draw.rect(screen, self.color, (self.x_left,self.y_up,self.width,self.height), self.margin_width)
        textSurface = self.font.render(self.text, True, self.textColor)
        textRect = textSurface.get_rect()
        if text_anchor == 0:
            textRect.midleft = (self.x_left+self.width*text_width_coef,self.y_up + self.height*text_height_coef)
        if text_anchor == 1:
            textRect.center = (self.x_left + self.width*text_width_coef, self.y_up + self.height*text_height_coef)
        screen.blit(textSurface, textRect)
        if self.has_icon:
            screen.blit(self.displayed_icon, (self.x_left-self.icon_width/2+self.width*self.icon_width_coef,
                                    self.y_up-self.icon_height/2+self.height*self.icon_height_coef))

class CircButton(Button):
    def __init__(self,name,color,center_x,center_y,radius,text='',margin_width=0,font=None,textColor=None):
        super().__init__(name,color,text,font,textColor)
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.margin_width = margin_width

    def setDataObject(self,data):
        self.data = data

    @staticmethod
    def distance(x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**0.5

    def WithinRange(self,x,y):
        return self.distance(self.center_x,self.center_y,x,y) < self.radius

    def Draw(self,screen):
        pygame.draw.circle(screen,self.color,[int(self.center_x),int(self.center_y)],int(self.radius),self.margin_width)
        if self.has_icon:
            screen.blit(self.displayed_icon, (self.center_x-self.icon_width/2,self.center_y-self.icon_height/2))
