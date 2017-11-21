from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
import sys

class LanguageAnalysis(object):

    def analyze(self,text):
        """
        This function is cited from cloud.google.com/natural-language/docs/sentiment-tutorial#analyzing_document_sentiment
        """
        client = language.LanguageServiceClient()
        document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
        annotations = client.analyze_sentiment(document=document)
        score = annotations.document_sentiment.score
        magnitude = annotations.document_sentiment.magnitude

        for index, sentence in enumerate(annotations.sentences):
            sentence_sentiment = sentence.sentiment.score
            print('Sentence {} has a sentiment score of {}'.format(
                index, sentence_sentiment))

        print('Overall Sentiment: score of {} with magnitude of {}'.format(
            score, magnitude))
        return 0

    def entity_sentiment_text(self,text):
        """
        This function is cited from cloud.google.com/natural-language/docs/analyzing-entity-sentiment
        """
        client = language.LanguageServiceClient()

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)

        # Detect and send native Python encoding to receive correct word offsets.
        encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            encoding = enums.EncodingType.UTF16

        result = client.analyze_entity_sentiment(document, encoding)

        for entity in result.entities:
            print(u'Entity Name: "{}"'.format(entity.name))
            for mention in entity.mentions:
                print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
                print(u'  Content : {}'.format(mention.text.content))
                print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
                print(u'  Sentiment : {}'.format(mention.sentiment.score))
                print(u'  Type : {}'.format(mention.type))
            print(u'Salience: {}'.format(entity.salience)) # Salience is how outstanding this work is in the sentence
            print(u'Sentiment: {}\n'.format(entity.sentiment))

if __name__ == '__main__':
    test = LanguageAnalysis()
    test.analyze('I took my 15112 midterm today and it was horrible. I had no idea how to do half of the problems and I am most certainly going to fail this exam.')
    test.entity_sentiment_text('I took my 15112 midterm today and it was horrible. I had no idea how to do half of the problems and I am most certainly going to fail this exam.')