Lingo is a personal diary management app that helps users record and keep track of diary, create reminders, analyze and visualize personal sentiment status. What's cooler about it is that all of these can be done through a voice assistant that the user gets to name when initializing. The app can extract important entities from diaries and display them on a timeline using tags represented by emojis. Also, the users can see how sentiment values reflected by their diaries change over a period so that they can keep track of their mental status over time. All personal diaries and reminders are saved locally.
To run the project, you will have the following libraries installed:
Pygame
Google Speech Recognition API
Google Natural Language API
Google Vision API
Pyaudio
Six
NLTK + Scikit-learn (for running the sentiment analysis locally)
Pickle

Use the following command in command prompt to install the corresponding module:
Pygame: "pip install pygame"
Google API client library: "pip install --upgrade google-api-python-client"
Pyaudio: "pip install pyaudio"
Six: "pip install Six"
NLTK: "pip install NLTK"
Scikit-learn: "pip install -U scikit-learn"
Pickle: "pip install pickle"

To authenticate Google API:
Follow the instructions to create a service account,
https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating_a_service_account
Select JSON as your key type.
Once complete, your service account key is downloaded to your browser's default location.
Then in command prompt,
"export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_KEY_FILE"
Replace PATH_TO_KEY_FILE with the path to your JSON service account file. GOOGLE_APPLICATION_CREDENTIALS should be written out as-is (it's not a placeholder in the example above).