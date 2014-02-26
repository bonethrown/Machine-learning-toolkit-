

class Name(object):

        def __init__(self, string):
                self.name = string.lower()
                self.url = ""
                self.des = ""
        def makeUnicode(self, string):
                if not isinstance(string, unicode):
                        string = string.encode('utf-8')
                        return string
                else:
                        return string
        def getNameDes(self):
                return " ".join([self.name,self.des])
        def get(self):
                return self
        def unigram(self, name):
                name = self.makeUnicode(name)
                return  name.split()
        def bigram(self, name):
                input_list = self.unigram(name)
                return zip(input_list, input_list[1:])
        def trigram(self, name):
                input_list = self.unigram(name)
                return zip(input_list, input_list[1:], input_list[2:])
        def grams(self):
                unigram = self.unigram(self.name)
                bigram = self.bigram(self.name)
                trigram = self.trigram(self.name)
                unigram.extend(bigram)
                unigram.extend(trigram)

                out = []
                for term in unigram:
                        if isinstance(term, tuple):
                                lookup = " ".join(map(unicode, term))
                                out.append(lookup)
                        else:
                                lookup = term
                                out.append(lookup)
                return out
        def matched(self, synList):
                ngrams = set(self.grams())
                matched = []
                for item in synList:
                        for gram in ngrams:
                                if item == gram:
                                        matched.append(gram)
                matched = list(set(matched))
                return matched
        def input_featurize(self, tokens):
                words = [w for w in self.unigram(tokens)]
                uniq = set(words)
                features = dict()
                for word in words:
                        features[word] = (word in uniq)
                return features

        def featurize(self):
                # call with name object
                words = [w for w in self.unigram(self.name)]
                uniq = set(words)
                features = dict()
                for word in words:
                        features[word] = (word in uniq)
                return features
