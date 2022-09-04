import nltk
import nltk.data
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import pandas as pd
import re
import string
from textblob import TextBlob
from spellchecker import SpellChecker
sent = SentimentIntensityAnalyzer()
spell = SpellChecker()
spell.word_frequency.remove_words(["ghat","nott", "ro", "ahd", "tine","peopl", "hav"])
spell.word_frequency.load_words(["afrocaribbean",'aftermath','afternoon','afterwards',"birdwatching",
                                 "breathlessness","catastrophising","disenfranchisement","dysthymia",
                                 "encephalomyelitis","extroversion","foodbank","friendlessness",
                                 "glastonbury","goosebump","groupthink","himalaya","hypnopompic",
                                 "instrumentalist","introversion","inwardness","introvertedness",
                                 "internalisation","judgementalism","lgbtq","lincolnshire","londoner",
                                 "marginalization","misattuned","monstrousness","misophonia",
                                 'neurodivergent','neurotherapy','neurotypical','neurotypicals',
                                 "ostracization","platitudinous","pleasantry","polytunnel","rightmove",
                                 "steppenwolf",'symptomatically','teacake','technophobia',"tradesperson",
                                 "understimulation", "tv", "tvs", "bbc","fomo"])
wordsToStem = ["lonely","loneliness","feeling","feel"]

