
def load_words(wordfile):
    words = []
    with open(wordfile) as fp:
        for line in fp:
            words.append(line.strip())
    return words
