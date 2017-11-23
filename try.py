import os
import pickle

with open(os.path.join('tags','tag.pickle'),'rb') as f:
    result = pickle.load(f)


