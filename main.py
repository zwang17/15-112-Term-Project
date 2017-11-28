from User_Interface import *
from Voice_Assistant import *
from Diary_Text_Editor import *
from Diary_Calendar import *
from Language_Analysis import *
from Highlight_Timeline import *
from Mood_Tracker import *

Siri = VoiceAssistant()
Timeline = TimeLine()
TextEditor = TextEditor()
Calendar = Calendar()
MoodTracker = MoodTracker()
UI = UserInterface(Siri,TextEditor,Calendar,Timeline,MoodTracker,1000,600)
Siri.setUI(UI)
Timeline.setUI(UI)
TextEditor.setUI(UI)
Calendar.setUI(UI)
MoodTracker.setUI(UI)
UI.run()