from Language_Analysis import *
import pickle
import Database as db
import copy
import string

class Word(object):
    """
    an instance of Word contains the text of Word and the status, which could be bold, itallic, even colorful
    """
    def __init__(self,text,status=None):
        self.text = text
        self.status = status

    def setStatus(self,status):
        self.status = status

    def getText(self):
        return self.text

    def __repr__(self):
        return self.getText()

    def __str__(self):
        return self.getText()

    def __eq__(self, other):
        return isinstance(other, Word) and self.text == other.text

class Sentence(object):
    def __init__(self,text=None):
        self.text = []
        if text != None:
            self.setTextByString(text)
    def setTextByString(self,string):
        self.text = []
        string = string.strip()
        word_list = string.split(" ")
        word_list[0] = word_list[0][0].upper() + word_list[0][1:]
        for index in range(len(word_list)):
            self.text.append(Word(word_list[index]))

    def setStausByWord(self,word,status):
        for index in range(len(self.text)):
            if self.text[index].getText() == word:
                self.text[index].setStatus(status)

    def __repr__(self):
        return repr(self.text)

    def __str__(self):
        result = ""
        for word in self.text:
            result += str(word) + " "
        result += " "
        return result

    def __eq__(self, other):
        return isinstance(other,Sentence) and self.text == other.text

class Diary(object):
    def __init__(self,date):
        self.date = date
        self.text = []
        self.sentiment_report = None
        self.entity_sentiment_report = None
        self.tags = None

    def updateSentimentAnalysis(self):
        print("Updating Sentiment Analysis...")
        self.sentiment_report = sentiment_analyze(str(self))
        print("Updating Entity Sentiment Analysis...")
        self.entity_sentiment_report = entity_sentiment_analysis(str(self))
        print("Sentiment Analysis Updated!")

    def updateTags(self,num_tags=3):
        self.tags = []
        sentiment_value_list = list(self.entity_sentiment_report.keys())
        sentiment_value_list.sort()
        sentiment_value_list.reverse()
        count = 0
        for value in sentiment_value_list:
            entity_name = self.entity_sentiment_report[value][0]
            tag_found = db.word_match_tag(entity_name)
            if tag_found != None:
                self.tags.append(tag_found)
                count += 1
            if count == num_tags:
                print("Tags updated!")
                break
        print(self.tags)
        print("Tags updated!")

    def addSentence(self,sentence):
        """
        :param sentence: a Sentence object
        """
        self.text.append(sentence)

    def addStrings(self,strings):
        strings.replace("  "," ")
        string_list = strings.split(" ")
        new_line = ""
        for index in range(len(string_list)-1):
            new_line = new_line + string_list[index] + " "
            if string_list[index+1][0].upper() in string.ascii_uppercase and string_list[index][-1] in string.punctuation:
                self.addSentence(Sentence(new_line))
                new_line = ""

    def __repr__(self):
        return repr(self.text)

    def __str__(self):
        result = ""
        for sentence in self.text:
            result += str(sentence)
        return result

    def __eq__(self, other):
        return str(self) == str(other)