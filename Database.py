import os
from Diary import *
import datetime
import pickle

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November','December']
month_num_day = { 'January': 31, 'February': 29, 'March': 31, 'April': 30, 'May': 31, 'June': 30,
                 'July': 31, 'August': 31, 'September': 30, 'October': 31, 'November': 30,'December': 31}

def todayDate():
    now = datetime.datetime.now()
    return [now.year,now.month,now.day]

def retrieve_diary(date):
    """
    :param date: should be a list of integers in the form [year,month,day]
    :return: an Diary object
    """
    date_str = str(date[0])+"."+str(date[1])+"."+str(date[2])+".pickle"
    try:
        with open("diary\\"+date_str,'rb') as f:
            diary = pickle.load(f)
        return diary
    except:
        return None

def word_match_tag(word):
    """
    :param word: entity word to be matched with a tag
    :param tag_name_list: the list of all available tags saved locally
    :return: the name of the file of the matched tag
    """
    with open('icon\\tags\\tag.pickle', 'rb') as f:
        tag_name_list = pickle.load(f)
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

def getSentiment(Analyst,text):
    result = Analyst.sentiment_analyze(text)
    return result

def getSimilarity(word,tag_name):
    """
    Helper function for word_match_tag
    :param word: entity word
    :param tag_name: tag name
    :return: similarity between the entity word and tag name based on frequency of the entity word in the tag name
    """
    frequency = 0
    while len(tag_name) > 1 and word in tag_name:
        frequency += 1
        tag_name = tag_name[tag_name.index(word)+len(word):]
    tag_name_wo_space = tag_name.replace(" ","")
    ratio = len(word)/len(tag_name_wo_space)
    score = ratio * frequency
    return score

def save_diary(diary):
    date = diary.date
    # offline mode
    diary.updateSentimentAnalysis()

    diary.updateTags()
    filename = str(date[0]) + "." + str(date[1]) + "." + str(date[2]) + ".pickle"
    with open("diary\\"+filename,"wb") as f:
        pickle.dump(diary,f,pickle.HIGHEST_PROTOCOL)

def retrieve_reminder(date):
    """
    :param date: should be a list of integers in the form [year,month,day]
    :return: an Diary object
    """
    date_str = str(date[0])+"."+str(date[1])+"."+str(date[2])+".pickle"
    try:
        with open("reminders\\"+date_str,'rb') as f:
            reminder = pickle.load(f)
        return reminder
    except:
        return None

def save_reminder(reminder):
    date = reminder.date
    filename = str(date[0]) + "." + str(date[1]) + "." + str(date[2]) + ".pickle"
    with open("reminders\\" + filename, "wb") as f:
        pickle.dump(reminder, f, pickle.HIGHEST_PROTOCOL)

def next_date(date):
    date[2] += 1
    if date[2] > 31:
        date[2] = 0
        date[1] += 1
    if date[1] > 12:
        date[1] = 0
        date[0] += 1


def previous_date(date):
    date[2] -= 1
    if date[2] < 1:
        date[1] -= 1
        if date[1] < 1:
            date[1] = 12
            date[0] -= 1
        date[2] = month_num_day[months[date[1] - 1]]

def retreieve_diary_between(startDate,endDate):
    ending_date = copy.deepcopy(endDate)
    ending_date[2] += 1
    starting_date = copy.deepcopy(startDate)
    result = []
    while starting_date != ending_date:
        diary = retrieve_diary(starting_date)
        if diary != None:
            result.append(diary)
        next_date(starting_date)
    return result

def sortDiariesByDates(diary_list):
    length = len(diary_list)
    for i in range(length):
        min = i
        for k in range(i+1,length):
            if diary_list[k].date < diary_list[min].date:
                min = k
        diary_list[i],diary_list[min] = diary_list[min],diary_list[i]

def getDiariesWithHighestSentiments(diary_list,num_diary):
    sentiment_diary_dict = {}
    for diary in diary_list:
        key = diary.sentiment_report[0]
        if key not in sentiment_diary_dict:
            sentiment_diary_dict[key] = [diary]
        else:
            sentiment_diary_dict[key].append(diary)
    key_list = list(sentiment_diary_dict.keys())
    key_list.sort()
    key_list.reverse()
    length = min(num_diary,len(key_list))
    key_list = key_list[:length]
    new_diary_list = []
    for key in key_list:
        for diary in sentiment_diary_dict[key]:
            new_diary_list.append(diary)
    sortDiariesByDates(new_diary_list)
    return new_diary_list

def getDeltaDays(date1,date2):
    return (datetime.date(date1[0],date1[1],date1[2])-datetime.date(date2[0],date2[1],date2[2])).days

def updateAllDiaries():
    # the purpose of this function is to update all diaries with new sentiment analysis potentially due to new
    # tag name list or methodology of sentiment/entity analysis
    for filename in os.listdir(os.path.join("diary")):
        name = filename.split(".")
        date = [int(name[0]),int(name[1]),int(name[2])]
        diary = retrieve_diary(date)
        save_diary(diary)

def updateTagNameListPickleFile():
    result = []
    for filename in os.listdir(os.path.join("icon","tags","tag")):
        result.append(filename)
    with open('tag.pickle', 'wb') as f:
        pickle.dump(result,f,pickle.HIGHEST_PROTOCOL)

