from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six
import sys

def sentiment_analyze(text):
    """
    This function is cited from cloud.google.com/natural-language/docs/sentiment-tutorial#analyzing_document_sentiment
    :return a len-3 tuple in the form of (overall sentiment score, overall sentiment magnitude, a list of sentiment values of each sentence in sequential order)
    """
    client = language.LanguageServiceClient()
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    sentence_sentiment_list = []
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment_list.append(sentence.sentiment.score)


    return (score,magnitude,sentence_sentiment_list)

def entity_sentiment_analysis(text):
    """
    This function is cited from cloud.google.com/natural-language/docs/analyzing-entity-sentiment
    :return a dictionary with salience values as keys, and the values are tuples in the form (entity name, entity magnitude value, entity sentiment value)
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
    report = {}
    for entity in result.entities:
        # print(u'Entity Name: "{}"'.format(entity.name))
        name = ""
        for mention in entity.mentions:
            name = mention.text.content
            # print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            # print(u'  Content : {}'.format(mention.text.content))
            # print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            # print(u'  Sentiment : {}'.format(mention.sentiment.score))
            # print(u'  Type : {}'.format(mention.type))
        try:
            magnitude_value = str(entity.sentiment)[11:str(entity.sentiment).index("\n")]
        except:
            magnitude_value = None
        try:
            sentiment_value = str(entity.sentiment)[str(entity.sentiment).index("score")+7:].strip()
        except:
            sentiment_value = None
        report[entity.salience] = (name,sentiment_value,magnitude_value)
        # print(u'Salience: {}'.format(entity.salience)) # Salience is how outstanding this word is in the sentence
        # print(u'Sentiment: {}\n'.format(entity.sentiment))
    return report

if __name__ == '__main__':
    sentiment_analyze('I took my 15112 midterm today and it was horrible. I had no idea how to do half of the problems and I am most certainly going to fail this exam.')
    entity_sentiment_analysis('I took my 15112 midterm today and it was horrible. I had no idea how to do half of the problems and I am most certainly going to fail this exam.')