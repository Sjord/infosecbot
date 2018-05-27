import re

class LinkClassifier:
    def __init__(self, bayes):
        self.bayes = bayes
        
    def link_to_text(self, link):
        domain_words = re.sub(r'[^a-z]+', ' ', link.domain)
        return link.title.lower() + " " + domain_words + " " + link.scheme

    def learn(self, links):
        train = []
        for link in links:
            if link.score != 0:
                train.append((self.link_to_text(link), link.score > 0))
                link.learned_at_score = link.score
        self.bayes.update(train)

    def classify(self, link):
        probdist = self.bayes.prob_classify(self.link_to_text(link))
        return probdist.prob(True)
