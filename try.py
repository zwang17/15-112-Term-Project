import os
import pickle
import Database as db
from Language_Analysis import *
import pickle
from Diary import *
from Diary_Calendar import *


# for manually modifying a diary entry object
# with open("diary\\2017.11.25.pickle",'rb') as f:
#     save = pickle.load(f)
# save.addSentence(Sentence('I had lunch at Chipotle and went to swim in the afternoon as usual.'))
# save.addSentence(Sentence('The water was kind of cold today.'))
# save.addSentence(Sentence('I was late for my English class this afternoon because it started five minutes earlier than I thought for some reason.'))
# save.addSentence(Sentence('Luckily the teacher was not taking attendance at the beginning of the class.'))
# print(save.text)
#
# with open("diary\\2017.11.25.pickle",'wb') as f:
#     pickle.dump(save,f,pickle.HIGHEST_PROTOCOL)

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

# print(type(datetime.datetime(2017, 11, 25).weekday()))
print(str(None))