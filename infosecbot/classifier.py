
from textblob.classifiers import NaiveBayesClassifier
import pickle
import sys


def learn_basic():
    train = []
    with open('../positive.txt') as fp:
        for line in fp:
            train.append((line, True))

    with open('../negative.txt') as fp:
        for line in fp:
            train.append((line, False))

    cl = NaiveBayesClassifier(train)
    with open('classifier.pickle', 'wb') as fp:
        pickle.dump(cl, fp) 


if __name__ == "__main__":
    # learn_basic()
    with open('classifier.pickle', 'rb') as fp:
        cl = pickle.load(fp)
    print(cl.classify(sys.argv[1]))
