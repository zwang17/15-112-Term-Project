import os
from Diary import *
import datetime

def todayDate():
    now = datetime.datetime.now()
    return [now.year,now.month,now.day]

def retrieve_diary(date):
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

def match_tag(diary):


def save_diary(diary):
    date = diary.date
    filename = str(date[0])+"."+str(date[1])+"."+str(date[2])+".txt"
    with open("diary\\"+filename,"w") as f:
        f.write(str(diary).strip())
    print("diary saved")