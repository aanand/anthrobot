import unittest
from anthrobot import characteristics
from anthrobot.config import Config


class Cat(Config):
    nouns = ["cat", "kitty"]


class CharacteristicsTest(unittest.TestCase):
    tweets = [
        u'@Tiorahkose aww ur cat is so cute',  # NOQA
        u"seriously my cat is so annoying it's made me hate all cats and i used to be such a cat lady. dogs are the way to go",  # NOQA
        u'my cat is so good and responsive and obedient except when it comes to destroying the freaking couch. its extremely aggravating',  # NOQA
        u'this cat is so annoying http://t.co/wMpz7Un2vk',  # NOQA
        u'@icantbeluke Your kitty is so cute!!',  # NOQA
        u'My neighbours cat is so cute \U0001f64a\U0001f49c http://t.co/ihJh3TZwo5',  # NOQA
        u'Set de fotos: carloslovelycarlos: mostlycatsmostly: (via understanding-me-god) THIS CAT IS SO BEAUTIFUL http://t.co/ymtWcZodUP',  # NOQA
        u'On 23/06/14, at 10:37 PM, HeX \u03a9 wrote: &gt; kitty is so damn good, best content',  # NOQA
        u'@TheDaiIyKitten: Retweet if this cat made you say awww! OH EM THIS CAT IS SO DAMN CUTE \U0001f60d\U0001f60d\U0001f60d\U0001f60d\U0001f60d http://t.co/AsfU4lsDa3',  # NOQA
        u'MY CAT IS SO WEIRD WTF',  # NOQA
        u'@PardueSuzanne @Bdreamer7 \nHey honey! Our cat is so close to a quick death....quick take a picture before a wind hits.',  # NOQA
        u'@MargaudLiseuse that cat is so cute *_*',  # NOQA
        u'Srsly like my cat is so annoying',  # NOQA
        u'[Every cat is really the most beautiful woman in the room.] by E.V. Lucas',  # NOQA
        u'RT @ChazG_23: My cat is so soft and lovable\u2764\ufe0f\U0001f618 http://t.co/ii9TNb9ZUe',  # NOQA
        u'My cat is so soft and lovable\u2764\ufe0f\U0001f618 http://t.co/ii9TNb9ZUe',  # NOQA
        u'My cat is so cute &amp; peaceful when she sleeps \u2764\ufe0f\U0001f63b',  # NOQA
        u'my cat is so depressed he spent 90% of his time today staring at the window\n??????',  # NOQA
        u'this cat is so damn cute. i want u Miumiu :3 http://t.co/sXAsbYteKN',  # NOQA
        u'This cat is so pretty',  # NOQA
    ]

    def setUp(self):
        self.config = Cat()

    def test_generate(self):
        generated_actions = characteristics.generate(self.config, self.tweets)
        print repr(generated_actions)
        self.assertEqual(set(generated_actions), set([
            u'beautiful',
            u'cute',
            u'good',
            u'cute *_*',
            u'close to a quick death',
            u"annoying it's made u hate all cats",
            u'weird wtf',
            u'pretty',
            u'the most beautiful woman in the room',
            u'annoying',
            u'damn cute',
            u'soft',
            u'damn good',
        ]))

    def test_so_much(self):
        generated_characteristics = characteristics.generate(self.config, [
            u'my cat is so big that i cant carry her',
            u'my cat is so big i cant carry her',
        ])
        self.assertEqual(set(generated_characteristics), set([
            u'so big that u cant carry me',
            u'big u cant carry me',
        ]))
