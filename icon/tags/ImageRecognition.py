import io
import os


from google.cloud import vision
from google.cloud.vision import types

def RecognizeImage(path):
    """Detects labels in the file.
    """
    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(
        os.path.dirname(__file__),"tag",
         path)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.web_detection(image=image)
    labels = response.web_detection

    result = {}
    for label in labels.web_entities:
        result[label.score] = label.description

    return result


if __name__ == '__main__':
    pass
