from User_Interface import *
from Voice_Assistant import *
from Diary_Text_Editor import *
from Diary_Calendar import *
from Language_Analysis import *
from Highlight_Timeline import *
from Mood_Tracker import *

print("Init voice assistant...")
Siri = VoiceAssistant()
print("Init highlight timeline...")
Timeline = TimeLine()
print("Init text editor...")
TextEditor = TextEditor()
print("Init diary calendar...")
Calendar = Calendar()
print("Init moodtracker...")
MoodTracker = MoodTracker()
print("Init user interface...")
UI = UserInterface(Siri,TextEditor,Calendar,Timeline,MoodTracker,1000,600)
print("Setting user interface...")
Siri.setUI(UI)
Timeline.setUI(UI)
TextEditor.setUI(UI)
Calendar.setUI(UI)
MoodTracker.setUI(UI)
print("All set!")
UI.run()