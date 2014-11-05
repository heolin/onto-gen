#!/usr/bin/env python
# -*- coding: utf-8 -*

import math
#from polimorf import Lemmatizer

_WORD_MIN_LENGTH = 3

_ENGLISH_STOP_WORDS = frozenset([
'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been',
'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can',
'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
'yourselves', 'the'])

_POLISH_STOP_WORDS = frozenset([u'a', u'acz', u'aczkolwiek', u'aj', u'albo', u'ale', u'ależ', u'ani', u'aż', u'bardziej', u'bardzo', u'bo', u'bowiem', u'by', u'byli', u'bynajmniej', u'być', u'był', u'była', u'było', u'były', u'będzie', u'będą', u'cali', u'cała', u'cały', u'ci', u'cię', u'ciebie', u'co', u'cokolwiek', u'coś', u'czasami', u'czasem', u'czemu', u'czy', u'czyli', u'daleko', u'dla', u'dlaczego', u'dlatego', u'do', u'dobrze', u'dokąd', u'dość', u'dużo', u'dwa', u'dwaj', u'dwie', u'dwoje', u'dziś', u'dzisiaj', u'gdy', u'gdyby', u'gdyż', u'gdzie', u'gdziekolwiek', u'gdzieś', u'i', u'ich', u'ile', u'im', u'inna', u'inne', u'inny', u'innych', u'iż', u'ja', u'ją', u'jak', u'jakaś', u'jakby', u'jaki', u'jakichś', u'jakie', u'jakiś', u'jakiż', u'jakkolwiek', u'jako', u'jakoś', u'je', u'jeden', u'jedna', u'jedno', u'jednak', u'jednakże', u'jego', u'jej', u'jemu', u'jest', u'jestem', u'jeszcze', u'jeśli', u'jeżeli', u'już', u'ją', u'każdy', u'kiedy', u'kilka', u'kimś', u'kto', u'ktokolwiek', u'ktoś', u'która', u'które', u'którego', u'której', u'który', u'których', u'którym', u'którzy', u'ku', u'lat', u'lecz', u'lub', u'ma', u'mają', u'mało', u'mam', u'mi', u'mimo', u'między', u'mną', u'mnie', u'mogą', u'moi', u'moim', u'moja', u'moje', u'może', u'możliwe', u'można', u'mój', u'mu', u'musi', u'my', u'na', u'nad', u'nam', u'nami', u'nas', u'nasi', u'nasz', u'nasza', u'nasze', u'naszego', u'naszych', u'natomiast', u'natychmiast', u'nawet', u'nią', u'nic', u'nich', u'nie', u'niech', u'niego', u'niej', u'niemu', u'nigdy', u'nim', u'nimi', u'niż', u'no', u'o', u'obok', u'od', u'około', u'on', u'ona', u'one', u'oni', u'ono', u'oraz', u'oto', u'owszem', u'pan', u'pana', u'pani', u'po', u'pod', u'podczas', u'pomimo', u'ponad', u'ponieważ', u'powinien', u'powinna', u'powinni', u'powinno', u'poza', u'prawie', u'przecież', u'przed', u'przede', u'przedtem', u'przez', u'przy', u'roku', u'również', u'sam', u'sama', u'są', u'się', u'skąd', u'sobie', u'sobą', u'sposób', u'swoje', u'ta', u'tak', u'taka', u'taki', u'takie', u'także', u'tam', u'te', u'tego', u'tej', u'temu', u'ten', u'teraz', u'też', u'to', u'tobą', u'tobie', u'toteż', u'trzeba', u'tu', u'tutaj', u'twoi', u'twoim', u'twoja', u'twoje', u'twym', u'twój', u'ty', u'tych', u'tylko', u'tym', u'u', u'w', u'wam', u'wami', u'was', u'wasz', u'wasza', u'wasze', u'we', u'według', u'wiele', u'wielu', u'więc', u'więcej', u'wszyscy', u'wszystkich', u'wszystkie', u'wszystkim', u'wszystko', u'wtedy', u'wy', u'właśnie', u'z', u'za', u'zapewne', u'zawsze', u'ze', u'zł', u'znowu', u'znów', u'został', u'żaden', u'żadna', u'żadne', u'żadnych', u'że', u'żeby'])


POLISH = "PL"
ENGLISH = "EN"

lemmatizer = None

def word_split( text):
    """
    Split a text in words. Returns a list of tuple that contains
    (word, location) location is the starting byte position of the word.
    """
    word_list = []
    wcurrent = []
    windex = None

    for i, c in enumerate(text.decode('utf-8')):
        if c.isalnum():
            wcurrent.append(c)
            windex = i
        elif wcurrent:
            word = u''.join(wcurrent)
            word_list.append((windex - len(word) + 1, word))
            wcurrent = []

    if wcurrent:
        word = u''.join(wcurrent)
        word_list.append((windex - len(word) + 1, word))

    return word_list


def words_cleanup(words, lang):
    """
    Remove words with length less then a minimum and stopwords.
    """
    cleaned_words = []
    stop_word = _ENGLISH_STOP_WORDS
    if lang == POLISH:
        stop_word = _POLISH_STOP_WORDS
    for index, word in words:
        if len(word) < _WORD_MIN_LENGTH or word in stop_word:
            continue
        cleaned_words.append((index, word))
    return cleaned_words


def words_normalize(words):
    """
    Do a normalization precess on words. In this case is just a tolower(),
    but you can add accents stripping, convert to singular and so on...
    """
#    global lemmatizer
#    if lemmatizer == None:
#        lemmatizer = Lemmatizer()

    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
        if len(wnormalized) > _WORD_MIN_LENGTH:
            #wnormalized = lemmatizer.lemmatize_word(word.encode('utf-8')).decode('utf-8')
            wnormalized = word
        normalized_words.append((index, wnormalized))
    return normalized_words


def word_index(text, lang="PL"):
    """
    Just a helper method to process a text.
    It calls word split, normalize and cleanup.
    """
    words = word_split(text)
    words = words_normalize(words)
    words = words_cleanup(words, lang)

    return words

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
