"""
!! This trainer is written following a YouTube tutorial named "NLTK with Python 3 for Natural Language Processing"
at https://www.youtube.com/watch?v=FLZvOKSCkxY&index=1&list=PLQVvvaa0QuDf2JswnfiGkliBInZnIC4HL
The training data was obtained from the same source.
"""
import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

positive_text = open("sample_text/positive.txt","r",encoding="utf-8")
negative_text = open("sample_text/negative.txt","r",encoding="utf-8")

positive_sample = positive_text.read().split("\n")
negative_sample = negative_text.read().split("\n")

formatted_sample = []

for sample in positive_sample:
    formatted_sample.append((sample,"pos"))
for sample in negative_sample:
    formatted_sample.append((sample,"neg"))

# all_words = []
# all_words_type = ["R","J"]
# for sample in positive_sample:
#     words = nltk.tokenize.word_tokenize(sample)
#     tag_result = nltk.pos_tag(words)
#     for word in tag_result:
#         for type in all_words_type:
#             if type in word[1]:
#                 all_words.append(word[0].lower())
#
# for sample in negative_sample:
#     words = nltk.tokenize.word_tokenize(sample)
#     tag_result = nltk.pos_tag(words)
#     for word in tag_result:
#         for type in all_words_type:
#             if type in word[1]:
#                 all_words.append(word[0].lower())
#
# all_words = nltk.FreqDist(all_words)
# word_features = list(all_words.keys())[:8000]

with open('model/feature_data/feature.pickle','rb') as f:
    word_features = pickle.load(f)

def match_features(document):
    """
    This function is cited from https://pythonprogramming.net/sentiment-analysis-module-nltk-tutorial/?completed=/new-data-set-training-nltk-tutorial/
    :param document:
    :return:
    """
    words = nltk.tokenize.word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

dataset = []
for sample in formatted_sample:
    dataset.append((match_features(sample[0]),sample[1]))

random.shuffle(dataset)
train_set, test_set = dataset[:10000],dataset[10000:]

# print("Trainning begin...")
# MNB_classifier = SklearnClassifier(MultinomialNB())
# MNB_classifier.train(train_set)
#
# with open("model/MNB_classifier.pickle","wb") as f:
#     pickle.dump(MNB_classifier, f,pickle.HIGHEST_PROTOCOL)
#
# BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
# BernoulliNB_classifier.train(train_set)
#
# with open("model/BernoulliNB_classifier.pickle","wb") as f:
#     pickle.dump(BernoulliNB_classifier, f,pickle.HIGHEST_PROTOCOL)
#
# LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
# LogisticRegression_classifier.train(train_set)
#
# with open("model/LogisticRegression_classifier.pickle","wb") as f:
#     pickle.dump(LogisticRegression_classifier, f,pickle.HIGHEST_PROTOCOL)

# MLP_classifier = SklearnClassifier(MLPClassifier())
# MLP_classifier.train(train_set)
# print("MLP_classifier accuracy percent:", (nltk.classify.accuracy(MLP_classifier, test_set))*100)
#
# with open("model/MLP_classifier.pickle","wb") as f:
#     pickle.dump(MLP_classifier,f,pickle.HIGHEST_PROTOCOL)
