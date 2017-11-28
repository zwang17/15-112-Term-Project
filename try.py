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

diary = Diary([2017,11,5])
text = "Christmas Eve was fun, but also terrible. I got so sick! Fever, chills, nausea. Super thankful I had my boyfriend there to take care of me, but I know that is not how he wanted to spend his basic training holiday leave. Also, Christmas Day I was sick. Again, he held me tight and took care of me all day long. Today I am giving him a break and am going to take care of myself. He's definitely hubby material. All the days I could have gotten sick though and it happens when he's home.. of course."

diary.addStrings(text)
Database.save_diary(diary)

# diary = Database.retrieve_diary([2017,10,30])
# print(diary.text)
# Database.save_diary(diary)

## for manually deleting a tag name in the tag name list
# with open('icon\\tags\\tag.pickle', 'rb') as f:
#     tag_name_list = pickle.load(f)
#     index = tag_name_list.index('Wisconsin , American Community Survey , Student , School , Catholic school , Root canal .png')
#     tag_name_list.pop(index)
#
# with open('icon\\tags\\tag.pickle', 'wb') as f:
#     pickle.dump(tag_name_list,f,pickle.HIGHEST_PROTOCOL)

def getSimilarity(word,tag_name):
    """
    Helper function for word_match_tag
    :param word: entity word
    :param tag_name: tag name
    :return: similarity between the entity word and tag name based on frequency of the entity word in the tag name
    """
    score = 0
    while len(tag_name) > 1 and word in tag_name:
        score += 1
        tag_name = tag_name[tag_name.index(word)+len(word):]
    return score

def word_match_tag(word,tag_name_list):
    """
    :param word: entity word to be matched with a tag
    :param tag_name_list: the list of all available tags saved locally
    :return: the name of the file of the matched tag
    """
    winner = None
    max_score = 0
    for tagName in tag_name_list:
        tag_name = tagName.lower()
        if word in tag_name:
            score = getSimilarity(word,tag_name)
            if score > max_score:
                max_score = score
                winner = tagName
    return winner


# save = Reminder([2017,11,25])
# save.addContent("Do 128 homework and review for midterm")
# save.addContent("Do 112 tp1")
#
# with open("reminders\\2017.11.25.pickle",'wb') as f:
#     pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)
