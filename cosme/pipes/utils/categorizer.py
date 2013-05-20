import time
import editdist
from nltk import metrics, stem, tokenize
from nltk import NaiveBayesClassifier,classify
import pickle
from nltk.tokenize import RegexpTokenizer

#requires a list of stinrings in flattened format
def catSType(*fields):
    terms = ["gays","gay","boy","shemale","tranny","trany","wank","wanking","jerking","transsexuals"]
    isGay = 0
    for field in fields:
        if field:
            field = field.lower().strip()
            for f in terms:
                if field.find(f) > 0:
                    isGay = 1
                    break
 
    print "################### isgay on %s is %s"%(fields,isGay) 
    return isGay
    

class Matcher:
    

    def __init__(self,config,threshold=1,tlength=2):
        
        self.conf = ""
        self.toMatch = []
        self.thresh = threshold
        self.tlength = tlength
        try:
            self.config = config
            fp = open(config,'r')
            print "loading config"
            for line in fp.readlines():
                #print "processing line %s"%line
                self.toMatch.append(line.lower().strip().split(" "))
            fp.close()
        except Exception, e:
            #TODO make output legible throw exception
            print "###ERROR In MATCHER : unable to load config"
            print e
        
    def Match(self, text):
        #tokeniz and normalize our text
        textArr = tokenize.wordpunct_tokenize(text.lower().strip())
        hits = 0
        results = []
        secondary = []
        #-tlength as we need to iterate over window size of words
        for ti in xrange(0,len(textArr)-self.tlength):
            
                for termT in self.toMatch:
                    #so whats the distance between our first token?
                
                    dist1 = editdist.distance(textArr[ti],termT[hits])
                    if  dist1 <= self.thresh:
                        if len(termT) <= 1:
                            print "got hit with %s"%termT
                            results.append(termT[hits])
                        else:
                            dist2 = editdist.distance(textArr[ti+1],termT[hits+1])
                            print "distance between %s and %s is %s" %(textArr[ti+1],termT[hits+1],dist2)
                            #WARNING: this will only work for 2-grams where the tlength is an n-gram.
                            if  dist2 <= self.thresh:
                                #we have a close hit lets check if the second term in tuple is a hit as well.
                                #hits = hits + 1
                                results.append("%s %s"%(termT[hits],termT[hits+1]))
                                #print termT
                                #print "got hit on term %s"%results
                        
                #looks like we've found a match
               
               
        #print secondary
        #we're done shit....
        return results

        
class Categorizer:
    def __init__(self,pathToModel,features):
        #initialize categorizer with model.
        self.tokenizer =  RegexpTokenizer('[A-Za-z]\w+')
        fp = open(pathToModel,"r")
        fpf = open(features,"r")
        model = pickle.load(fp)
        self.features = pickle.load(fpf)
        fp.close()
        fpf.close()
        self.classifierNB = model
        
    def classify(self,text):
        featureSet = self.naiveFeatures(text)
        #print featureSet
        labels = self.classifierNB.classify(featureSet)
        labelsProbDist = self.classifierNB.prob_classify(featureSet)
        return labels

        
    def naiveFeatures(self,vid,train=False):
        vidTokens =  self.tokenizer.tokenize(vid.lower().strip())
        vid = set(vidTokens)
        #print vid
        features = {}
        if train:
            for word in self.features:
                features[word] = (word in vid)
        else:
            for word in vid:
                features[word] = (word in self.features)
        return features


if __name__ == '__main__':
    text = "Busty Bvlgari louise at kinky orgya BigTit Pornstar Aletta Ocean in uniform anally fucks sucks unhappy custo"
    dict = '/home/dev/aa_nubunu/data/ling/brands.list'
    text_cat = "Bvlgari"
   
    print "running tests"
    print"matching on: %s"%text
    
    
    print "using dictoinary: %s" % dict
    m = Matcher(dict)
    start = time.time()
    result = m.Match(text)
    end = time.time()
    print "results found %s"%result
    print "time: %s ms"%(end-start)
        
    print "testing categorizer"
    print  "text:%s"%text_cat
    c = Categorizer('serialized-model-python-cats','featuresCat')
    label =  c.classify(text_cat)
    print "best  found label is"
    print label
    
    print "testing categorizer done"
