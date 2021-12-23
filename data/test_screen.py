from re import S
from unittest import TestCase
from faker import Faker
from data.screen import ScreenData

class Test_screen(TestCase):

    def test_create(self):

        obj = ScreenData()
        f = Faker()
        id = obj.create(
            'https://www.youtube.com/watch?v=DBnENlXt-H4',
            'https://joincake.imgix.net/neven-krcmarek-2Ni0lCRF9bw-unsplash.jpg?w=761&height=348&fit=crop&crop=edges&auto=format&dpr=1',            
        )

        self.assertIsInstance(
            id,
            tuple
        )

        self.assertIsInstance(
            id[0],
            int
        )

        self.assertIsInstance(
            id[1],
            str
        )