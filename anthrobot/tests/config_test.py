import unittest
from anthrobot.config import Config


class ConfigTest(unittest.TestCase):
    def test_seeds(self):
        self.assertEqual(Cat().seeds(), [
            "your cat is",
            "your cat just",
            "your kitty is",
            "your kitty just",
            "my cat is",
            "my cat just",
            "my kitty is",
            "my kitty just",
        ])


class Cat(Config):
    nouns = ["cat", "kitty"]
