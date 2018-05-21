import pickle
#import regex 
import re
from os import path
from typing import List
import langrpc
with open(path.join(path.dirname(path.realpath(__file__)), "model.pickle"), 'br') as f:
    pipe = pickle.load(f)

LABELS = ['de', 'fr', 'en', 'it', 'sg']

VERSION_NUMBER = 1
VERSION_DESCRIPTION = "TfidfVectorizer_ngrams3-5_f6000_logreg"

#r0 = regex.compile("[^\p{l} \.,]")
rr = re.compile("[^\w \.,]|\d|_")
def sanitize(txt: str) -> str:
    txt = txt.lower()
    txt = re.sub(rr, "", txt)
    #txt = regex.sub(r0, "", txt)
    txt = re.sub(" +", " ", txt)
    txt = re.sub(" \.", ".", txt)
    return txt.strip()

def predict(text: str) -> (str, List[str], List[float]):
    results = predict_all([text])
    return results[0][0], results[1][0], results[2][0]

def predict_all(texts: List[str]) -> (List[str], List[str], List[List[str]]):
    san = [sanitize(txt) for txt in texts]
    results = pipe.predict_proba(texts)
    return san, results.argmax(axis=1).flatten(), results.tolist()