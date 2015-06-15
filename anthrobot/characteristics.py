from pattern.en import parsetree

import re

from .utils import truncate


def generate(config, tweets):
    seeds = config.characteristic_seeds()
    tweets = [t for t in tweets if not config.reject_tweet(tweets)]

    matches = get_matches(tweets, seeds)
    truncated = [truncate(m, seeds) for m in matches]
    transformed = [transform(m) for m in truncated]
    nonempty = [c for c in transformed if len(c) > 0]
    unique = list(set(nonempty))
    filtered = [c for c in unique if not filter_verbs(c)]

    return filtered


def get_matches(tweets, seeds):
    searches = [
        re.search(seed + ".*", tweet, flags=re.IGNORECASE)
        for seed in seeds
        for tweet in tweets
    ]
    return [s.group() for s in searches if s]


def transform(text):
    text = text.lower() + " "

    transformations = [
      # transform first person to third
      (" me ",    " u "),
      (" my ",    " ur "),

      (" i'm ",   " ur "),
      (" im ",    " ur "),
      (" i am ",  " ur "),
      (" i ",     " u "),
      (" i ",     " u "),
      (" i've ",  " u've "),
      (" ive ",   " u've "),
      (" i'd ",   " u'd "),
      (" id ",    " u'd "),

      (" we ",    " u "),
      (" ours ",  " urs "),
      (" our ",   " ur "),
      (" us ",    " ur "),

      # transform third person to first person
      (" his ",   " my "),
      (" him ",   " me "),
      (" her ",   " me "),
      (" he ",    " i "),
      (" she ",   " i "),
      (" he's ",  " im "),
      (" she's ", " im "),
      (" hes ",   " im "),
      (" shes ",  " im "),
      (" shes ",  " im "),

      (" n't ",   " not "),
    ]

    for orig, repl in transformations:
        text = text.replace(orig, repl)

    return text.strip()


def filter_verbs(text):
    t = parsetree(text)[0]
    if t[0].pos.startswith('RB') and len(t) > 1:
        return t[1].pos.startswith('VB')
    else:
        return t[0].pos.startswith('VB')
