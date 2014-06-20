class Config(object):
    articles = ["your", "my"]
    verbs = ["is", "just"]

    @property
    def nouns(self):
        raise Exception("Config subclass must implement `nouns'")

    def seeds(self):
        return [
            " ".join([a, n, v]).strip()
            for a in self.articles
            for n in self.nouns
            for v in self.verbs
        ]
