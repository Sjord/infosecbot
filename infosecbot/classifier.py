
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import HashingVectorizer
from infosecbot.storage import storage


def load_classifier():
    classifier = InfosecClassifier()
    classifier.learn(storage["links"])
    return classifier


def get_link_text(link):
    return " ".join((link.title.lower(), link.domain.replace(".", " ")))


class InfosecClassifier:
    def __init__(self):
        self.bernoulli = BernoulliNB()
        self.vectorizer = HashingVectorizer(preprocessor=get_link_text)

    def learn(self, links):
        links = [link for link in links if link.score != 0 and link.score != link.learned_at_score]
        classifications = [link.score > 0 for link in links]
        features = self.vectorizer.fit_transform(links, classifications)
        self.bernoulli.fit(features, classifications)

    def classify(self, link):
        features = self.vectorizer.fit_transform([link])
        return self.bernoulli.predict(features)


if __name__ == "__main__":
    c = InfosecClassifier()
    c.learn(storage["links"])
    l = storage["links"][0]
    res = c.classify(l)
    print(l, res)
   

