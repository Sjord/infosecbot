
from textblob.classifiers import NaiveBayesClassifier
import pickle
import sys
import infosecbot.provider.reddit as reddit
from infosecbot.storage import storage
from infosecbot.linkclassifier import LinkClassifier

def learn_basic():
    train = []
    with open('positive.txt') as fp:
        for line in fp:
            train.append((line, True))

    with open('negative.txt') as fp:
        for line in fp:
            train.append((line, False))

    cl = NaiveBayesClassifier(train)
    return cl


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


def get_learnable_links():
    train = []
    for link in storage['links']:
        if link.score != link.learned_at_score and link.score != 0:
            train.append(link)
    return train


def initialize_classifier():
    bayes = learn_basic()
    classifier = LinkClassifier(bayes)
    classifier.learn(storage['links'])
    return classifier


if __name__ == "__main__":
    cl = load_classifier()

    action = sys.argv[1]
    if action == "show":
        cl.bayes.show_informative_features(n=100)
    elif action == "init":
        cl = initialize_classifier()
        save_classifier(cl)
    elif action == "update":
        cl.learn(get_learnable_links())
        save_classifier(cl)
        storage.save()
    else:
        raise ValueError("action")
