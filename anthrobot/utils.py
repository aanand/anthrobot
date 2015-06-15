def truncate(text, seeds):
    text = text.lower()
    matching_seed = None
    start = len(text)

    for s in seeds:
        if s in text and text.index(s) < start:
            matching_seed = s
            start = text.index(s) + len(s)

    delims = set([
        ".", " http", ",", " and", "!", "?", "#" "~", "(", ":", ")", "^", "-",
        "@", "#", "&", ";"
    ])
    end = min([len(text)] + [text.index(d) for d in delims if d in text])

    text = filter_unicode(text[start:end]).strip()

    # preserve the "so" in "so <adjective> that"
    if matching_seed and matching_seed.split()[-1] == "so" and \
       (" " in text) and text.split()[1] == "that":

        text = "so " + text

    return text


def filter_unicode(s):
    return "".join(i for i in s if ord(i) < 128)
