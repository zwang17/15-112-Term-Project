
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

    def addSentence(self,sentence):
        """
        :param sentence: a Sentence object
        """
        self.text.append(sentence)

    def __repr__(self):
        return repr(self.text)

    def __str__(self):
        result = ""
        for sentence in self.text:
            result += str(sentence)
        return result