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

# diary = Diary([2017,10,27])
# text = "Tomorrow is my first day of senior year, and I am beyond nervous. I don't know anyone in my gym and lunch and those are the most social periods of the day. I don't have a specific friend group like everyone else does, so I am terrified that I am going to end up by myself. I don't like going to talk to new people because I feel like they don't want to talk to me and I feel like they think of me as a loser and that makes me sad. I would much rather just stay by myself but then I feel so embarrassed and judged. I always want to cry and have panic attacks in these situations. I don't know how to handle being alone if I am. I don't know how I can go four months by myself while everyone else has friends. I am praying to God that I end up knowing someone and having someone to talk to that I am kind of friends with. I am so scared. I want to cry just thinking about it. School gives me so much anxiety... well high school does. At least when I start college everyone will be in the same boat and wanna meet people, in high school you're pretty much fucked if you're a senior with no friends."
#
# diary.addStrings(text)
# Database.save_diary(diary)

# diary = Database.retrieve_diary([2017,11,28])
# print(diary.sentiment_report)
# Database.save_diary(diary)

# for manually deleting a tag name in the tag name list
# with open('icon\\tags\\tag.pickle', 'rb') as f:
#     tag_name_list = pickle.load(f)
#     print(tag_name_list)
#     index = tag_name_list.index('Flag of Croatia , Flag , Croatian language , Zagreb School of Economics and Management , National flag .png')
#     tag_name_list.pop(index)

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

#
# save = Reminder([2017,11,28])
# save.addContent("Do 128 homework and review for midterm")
# save.addContent("Do 112 tp1")
#
# Database.save_reminder(save)