def clean_text(text):
    #Make text lowercase, remove punctuation, remove numbers.
    #Removes repeating letters - "literallllllllly" -> "literally"
    #corrects spelling.
    text = str(text)
    text = text.lower()
    #I'd, I'm, and I'll arent detectable by stopwords if the punctuation is removed
    text = re.sub(r"i'd", "i would", text)
    text = re.sub(r"i'll", "i will", text)
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"i've", "i have", text)
    #Common spelling corrections the spellcheck can't deal with
    text = re.sub(r" u ", " you ", text)
    text = re.sub(r" ur ", " your ", text)
    text = re.sub(r"ahd", "and", text)
    #Punctuation removing, special characters are really annoying
    text = re.sub("\[\]", " ", text)
    text = re.sub("[,/\-\.]", " ", text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[œâžðŸ˜Š€£¢ã²°¨ä©±«¦»•‰—‘’“”…]', "", text)
    text = re.sub(r'\x9d', "", text)#This is whitespace when viewed in Excel?? Idk why
    text = re.sub(r'\xad', "", text)#messes with me soo i gotta take them out
    #Removing repeating characters
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    #This is where things get specific. If there's a typo that's bothering you, 
    #place the regular expression down here.
    #Trying to put spaces in places people forgot the spaces (typos)
    text = re.sub(r'(being)([^s ])', r'\1 \2', text)#being
    text = re.sub(r'( beings)([^ ])', r'\1 \2', text)#beings
    text = re.sub(r'( with)([^eyiaodhs ])', r'\1 \2', text)#with
    text = re.sub(r'(people)([^drshl ])', r'\1 \2', text)#people
    text = re.sub(r'( peoples)([^drhl ])', r'\1 \2', text)#peoples
    text = re.sub(r'( not)([^aecuihotw ])', r'\1 \2', text)#not
    text = re.sub(r'(loneliness)([^e ])', r'\1 \2', text)#loneliness
    text = re.sub(r'( lonely)([^ ])', r'\1 \2', text)#lonely
    text = re.sub(r'( feel)([^esi ])', r'\1 \2', text)#feel
    text = re.sub(r'( and)([^sraieo ])', r'\1 \2', text)#and
    text = re.sub(r'( self)([^seidwnlh ])', r'\1 \2', text)#self
    text = re.sub(r'(feeling)([^s ])', r'\1 \2', text)#feeling
    #putting spaces in words where people forget hyphens! 
    text = re.sub(r'noone ', r"no one ", text)
    text = re.sub(r'backscratcher ', r"back scratcher ", text)
    text = re.sub(r'closeminded ', r"close minded ", text)
    text = re.sub(r'comfortzone ', r"comfort zone ", text)
    text = re.sub(r'downtrodden ', r"down trodden ", text)
    text = re.sub(r'mothertongue ', r"mother tongue ", text)
    text = re.sub(r'openminded ', r"open minded ", text)
    text = re.sub(r'phantomlimb ', r"phantom limb ", text)
    text = re.sub(r'weakminded ', r"weak minded ", text)
    text = re.sub(r'smalltalk ', r"small talk ", text)
    text = re.sub(r'mindnumbing ', r"mind numbing ", text)
    text = re.sub(r'gettogethers', r"get togethers", text)
    text = re.sub(r'illhealth', r"ill health", text)
    text = re.sub(r'illnessanxiety', r"illness anxiety", text)
    #these guys are just messing with my topics im not gonna lie
    text = re.sub(r' esp ', r" especially ", text)
    text = re.sub(r' nderstood', r" understood", text)
    text = re.sub(r' afriend ', r" a friend ", text)
    text = re.sub(r'compassionlove', r"compassion love", text)
    text = re.sub(r'tosnuggkeveith', r"to snuggle with", text)
    text = re.sub(r'sightssounds', r"sights sounds", text)
    text = re.sub(r'relationshipwith', r"relationship with", text)
    text = re.sub(r'signicantvroles', r"significant roles", text)
    text = re.sub(r'disalutioned ', r"disillusioned ", text)
    text = re.sub(r'withanother', r"with another", text)
    text = re.sub(r'withsomeone', r"with someone", text)
    text = re.sub(r'soneone', r"someone", text)
    text = re.sub(r' feb ', r" february ", text)
    text = re.sub(r' tis ', r" this ", text)
    text = re.sub(r' ti ', r" to ", text)
    text = re.sub(r' ia ', r" is ", text)
    text = re.sub(r' tine ', r" time ", text)
    #correct that spelling ehh macarina
    for word in spell.unknown(str(text).split()):
        correctword = spell.correction(word)
        text = re.sub(r"\b{}\b".format(word), correctword, text)
    
    return text

cleaning = lambda x: clean_text(x)

def remove_stopwords(text):
    #removes stopwords (me, my, him, if, etc...)
    #lemmatizes words ("making" becomes "make")
    lemmatizer = nltk.WordNetLemmatizer()
    text = str(text)
    noStopWords = ""
    Stopwords = stopwords.words('english')
    extrawords = ["like"]
    for word in str(text).split():
        if word == "no" or word == "not" or word == "us" or word == "own":
            noStopWords = noStopWords + word + " "
        
        elif word not in Stopwords and word not in extrawords:
            word = lemmatizer.lemmatize(word, pos = "v")
            noStopWords = noStopWords + word + " "      
    
    return noStopWords
            
stopwordRemoval = lambda x: remove_stopwords(x)

def polarityCalc(text):
    return (sent.polarity_scores(text)["compound"])

def subjectivityCalc(text):
    return TextBlob(text).sentiment.subjectivity
    
def calcWordCount(dataName, colName):
    dataName["Word_Count"] = dataName[colName]
    for  i, entry in enumerate(dataName["Word_Count"]):
        entry = str(entry)
        if entry != "-99":
            wc = len(entry.split())
            dataName.loc[i, "Word_Count"] = int(wc)
        else:
            dataName.loc[i, "Word_Count"] = int(0)

    dataName["Length"] = dataName[colName].str.len()

def calcPolSub(dataName, colName):
    dataName["Subjectivity"] = dataName[colName]
    dataName["Polarity"] = dataName[colName]
    for  i, entry in enumerate(dataName["Subjectivity"]):
        entry = str(entry)
        if entry != "-99":
            subjectivity = subjectivityCalc(entry)
            polarity = polarityCalc(entry)
            dataName.loc[i, "Subjectivity"] = subjectivity
            dataName.loc[i, "Polarity"] = polarity
        else:
            dataName.loc[i, "Subjectivity"] = ""
            dataName.loc[i, "Polarity"] = ""

def getMisspelled(text):
    misspellings = set()
    for i, entry in enumerate(text):
        for word in spell.unknown(str(text[i]).split()):
            misspellings.add(word)
    return misspellings


