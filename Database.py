import os
from Diary import *
import datetime

def todayDate():
    now = datetime.datetime.now()
    return [now.year,now.month,now.day]

def retrieve_diary(date):
    """
    :param date: should be a list of integers in the form [year,month,day]
    :return: an Diary object
    """
    date_str = str(date[0])+"."+str(date[1])+"."+str(date[2])+".txt"
    exist = False
    for filename in os.listdir("diary"):
        if filename == date_str:
            exist = True
    if not exist:
        return None
    with open("diary\\"+date_str,'r') as f:
        text = f.read().strip()
    text = text.split("  ")
    result = Diary(date)
    for line in text:
        result.addSentence(Sentence(line))
    return result

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

def save_diary(diary):
    date = diary.date
    filename = str(date[0])+"."+str(date[1])+"."+str(date[2])+".txt"
    with open("diary\\"+filename,"w") as f:
        f.write(str(diary).strip())
    print("diary saved")

