from __future__ import division

from pattern.en import parsetree, conjugate, lemma
import re
import numpy as np
from numpy.random import choice

from .blacklist import BLACKLIST

SEARCH_SEEDS = ['cat is', 'kitty is', 'cat just', 'kitty just', 'sometimes my cat']

def reject_tweet(tweet):
    return any(x in tweet for x in BLACKLIST)

def filter_unicode(s): return "".join(i for i in s if ord(i)<128)

def truncate(text, seeds=None):
    text = text.lower()

    start = len(text)

    if seeds is None:
        seeds = SEARCH_SEEDS

    for s in SEARCH_SEEDS:
        if s in text and text.index(s) < start:
            start = text.index(s) + len(s)

    delims = set([".", " http", ",", " and", "!", "?", "#" "~", "(", ":", ")", "^", "-", "@", "#", "&", ";"])
    end = min([len(text)] + [text.index(d) for d in delims if d in text])
    return filter_unicode(text[start:end]).strip()


def transform_cat_action(text):
    transformations = []

    # text
    text = text.lower() + " "

    # transform the verb
    orig_verb = text.split()[0]

    if "fuck" in orig_verb:
        transformations += [(orig_verb, "")]
        try:
            orig_verb = text.split()[1]
        except IndexError:
            return ''

    elif "something" in orig_verb or "anything" in orig_verb:
        return ''

    new_verb = conjugate(lemma(orig_verb), person=3)

    # weird "lies" bug?
    if new_verb == 'layers':
        new_verb = 'lies'

    transformations += [(orig_verb, new_verb)]

    # transform first person to third
    transformations += [(" me ", " u ")]
    transformations += [(" my ", " ur ")]

    transformations += [(" i'm ", " ur ")]
    transformations += [(" im ", " ur ")]
    transformations += [(" i am ", " ur ")]
    transformations += [(" i ", " u ")]
    transformations += [(" i ", " u ")]
    transformations += [(" i've ", " u've ")]
    transformations += [(" ive ", " u've ")]
    transformations += [(" i'd ", " u'd ")]
    transformations += [(" id ", " u'd ")]

    transformations += [(" we ", " u ")]
    transformations += [(" ours ", " urs ")]
    transformations += [(" our ", " ur ")]
    transformations += [(" us ", " ur ")]

    # transform third person to gender-neutral
    transformations += [(" his ", " her ")]
    transformations += [(" him ", " her ")]
    transformations += [(" her ", " her ")]
    transformations += [(" he ", " she ")]
    transformations += [(" she ", " she ")]
    transformations += [(" he's ", " she's ")]
    transformations += [(" she's ", " she's ")]
    transformations += [(" hes ", " she's ")]
    transformations += [(" shes ", " she's ")]

    transformations += [(" n't ", " not ")]

    for orig, repl in transformations:
        text = text.replace(orig, repl)

    return text.strip()

def transform_cat_characteristic(text):
    transformations = []

    # text
    text = text.lower() + " "

    # transform first person to third
    transformations += [(" me ", " u ")]
    transformations += [(" my ", " ur ")]

    transformations += [(" i'm ", " ur ")]
    transformations += [(" im ", " ur ")]
    transformations += [(" i am ", " ur ")]
    transformations += [(" i ", " u ")]
    transformations += [(" i ", " u ")]
    transformations += [(" i've ", " u've ")]
    transformations += [(" ive ", " u've ")]
    transformations += [(" i'd ", " u'd ")]
    transformations += [(" id ", " u'd ")]

    transformations += [(" we ", " u ")]
    transformations += [(" ours ", " urs ")]
    transformations += [(" our ", " ur ")]
    transformations += [(" us ", " ur ")]

    # transform third person to first person
    transformations += [(" his ", " my ")]
    transformations += [(" him ", " me ")]
    transformations += [(" her ", " me ")]
    transformations += [(" he ", " i ")]
    transformations += [(" she ", " i ")]
    transformations += [(" he's ", " im ")]
    transformations += [(" she's ", " im ")]
    transformations += [(" hes ", " im ")]
    transformations += [(" shes ", " im ")]
    transformations += [(" shes ", " im ")]

    transformations += [(" n't ", " not ")]

    for orig, repl in transformations:
        text = text.replace(orig, repl)

    return text.strip()
    

def get_seed_tweets(twitter):
    cat_tweets = []

    for seed in SEARCH_SEEDS:
        i = None
        for searches in range(30):
            cat_tweets += twitter.search('"' + seed + '"', start=i, count=100)
            i = cat_tweets[-1].id
            print("got {} tweets".format(len(cat_tweets)))
            #print(cat_tweets[-100:])

    return list(set(t.text for t in cat_tweets))

def create_actions(raw_tweets):
    catting = []
    raw_tweets = [x for x in raw_tweets if not reject_tweet(x)]
    for seed in SEARCH_SEEDS:
        catting += [re.search(seed + " [a-z]+ing.*", t, flags=re.IGNORECASE) for t in raw_tweets]

    catting = [x.group() for x in catting if x]

    return list(set(transform_cat_action(truncate(x)) for x in catting))

def filter_verbs(text):
    t = parsetree(text)[0]
    if t[0].pos.startswith('RB') and len(t) > 1:
        return t[1].pos.startswith('VB')
    else:
        return t[0].pos.startswith('VB')


def create_characteristics(raw_tweets):
    catting = []
    seeds = []

    raw_tweets = [x for x in raw_tweets if not reject_tweet(x)][-10000:]

    for seed1 in ['cat is', 'kitty is']:
        for seed2 in ['so', 'really']:
            seeds += ' '.join((seed1, seed2))

    for seed in seeds:
        catting += [re.search(seed + ".*", t, flags=re.IGNORECASE) for t in raw_tweets]

    catting = [x.group() for x in catting if x]

    raw_chars = [transform_cat_characteristic(truncate(x, seeds)) for x in catting]
    raw_chars = list(set(c for c in raw_chars if len(c) > 0))

    return [c for c in raw_chars if not filter_verbs(c)]

def get_new_actions(start=0):
    with codecs.open('mined_cat_tweets.txt', encoding='utf-8') as f:
        raw_tweets = [l.strip() for i, l in enumerate(f.readlines()) if i > start and any(x in l.lower() for x in ('cat', 'kitty'))]
    raw_tweets = list(set(raw_tweets))
    actions = create_actions(raw_tweets)
    return list(set(actions))

def cat_talk(mode=None):
    weights = np.array([1/(1+n) for n in xrange(5)])
    
    say = ''

    if mode == 'meow' or mode is None:
        for _ in xrange(choice(range(1,5), p=(weights[:-1] / weights[:-1].sum()))):
            say += 'm'
            
            say += choice(range(1,5), p=(weights[:-1] / weights[:-1].sum())) * 'e'
            if np.random.random() > 0.1:
                say += choice(range(1,5), p=(weights[:-1] / weights[:-1].sum())) * 'o'
            say += choice(range(1,5), p=(weights[:-1] / weights[:-1].sum())) * 'w'

            say += ' '

        say = say.strip()

        if np.random.random() > 0.3:
            say += choice(['.', '!', '...', '~', '?']) * choice(range(1,4), p=(weights[:-2] / weights[:-2].sum()))

    #else mode == 'purr':
    else:
        for _ in xrange(choice(range(1,5), p=(weights[:-1] / weights[:-1].sum()))):
            say += 'pu'
            
            say += choice(range(1,5), p=(weights[:-1] / weights[:-1].sum())) * 'r'
            say += choice(range(1,5), p=(weights[:-1] / weights[:-1].sum())) * 'r'

            say += ' '

    return say.strip()
