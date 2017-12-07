import os
import pickle
import Database as db
from Language_Analysis import *
import pickle
from Diary import *
from Diary_Calendar import *
from Reminder import *
from Highlight_Timeline import *
import nltk


# reminder = Reminder([2017,11,28])
# reminder.addContent("Work on TP")
# Database.save_reminder(reminder)
#
# reminder = Reminder([2017,11,27])
# reminder.addContent("Finish Essay")
# Database.save_reminder(reminder)
#
# reminder = Reminder([2017,12,5])
# reminder.addContent("Finish TP and submit through autolab")
# reminder.addContent("Finished 242 Homework")
# Database.save_reminder(reminder)
#
# reminder = Reminder([2017,12,3])
# reminder.addContent("Get package from UC")
# Database.save_reminder(reminder)


# for manually modifying a diary entry object

diary = Diary([2017,12,1])
text = "I went to the zoo today with mom, dad. We had so much fun! I saw a tiger, a monkey and some other things that I do not even know their names. I also went to the water part where I saw dolphin and different fish. It was so much fun and I want to go back some time."
diary.addStrings(text)
Database.save_diary(diary)

### update sentiment analysis of all diaries

# for manually deleting a tag name in the tag name list
# with open('icon\\tags\\tag.pickle', 'rb') as f:
#     tag_name_list = pickle.load(f)
#     print(tag_name_list)
#     index = tag_name_list.index('Flag of Croatia , Flag , Croatian language , Zagreb School of Economics and Management , National flag .png')
#     tag_name_list.pop(index)

# with open('icon\\tags\\tag.pickle', 'wb') as f:
#     pickle.dump(tag_name_list,f,pickle.HIGHEST_PROTOCOL)

# Database.updateAllDiaries()


# Es = Estimator.SentiEstimator(data,classifier)
# print(Es.estimate("I was very happy today. I woke up early and went to eat a great breakfast."))
