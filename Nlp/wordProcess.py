import nltk 
from nltk.stem import RSLPStemmer
from term import Term
import re
class WordProcess:
    """WordProcess is low level class to pre process words, performing task as clearing stop words, stemming the words  and creating tokens from word"""
    def __init__(self):

        #rules of special values, the precedence of the rules matter
        self._rules = []
        self._rules.append("[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+") #email
        self._rules.append("([0-9]{1,2}\s+d\s?e?\s+\&?\&?[a-zà-ü]{4,9}\s+de\s+[0-9]{4}\,?\s?([àa]s\s+)?\&?\&?[0-9]{2}(:|h|h:)[0-9]{2})") #data e hora completa: 21 de agosto de 2018, as 10:40
        self._rules.append("([0-9]{1,2}\s+d\s?e?\s+\&?\&?[a-zà-ü]{4,9}\s+de\s+[0-9]{4})") #data completa 21 de agosto de 2018
        self._rules.append("([0-9]{2}(:|h|h:)[0-9]{2}(:|h|h:)[0-9]{2})") #hora hh:mm:ss
        self._rules.append("([0-9]{2}(:|h|h:)[0-9]{2})") #hora hh:mm
        #self._rules.append("(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$") #url
        #self._rules.append("[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)") #url sem http
        self._rules.append("((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))") #url
        
    def Tokenize(self,sentence):
        words = sentence.lower()
        #Before tokenize, resolve special information, such as e-mail and dates. 
        #TODO: It's important to make this more generic
        tokenList = list()
        idx = 0

        for rule in self._rules:
            regex = re.compile(rule)
            match = regex.search(words)
            while(match!=None):
                totalLength = len(words)
                end = match.end()
                start = match.start()
                value = match.group(0)
                tokenList.append(value)
                words = words[0:start] + "_" + str(idx) + "_" + words[end:totalLength]
                match = regex.search(words)
                idx+=1

        words = nltk.word_tokenize(words)
        
        #TODO: This will have performance issues. Think in a better solution
        for x in range(len(tokenList)):
            for i,item in enumerate(words):
                if item=="_"+  str(x) + "_":
                    words[i] = tokenList[x]
                

        return words

    def Stemming(self,wordArray):
        stemmer = RSLPStemmer()
        if(isinstance(wordArray, str)):
            term = Term()
            term.value = wordArray
            term.stem = stemmer.stem(wordArray.lower())
            return term
        else:
            phrase = []
            for word in wordArray:
                term = Term()
                term.value = word
                term.stem = stemmer.stem(word.lower())
                phrase.append(term)
            return phrase
    
    def RemoveStopWords(self, termArray):

        stopwords = nltk.corpus.stopwords.words('portuguese')
        #TODO: Rethink this
        #stopwords = ["a","as","o","os","de","da","do","das","dos"]
        phrase = []
        for word in termArray:
            if word.value not in stopwords:
                phrase.append(word)
        return phrase

    def RemoveSpecialChars(self, termArray):
        ##TODO: Should use something more dinamyc based on the language, as stopwords does
        chars = [",",".","?","!"]
        phrase = []
        for word in termArray:
            if word.value not in chars:
                phrase.append(word)
        return phrase

