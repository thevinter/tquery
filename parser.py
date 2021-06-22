import json
import string
from collections import OrderedDict
from collections import defaultdict 
from collections import Counter

users = []

class User:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.freq = defaultdict(int)

    def add_message(self, msg):
        self.messages.append(msg)
        self.freq[msg.text] += 1

    def get_word_frequency(self, word):
        try:
            return self.freq[word]
        except:
            return None

    def get_top_words(self):
        h = Counter(self.freq)
        print(f"The most said words by {self.name} are:")
        high = h.most_common(10)
        for i in high:
            print(i[0]," :",i[1])


class Message:
    def __init__(self, text, date):
        self.text = text
        self.date = date

def add_to_user(name, word):
    usr = findUser(name)
    if usr == None:
        usr = User(name)
        users.append(usr)
    usr.add_message(word)

def findUser(name):
    for u in users:
        if u.name == name:
            return u
    return None


def read_json():
    translator = str.maketrans('', '', string.punctuation)
    f = open("/home/vinter/Documents/FruppoChat/result.json", "r")
    stop = open("/home/vinter/src/python/frupparser/stopwords.txt")
    f = json.loads(f.read())
    texts = defaultdict(int)
    eng = open("/home/vinter/src/python/frupparser/eng_stopwords.txt")

    stopwords = [] 
    blacklist = ["Combot", "CryptoWhale", "Ultimora Bot", "LastFM Robot"]
    for l in stop.readlines():
        stopwords.append(l.strip())
    for l in eng.readlines():
        stopwords.append(l.strip())
    stopwords.append("status")
    stopwords.append('')

    messages = f['messages']
    for m in messages:
        if m['type'] == 'message' and m['from'] not in blacklist:
            if type(m['text']) == list:
                for mes in m['text']:
                    if(type(mes) == dict):
                        message=mes['text'].lower().strip()
                    else:
                        message=mes.lower().strip()
                    for w in message.split(" "):
                        if w != '' and w not in stopwords and len(w) > 2:
                            w = w.translate(translator)
                            msg = Message(w, m['date'])
                            add_to_user(m['from'], msg)
                            texts[w] += 1
            else:
                message = m['text'].lower().strip()
                for w in message.split(" "):
                    if w != '' and w not in stopwords and len(w) > 2:
                        w = w.translate(translator)
                        msg = Message(w, m['date'])
                        add_to_user(m['from'], msg)
                        texts[w] += 1

    texts = sorted(texts.items(), key = lambda i: i[1], reverse=True)
    f = open("output.txt", "w")
    for t in texts:
        out = str(t[0]) + ',' + str(t[1]) + '\n'
        f.write(out)

read_json()
f = open('output.txt', 'r')
texts = defaultdict(int)
for l in f.readlines():
    vals = l.split(",")
    if len(vals) == 1:
        continue
    if vals[0] == '':
        continue
    texts[vals[0].strip()] += int(vals[1].strip())

def find_word_freq(word):
    freq=list(texts.keys()).index(word)

    print(f"The word {word} is the {freq}th most used word in the group and it has been used {texts[word]} times")



#h = Counter(texts)

#print("Top 10 words:")
#high = h.most_common(10)
#for i in high:
#    print(i[0]," :",i[1])


def check_word_usage(word):
    total_max = -1
    max_user = None
    for user in users:
        max = user.get_word_frequency(word)
        if max > total_max:
            total_max = max
            max_user = user.name
        if max == None:
            continue
        print(f"{user.name} said the word {word} {max} times")
    print(f"The person that said it more is {max_user}")


def find_word_for_user(word, user):
    print(f"The user {user} said {word} {findUser(user).get_word_frequency(word)} times")

print('---------------------------------------')

for user in users:
    user.get_top_words()


print('---------------------------------------')

