from unittest import TestCase
from random import randint

from interface.combat import modifiers, combat_data


class Test_modifiers(TestCase):

    def test_one(self):

        rand = randint(1,30)

        mod = modifiers(rand)

        self.assertIsInstance(
            mod,
            int
        )
