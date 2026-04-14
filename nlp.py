# NLP

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class NLPClassifier:
    def __init__(self):
        data = [
            ["Catholics worship Mary", "Mary", "incorrect"],
            ["The Eucharist is symbolic", "Sacraments", "incorrect"],
            ["God is Trinity", "Trinity", "correct"],
            ["Faith alone saves", "Salvation", "partial"],
            ["Confession forgives sins", "Sacraments", "correct"],
        ]

        df = pd.DataFrame(data, columns=["text", "topic", "label"])

        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(df["text"])

        self.topic_model = LogisticRegression().fit(X, df["topic"])
        self.error_model = LogisticRegression().fit(X, df["label"])

    def classify(self, text):
        vec = self.vectorizer.transform([text])
        return (
            self.topic_model.predict(vec)[0],
            self.error_model.predict(vec)[0]
        )