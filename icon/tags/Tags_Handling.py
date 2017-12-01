import os
from ImageRecognition import RecognizeImage
import copy
import pickle

def getHighestLabels(dict):
    L = []
    for key in dict:
        L.append(key)
    L.sort()
    L.reverse()
    result = ""
    for value in L[:6]:
        if "Emoji" not in dict[value]:
            result += dict[value] + " , "
    result = result[:-2]
    result += ".png"
    return result

# def modifyName(filename):
    # if "," not in filename:
    #     string_list = filename.strip(" ")
    #     new_name = ""
    #     for i in string_list:
    #         new_name = new_name + i + ","
    #     return new_name
    # else:
    #     return filename
#     filename = filename[:-5]
#     tag_list = filename.split(",")
#     new_list = copy.deepcopy(tag_list)
#     for index in range(len(tag_list)):
#         tag = tag_list[index]
#         if " of " in tag or " to " in tag or " flag " in tag:
#             new_list.pop(new_list.index(tag))
#     result = ""
#     for index in range(len(new_list)-1):
#         result = result + new_list[index] + ","
#     result = result + new_list[-1] + ".png"
#     return result
#
# for filename in os.listdir(os.path.join("tag")):
#     old_file = os.path.join("tag", filename)
#     # new_name = getHighestLabels(RecognizeImage(filename))
#     new_name = modifyName(filename)
#     new_file = os.path.join("tag", new_name)
#     os.rename(old_file,new_file)
#     print(filename + " got renamed to " + new_name)

