import nltk
import pickle
import os

class SentiEstimator(object):
    def __init__(self,data,*estimators):
        self.estimators = estimators
        self.feature_data = data

    def match_features(self,text):
        """
        This function is cited from https://pythonprogramming.net/sentiment-analysis-module-nltk-tutorial/?completed=/new-data-set-training-nltk-tutorial/
        :param document:
        :return:
        """
        words = nltk.tokenize.word_tokenize(text)
        features = {}
        for w in self.feature_data:
            features[w] = (w in words)
        return features

    def estimate(self,text):
        num_estimator = len(self.estimators)
        final_score = 0
        for estimator in self.estimators:
            score = estimator.prob_classify_many(self.match_features(text))[0].prob("pos")
            print(score)
            final_score += score
        final_score = final_score/num_estimator - 0.5
        final_score = final_score * 2
        return final_score

    def getSentimentReport(self,text):
        sentence_list = nltk.sent_tokenize(text)
        overall_score = self.estimate(text)
        score_by_sentence = []
        for sentence in sentence_list:
            score_by_sentence.append(self.estimate(sentence))
        print("Overall Score: "+ str(overall_score))
        return (overall_score,score_by_sentence)