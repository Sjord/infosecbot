
from textblob.classifiers import NaiveBayesClassifier
import pickle
import sys
import infosecbot.provider.reddit as reddit
from infosecbot.storage import storage

def learn_basic():
    train = []
    with open('../positive.txt') as fp:
        for line in fp:
            train.append((line, True))

    with open('../negative.txt') as fp:
        for line in fp:
            train.append((line, False))

    cl = NaiveBayesClassifier(train)


def learn_reddit():
    train = []
    spam = reddit.gather_urls(["worldnews", "programmerhumor"], "top")
    for s in spam:
        train.append((s['title'], False))

    spam = reddit.gather_urls(None, "top")
    for s in spam:
        train.append((s['title'], True))

    return train


def load_classifier():
    with open('classifier.pickle', 'rb') as fp:
        return pickle.load(fp)


def save_classifier(cl):
    with open('classifier.pickle', 'wb') as fp:
        pickle.dump(cl, fp) 


def learn_links(cl):
    train = []
    for link in storage['links']:
        if link.score != link.learned_at_score and link.score != 0:
            train.append((link.title, link.score > 0))
            link.learned_at_score = link.score
    return train


if __name__ == "__main__":
    cl = load_classifier()
    cl.update(learn_links(cl))
    save_classifier(cl)
    storage.save()
