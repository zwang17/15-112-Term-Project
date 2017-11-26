import os
from ImageRecognition import RecognizeImage

def getHighestLabels(dict):
    L = []
    for key in dict:
        L.append(key)
    L.sort()
    L.reverse()
    result = ""
    for value in L[:6]:
        if dict[value] != "Emoji":
            result += dict[value] + " , "
    result = result[:-2]
    result += ".png"
    return result

for filename in os.listdir(os.path.join("tag")):
    old_file = os.path.join("tag", filename)
    new_name = getHighestLabels(RecognizeImage(old_file))
    new_file = os.path.join("tag", new_name)
    os.rename(old_file,new_file)
    print(filename + "got renamed to " + new_name)