from User_Interface import *
from Voice_Assistant import *
from Diary_Text_Editor import *
from Diary_Calendar import *
from Language_Analysis import *

Siri = VoiceAssistant()
TextEditor = TextEditor()
Calendar = Calendar()
UI = UserInterface(Siri,TextEditor,Calendar,1000,600)
UI.run()