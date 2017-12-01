import os
import pickle
import Database as db
from Language_Analysis import *
import pickle
from Diary import *
from Diary_Calendar import *
from Reminder import *
from Highlight_Timeline import *

# for manually modifying a diary entry object

# diary = Diary([2017,11,30])
# text = "It was a sunny day today. Everything went well! I woke up at 8:30 and went to only two classes today. First one was a recitation and the second one was 112 lecture, which was a lot of fun. The professors talked about really interesting math problems that are related to computer science. I ate ramen for lunch at the university center as usual and studies in the library for the entire afternoon. I also had some fruit that came with the block. I went to swim in the evening as usual."
# diary.addStrings(text)
# Database.save_diary(diary)

### update sentiment analysis of all diaries

# for manually deleting a tag name in the tag name list
# with open('icon\\tags\\tag.pickle', 'rb') as f:
#     tag_name_list = pickle.load(f)
#     print(tag_name_list)
#     index = tag_name_list.index('Flag of Croatia , Flag , Croatian language , Zagreb School of Economics and Management , National flag .png')
#     tag_name_list.pop(index)

# with open('icon\\tags\\tag.pickle', 'wb') as f:
#     pickle.dump(tag_name_list,f,pickle.HIGHEST_PROTOCOL)

Database.updateAllDiaries()