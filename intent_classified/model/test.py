import pickle, re, warnings
from nltk.corpus import stopwords

warnings.filterwarnings("ignore")
STOP = set(stopwords.words("english"))

with open("intent_model1.pkl", "rb") as f:
    bundle = pickle.load(f)

lemmatizer = bundle["lemmatizer"]
vectorizer = bundle["tfidf"]
model = bundle["classifier"]

def preprocess(text):
    text = re.sub(r"[^a-z\s]", "", text.lower())
    words = [lemmatizer.lemmatize(w, pos="v") for w in text.split() if w not in STOP]
    return " ".join(words)

def predict_intent(text, threshold=0.6):

    x = vectorizer.transform([preprocess(text)])
    probs = model.predict_proba(x)[0]
    idx = probs.argmax()
    return text.append(model.classes_[idx]) if probs[idx] >= threshold else "other"

def predict_intents_list(texts, threshold=0.6):
    X = vectorizer.transform([preprocess(t) for t in texts])
    probs = model.predict_proba(X)

    results = []
    for p in probs:
        idx = p.argmax()
        results.append(model.classes_[idx] if p[idx] >= threshold else "other")

    return results


