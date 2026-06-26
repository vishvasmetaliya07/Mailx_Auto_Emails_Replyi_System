import pickle

# Load saved model
with open("intent_model.pkl", "rb") as f:
    model_bundle = pickle.load(f)

lemmatizer = model_bundle["lemmtizer"]
vectorizer = model_bundle["vector"]
classifier = model_bundle["model"]

# Example inference
texts = ["Hi there", "I want pizza", "Bye!"]

# Preprocess → Vectorize → Predict
lemmatized_texts = lemmatizer.transform(texts)
X = vectorizer.transform(lemmatized_texts)
predicted_intents = classifier.predict(X)

print(predicted_intents)  # ['greet', 'order_food', 'goodbye']
