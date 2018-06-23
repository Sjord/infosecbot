from nltk import NaiveBayesClassifier
import nltk
from infosecbot.storage import storage
import re


def link_features(link, words, prop):
    return {w: w in link.__dict__[prop] for w in words}


def load_words(wordfile):
    words = []
    with open(wordfile) as fp:
        for line in fp:
            words.append(line.strip())
    return words


def load_bayes():
    words = load_words("titlewords.txt")
    feature_sets = []
    for link in storage['links']:
        if link.score != 0:
            features = {w: re.search(r"\b"+w+r"\b", link.title.lower()) is not None for w in words}
            feature_sets.append((features, link.score > 0))
    train_set = feature_sets[0::2]
    test_set = feature_sets[1::2]
    bayes = NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(bayes, test_set))

def load_bayes2():
    words = load_words("domainwords.txt")
    feature_sets = []
    for link in storage['links']:
        if link.score != 0:
            features = {w: w in link.domain for w in words}
            feature_sets.append((features, link.score > 0))
    train_set = feature_sets[0::2]
    test_set = feature_sets[1::2]
    bayes = NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(bayes, test_set))


def load_bayes3(titlewords):
    # titlewords = load_words("titlewords.txt")
    domainwords = load_words("domainwords.txt")
    feature_sets = []
    for link in storage['links']:
        if link.score != 0:
            features = {"domain-" + w: w in link.domain for w in domainwords}
            features.update({"title-" + w: re.search(r"\b"+w+r"\b", link.title.lower()) is not None for w in titlewords})
            features["is-https"] = link.url.startswith("https:")
            feature_sets.append((features, link.score > 0))
    train_set = feature_sets[0::2]
    test_set = feature_sets[1::2]
    bayes = NaiveBayesClassifier.train(train_set)
    return nltk.classify.accuracy(bayes, test_set)




    


if __name__ == "__main__":
    titlewords = load_words("titlewords.txt")
    print(load_bayes3(titlewords))
    for i in range(len(titlewords)):
        print(load_bayes3(titlewords[0:i] + titlewords[i+1:]), titlewords[i])
